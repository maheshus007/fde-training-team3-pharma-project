import type { Product } from "@/lib/schemas";

export const products: Product[] = [
  { id: "all", name: "All NovaCura programs", description: "Portfolio-wide AEGIS-PHARMA assurance view." },
  { id: "NCX-101", name: "NCX-101", description: "Investigational oncology compound with a phase II evidence program." },
  { id: "NCB-204", name: "NCB-204", description: "Biologics process-development program requiring batch evidence review." },
  { id: "NCS-310", name: "NCS-310", description: "Specialty-care therapy monitored through pharmacovigilance workflows." },
  { id: "NCR-415", name: "NCR-415", description: "Respiratory portfolio program with supply and quality signal dependencies." },
];
