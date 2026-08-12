export const glossary = {
  "GxP": "Good practice requirements governing regulated life-sciences activities, including traceability, validation, and data integrity.",
  "PV": "Pharmacovigilance: the detection, assessment, understanding, and prevention of adverse effects or other medicine-related problems.",
  "ALCOA+": "Data-integrity principles: attributable, legible, contemporaneous, original, accurate, complete, consistent, enduring, and available.",
  inject: "A controlled challenge introduced to verify that a workflow detects, contains, and documents an expected failure mode.",
  "bounded workflow": "A workflow restricted to defined inputs, outputs, steps, authority, budget, and escalation paths.",
  "fail-closed": "A control posture that refuses to continue when a required condition cannot be verified.",
  abstention: "An explicit non-decision when evidence, authority, identity, terminology, unit, or time context is insufficient.",
  listedness: "Whether an adverse event is described in the reference safety information for a medicinal product.",
} as const;

export type GlossaryTerm = keyof typeof glossary;
