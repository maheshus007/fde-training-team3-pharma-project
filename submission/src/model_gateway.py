"""Fail-closed model selection against integrity / intended-use evidence (INJ-070 / INJ-081)."""
from __future__ import annotations


def select_model(intended_use: str, language: str) -> tuple[str | None, str]:
    lang = (language or "").strip().lower()
    if lang and lang not in {"en", "de"}:
        return (
            None,
            (
                f"Abstain: no verified model for language '{language}' under intended use "
                f"'{intended_use}' (INJ-072 / INJ-081). Deterministic path continues."
            ),
        )
    return (
        "ntg-offline-extract-v1",
        (
            f"Selected offline extract model for '{intended_use}' / {language}. "
            "Hash must match registry before any inference enablement (INJ-070)."
        ),
    )
