# C4 Level 3 — Components

## Shared

AuthZChecker, PurposeBinder, ManifestVerifier, BudgetController, CheckpointStore, AuditLogger, SchemaValidator, PolicyGuard, IdempotencyStore.

## Workflow A

GenealogyReconciler, LabUnitGate, OosConflictPresenter, PacketGapFinder, ReadinessAssessor.

## Workflow B

IntakeNormalizer, DuplicateCandidateService, ClockConflictPresenter, ListednessPresenter, SensitiveSegmentGate, SocialAuthenticityGate.

## Workflow C

ConstraintEnumerator, ColdChainAssociationChecker, DraftOptionRanker, EthicsChannelFlagger.

## Platform

OntologyResolver, RerAssembler, KgIngestor (provisional), KgQueryService (provisional), AgentPlanner, ToolDispatcher, InferencePort.

## FR ↔ component map

| FR | Primary components |
|---|---|
| FR-A | GenealogyReconciler, LabUnitGate, OosConflictPresenter, PacketGapFinder, ReadinessAssessor |
| FR-B | IntakeNormalizer, DuplicateCandidateService, ClockConflictPresenter, ListednessPresenter, SensitiveSegmentGate, SocialAuthenticityGate |
| FR-C | ConstraintEnumerator, ColdChainAssociationChecker, DraftOptionRanker, EthicsChannelFlagger |
| FR-D | AgentPlanner, ToolDispatcher, BudgetController, CheckpointStore, IdempotencyStore |
| FR-E | OntologyResolver, RerAssembler, Kg* (provisional) |
| FR-F | HITL workbench UI |
