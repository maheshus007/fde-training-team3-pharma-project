"""Evaluation adapters — bridge public fixtures to workflow contracts."""

from .workflow_adapter import WorkflowAdapter, adapt_public_fixture

__all__ = ["WorkflowAdapter", "adapt_public_fixture"]
