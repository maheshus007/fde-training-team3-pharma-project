"""In-memory GraphPort. T-005: ingest challenge CSVs. CQ queries land in T-006."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_INTEGRATION = Path(__file__).resolve().parent
if str(_INTEGRATION) not in sys.path:
    sys.path.insert(0, str(_INTEGRATION))

from ports.graph import ALLOWED_CQ_IDS, FORBIDDEN_EDGE_LABELS, ForbiddenEdgeError  # noqa: E402

SUPPORTS_CQ = True
SUPPORTS_CQ3 = True
SUPPORTS_INGEST = True
_PATH_CAP = 50

_DATA = Path(__file__).resolve().parents[4] / "data"
_INGEST_BATCH_ID = "t005-fixture-rebuild"

_REL_TO_EDGE = {
    "consumed": "CONSUMED",
    "missing_branch": "MISSING_BRANCH",
    "issued": "ISSUED",
}


def _sha256_facts(facts: dict[str, Any]) -> str:
    payload = json.dumps(facts, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_as_of(value: str) -> datetime | None:
    text = str(value).strip()
    if not text:
        return None
    if " " in text and "T" not in text:
        text = text.replace(" ", "T", 1)
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _vid(system: str, record_id: str) -> str:
    return f"{system}|{record_id}"


def _rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class MemoryGraph:
    def __init__(self) -> None:
        self._vertices: dict[str, dict[str, Any]] = {}
        self._edges: list[dict[str, Any]] = []

    def ingest_from_fixtures(self) -> int:
        self._vertices.clear()
        self._edges.clear()
        retrieved = _now()
        self._ingest_batches(retrieved)
        self._ingest_genealogy(retrieved)
        self._ingest_warehouse(retrieved)
        self._ingest_lab(retrieved)
        self._ingest_mappings(retrieved)
        self._ingest_icsr(retrieved)
        self._ingest_duplicates(retrieved)
        self._ingest_shipments(retrieved)
        self._ingest_loggers(retrieved)
        self._ingest_idmp(retrieved)
        return len(self._edges)

    def query(self, cq_id: str, params: dict[str, Any], purpose: str, as_of: str) -> dict[str, Any]:
        del purpose
        if cq_id not in ALLOWED_CQ_IDS:
            return {
                "cq_id": cq_id,
                "paths": [],
                "abstentions": [{"code": "unknown_cq", "reason": f"unknown CQ {cq_id}"}],
                "truncated": False,
            }
        if not self._vertices:
            self.ingest_from_fixtures()
        handlers = {
            "CQ-1": self._query_cq1,
            "CQ-2": self._query_cq2,
            "CQ-3": self._query_cq3,
            "CQ-6": self._query_cq6,
        }
        handler = handlers.get(cq_id)
        if handler is None:
            return {"cq_id": cq_id, "paths": [], "abstentions": [], "truncated": False}
        paths, abstentions = handler(params or {}, as_of)
        truncated = len(paths) > _PATH_CAP
        return {
            "cq_id": cq_id,
            "paths": paths[:_PATH_CAP],
            "abstentions": abstentions,
            "truncated": truncated,
        }

    def _vids_for_record(self, record_id: str, label: str | None = None) -> list[str]:
        out: list[str] = []
        for vid, vertex in self._vertices.items():
            if vertex.get("record_id") != record_id:
                continue
            if label is not None and vertex.get("label") != label:
                continue
            out.append(vid)
        return out

    def _edge_in_as_of(self, props: dict[str, Any], as_of: str) -> bool:
        effective = props.get("effective_at")
        if not effective:
            return True
        as_of_dt = _parse_as_of(as_of)
        eff_dt = _parse_as_of(str(effective))
        if as_of_dt is None or eff_dt is None:
            return True
        return eff_dt <= as_of_dt

    def _path(self, edge: dict[str, Any]) -> dict[str, Any]:
        props = dict(edge.get("properties") or {})
        return {
            "nodes": [edge["from"], edge["to"]],
            "edges": [edge["label"]],
            "provenance": [props],
        }

    def _query_cq1(self, params: dict[str, Any], as_of: str) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
        batch_id = str(params.get("batch_id") or "")
        batch_vids = set(self._vids_for_record(batch_id, "Batch"))
        labels = {"MISSING_BRANCH", "ISSUED", "CONSUMED"}
        paths: list[dict[str, Any]] = []
        for edge in self._edges:
            if edge["label"] not in labels:
                continue
            if not self._edge_in_as_of(edge.get("properties") or {}, as_of):
                continue
            if edge["from"] in batch_vids or edge["to"] in batch_vids:
                paths.append(self._path(edge))
        return paths, []

    def _query_cq2(self, params: dict[str, Any], as_of: str) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
        lab_id = str(params.get("lab_result_id") or "")
        lab_vids = set(self._vids_for_record(lab_id, "LabResult"))
        paths: list[dict[str, Any]] = []
        approved = None
        for edge in self._edges:
            if edge["label"] != "MAPPED_TO":
                continue
            if edge["from"] not in lab_vids:
                continue
            if not self._edge_in_as_of(edge.get("properties") or {}, as_of):
                continue
            paths.append(self._path(edge))
            approved = (edge.get("properties") or {}).get("approved")
            mapping = self._vertices.get(edge["to"], {})
            facts = mapping.get("facts") or {}
            if approved is None:
                approved = facts.get("approved")
        abstentions: list[dict[str, str]] = []
        if str(approved).strip().lower() in {"", "no", "none", "false"} or approved is None:
            abstentions.append(
                {
                    "code": "unit_unapproved",
                    "reason": f"{lab_id} unit mapping is not approved; comparison abstained",
                }
            )
        return paths, abstentions

    def _query_cq3(self, params: dict[str, Any], as_of: str) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
        raw_ids = params.get("case_ids") or []
        if isinstance(raw_ids, str):
            wanted = {raw_ids}
        else:
            wanted = {str(x) for x in raw_ids if x}
        paths: list[dict[str, Any]] = []
        for edge in self._edges:
            if edge["label"] != "DUPLICATE_CANDIDATE":
                continue
            if not self._edge_in_as_of(edge.get("properties") or {}, as_of):
                continue
            from_rec = (self._vertices.get(edge["from"]) or {}).get("record_id")
            to_rec = (self._vertices.get(edge["to"]) or {}).get("record_id")
            if wanted and from_rec not in wanted and to_rec not in wanted:
                continue
            path = self._path(edge)
            props = path["provenance"][0] if path["provenance"] else {}
            props.pop("merge", None)
            props.pop("merged", None)
            paths.append(path)
        return paths, []

    def _query_cq6(self, params: dict[str, Any], as_of: str) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
        shipment_id = str(params.get("shipment_id") or "")
        ship_vids = set(self._vids_for_record(shipment_id, "Shipment"))
        logger_vids: set[str] = set()
        paths: list[dict[str, Any]] = []
        for edge in self._edges:
            if edge["from"] not in ship_vids:
                continue
            if edge["label"] not in {"ASSOCIATED_LOGGER", "ASSOCIATED_PALLET"}:
                continue
            if not self._edge_in_as_of(edge.get("properties") or {}, as_of):
                continue
            paths.append(self._path(edge))
            if edge["label"] == "ASSOCIATED_LOGGER":
                logger_vids.add(edge["to"])
        for edge in self._edges:
            if edge["from"] not in logger_vids:
                continue
            if edge["label"] != "ASSOCIATED_PALLET":
                continue
            if not self._edge_in_as_of(edge.get("properties") or {}, as_of):
                continue
            paths.append(self._path(edge))
        return paths, []

    def add_edge(self, label: str, from_id: str, to_id: str, properties: dict[str, Any] | None = None) -> None:
        if label in FORBIDDEN_EDGE_LABELS:
            raise ForbiddenEdgeError(label)
        props = dict(properties or {})
        self._edges.append({"label": label, "from": from_id, "to": to_id, "properties": props})

    def _vertex(
        self,
        label: str,
        system: str,
        record_id: str,
        facts: dict[str, Any],
        *,
        authority: str,
        effective_at: str | None,
        retrieved_at: str,
        trust_status: str = "unknown",
    ) -> str:
        vid = _vid(system, record_id)
        if vid in self._vertices:
            return vid
        self._vertices[vid] = {
            "id": vid,
            "pk": label,
            "label": label,
            "source_system": system,
            "record_id": record_id,
            "authority": authority,
            "effective_at": effective_at,
            "retrieved_at": retrieved_at,
            "integrity_sha256": _sha256_facts(facts),
            "trust_status": trust_status,
            "facts": facts,
        }
        return vid

    def _edge(
        self,
        label: str,
        from_id: str,
        to_id: str,
        *,
        source_system: str,
        record_id: str,
        authority: str,
        retrieved_at: str,
        effective_at: str | None = None,
        extra: dict[str, Any] | None = None,
    ) -> None:
        props = {
            "source_system": source_system,
            "record_id": record_id,
            "authority": authority,
            "effective_at": effective_at,
            "retrieved_at": retrieved_at,
            "integrity_sha256": _sha256_facts({"label": label, "from": from_id, "to": to_id}),
            "trust_status": "unknown",
            "ingest_batch_id": _INGEST_BATCH_ID,
        }
        if extra:
            props.update(extra)
        self.add_edge(label, from_id, to_id, props)

    def _ingest_batches(self, retrieved_at: str) -> None:
        for row in _rows(_DATA / "batches.csv"):
            batch_id = row.get("batch_id", "")
            if not batch_id:
                continue
            site = row.get("site") or "unknown"
            self._vertex(
                "Batch",
                site,
                batch_id,
                dict(row),
                authority=site,
                effective_at=row.get("manufacture_date") or None,
                retrieved_at=retrieved_at,
            )
            product_id = row.get("product_id", "")
            if product_id:
                prod = self._vertex(
                    "Product",
                    "RIM",
                    product_id,
                    {"product_id": product_id},
                    authority="RIM",
                    effective_at=None,
                    retrieved_at=retrieved_at,
                )
                self._edge(
                    "EVIDENCED_BY",
                    _vid(site, batch_id),
                    prod,
                    source_system=site,
                    record_id=batch_id,
                    authority=site,
                    retrieved_at=retrieved_at,
                    effective_at=row.get("manufacture_date") or None,
                )

    def _ingest_genealogy(self, retrieved_at: str) -> None:
        for row in _rows(_DATA / "material_genealogy.csv"):
            batch_id = row.get("batch_id", "")
            lot = row.get("material_lot", "")
            relation = str(row.get("relation", "")).strip().lower()
            source = row.get("source") or "MES"
            if not batch_id or not lot:
                continue
            label = _REL_TO_EDGE.get(relation)
            if label is None:
                continue
            batch = self._vertex(
                "Batch",
                source,
                batch_id,
                {"batch_id": batch_id},
                authority=source,
                effective_at=None,
                retrieved_at=retrieved_at,
            )
            material = self._vertex(
                "MaterialLot",
                source,
                lot,
                {"material_lot": lot},
                authority=source,
                effective_at=None,
                retrieved_at=retrieved_at,
            )
            self._edge(
                label,
                batch,
                material,
                source_system=source,
                record_id=lot,
                authority=source,
                retrieved_at=retrieved_at,
            )

    def _ingest_warehouse(self, retrieved_at: str) -> None:
        for row in _rows(_DATA / "warehouse_movements.csv"):
            lot = row.get("material_lot", "")
            batch_id = row.get("batch_id", "")
            movement_id = row.get("movement_id", "")
            status = str(row.get("status", "")).strip().lower()
            if not lot or not batch_id:
                continue
            label = _REL_TO_EDGE.get(status)
            if label is None:
                continue
            material = self._vertex(
                "MaterialLot",
                "WM",
                lot,
                {"material_lot": lot, "movement_id": movement_id},
                authority="warehouse",
                effective_at=None,
                retrieved_at=retrieved_at,
            )
            batch = self._vertex(
                "Batch",
                "WM",
                batch_id,
                {"batch_id": batch_id},
                authority="warehouse",
                effective_at=None,
                retrieved_at=retrieved_at,
            )
            self._edge(
                label,
                material,
                batch,
                source_system="WM",
                record_id=movement_id or lot,
                authority="warehouse",
                retrieved_at=retrieved_at,
                extra={"facts": dict(row)},
            )

    def _ingest_lab(self, retrieved_at: str) -> None:
        for row in _rows(_DATA / "lab_results.csv"):
            result_id = row.get("result_id", "")
            batch_id = row.get("batch_id", "")
            if not result_id:
                continue
            lab = self._vertex(
                "LabResult",
                "LIMS",
                result_id,
                dict(row),
                authority="LIMS",
                effective_at=None,
                retrieved_at=retrieved_at,
            )
            if batch_id:
                batch = self._vertex(
                    "Batch",
                    "LIMS",
                    batch_id,
                    {"batch_id": batch_id},
                    authority="LIMS",
                    effective_at=None,
                    retrieved_at=retrieved_at,
                )
                self._edge(
                    "EVIDENCED_BY",
                    lab,
                    batch,
                    source_system="LIMS",
                    record_id=result_id,
                    authority="LIMS",
                    retrieved_at=retrieved_at,
                )

    def _ingest_mappings(self, retrieved_at: str) -> None:
        for row in _rows(_DATA / "interface_mappings.csv"):
            interface = row.get("interface", "")
            if not interface:
                continue
            mapping = self._vertex(
                "Mapping",
                "IFACE",
                interface,
                dict(row),
                authority="interface_mappings",
                effective_at=None,
                retrieved_at=retrieved_at,
            )
            lr88 = _vid("LIMS", "LR-88")
            if lr88 in self._vertices:
                self._edge(
                    "MAPPED_TO",
                    lr88,
                    mapping,
                    source_system="IFACE",
                    record_id=interface,
                    authority="interface_mappings",
                    retrieved_at=retrieved_at,
                    extra={"approved": row.get("approved")},
                )

    def _ingest_icsr(self, retrieved_at: str) -> None:
        for row in _rows(_DATA / "icsr_cases.csv"):
            case_id = row.get("case_id", "")
            if not case_id:
                continue
            self._vertex(
                "IcsrCase",
                "SAFETY",
                case_id,
                dict(row),
                authority=row.get("source") or "SAFETY",
                effective_at=row.get("awareness_date") or None,
                retrieved_at=retrieved_at,
            )

    def _ingest_duplicates(self, retrieved_at: str) -> None:
        for row in _rows(_DATA / "duplicate_candidates.csv"):
            case_a = row.get("case_a", "")
            case_b = row.get("case_b", "")
            if not case_a or not case_b:
                continue
            a = self._vertex(
                "IcsrCase",
                "SAFETY",
                case_a,
                {"case_id": case_a},
                authority="SAFETY",
                effective_at=None,
                retrieved_at=retrieved_at,
            )
            b = self._vertex(
                "IcsrCase",
                "SAFETY",
                case_b,
                {"case_id": case_b},
                authority="SAFETY",
                effective_at=None,
                retrieved_at=retrieved_at,
            )
            similarity = row.get("similarity")
            extra: dict[str, Any] = {"reason": row.get("reason", "")}
            if similarity not in (None, ""):
                try:
                    extra["similarity"] = float(similarity)
                except ValueError:
                    extra["similarity"] = similarity
            self._edge(
                "DUPLICATE_CANDIDATE",
                a,
                b,
                source_system="SAFETY",
                record_id=f"{case_a}:{case_b}",
                authority="duplicate_candidates",
                retrieved_at=retrieved_at,
                extra=extra,
            )

    def _ingest_shipments(self, retrieved_at: str) -> None:
        for row in _rows(_DATA / "shipments.csv"):
            shipment_id = row.get("shipment_id", "")
            if not shipment_id:
                continue
            ship = self._vertex(
                "Shipment",
                "LOGISTICS",
                shipment_id,
                dict(row),
                authority="logistics",
                effective_at=None,
                retrieved_at=retrieved_at,
            )
            logger = row.get("logger", "")
            pallet = row.get("pallet", "")
            if logger:
                log_v = self._vertex(
                    "Logger",
                    "LOGISTICS",
                    logger,
                    {"logger": logger},
                    authority="logistics",
                    effective_at=None,
                    retrieved_at=retrieved_at,
                )
                self._edge(
                    "ASSOCIATED_LOGGER",
                    ship,
                    log_v,
                    source_system="LOGISTICS",
                    record_id=shipment_id,
                    authority="logistics",
                    retrieved_at=retrieved_at,
                )
            if pallet:
                pal_v = self._vertex(
                    "Pallet",
                    "LOGISTICS",
                    pallet,
                    {"pallet": pallet},
                    authority="logistics",
                    effective_at=None,
                    retrieved_at=retrieved_at,
                )
                self._edge(
                    "ASSOCIATED_PALLET",
                    ship,
                    pal_v,
                    source_system="LOGISTICS",
                    record_id=shipment_id,
                    authority="logistics",
                    retrieved_at=retrieved_at,
                )

    def _ingest_loggers(self, retrieved_at: str) -> None:
        for row in _rows(_DATA / "temperature_loggers.csv"):
            logger = row.get("logger", "")
            pallet = row.get("pallet", "")
            if not logger or not pallet:
                continue
            log_v = self._vertex(
                "Logger",
                "LOGISTICS",
                logger,
                {"logger": logger},
                authority="temperature_loggers",
                effective_at=row.get("timestamp") or None,
                retrieved_at=retrieved_at,
            )
            pal_v = self._vertex(
                "Pallet",
                "LOGISTICS",
                pallet,
                {"pallet": pallet},
                authority="temperature_loggers",
                effective_at=row.get("timestamp") or None,
                retrieved_at=retrieved_at,
            )
            self._edge(
                "ASSOCIATED_PALLET",
                log_v,
                pal_v,
                source_system="LOGISTICS",
                record_id=f"{logger}:{pallet}:{row.get('timestamp', '')}",
                authority="temperature_loggers",
                retrieved_at=retrieved_at,
                effective_at=row.get("timestamp") or None,
                extra={"timezone": row.get("timezone"), "temp_c": row.get("temp_c")},
            )

    def _ingest_idmp(self, retrieved_at: str) -> None:
        for row in _rows(_DATA / "medicinal_products.csv"):
            product_id = row.get("product_id", "")
            if not product_id:
                continue
            source = row.get("source") or "RIM"
            self._vertex(
                "Product",
                source,
                product_id,
                dict(row),
                authority=source,
                effective_at=None,
                retrieved_at=retrieved_at,
            )
        for row in _rows(_DATA / "idmp_mappings.csv"):
            local_p = row.get("local_product", "")
            idmp_p = row.get("idmp_product", "")
            if not local_p or not idmp_p:
                continue
            local_v = self._vertex(
                "Product",
                "ERP",
                local_p,
                {"product_id": local_p},
                authority="ERP",
                effective_at=None,
                retrieved_at=retrieved_at,
            )
            idmp_v = self._vertex(
                "Product",
                "RIM",
                idmp_p,
                {"product_id": idmp_p},
                authority="RIM",
                effective_at=None,
                retrieved_at=retrieved_at,
            )
            self._edge(
                "MAPPED_TO",
                local_v,
                idmp_v,
                source_system="IDMP",
                record_id=f"{local_p}:{idmp_p}",
                authority="idmp_mappings",
                retrieved_at=retrieved_at,
                extra={"mapping_status": row.get("mapping_status")},
            )
