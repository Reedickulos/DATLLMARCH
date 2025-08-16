"""Result analysis module.

This module defines the analysis step of the discovery pipeline.  Given
an architecture and its evaluation metrics, it computes a composite
score and produces a short textual summary.  In more advanced
implementations this step could call an LLM to produce a natural
language report comparing the candidate against baselines and prior
experiments.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .eval import EvaluationResult


@dataclass
class AnalysisReport:
    """Encapsulate the results of one architecture evaluation cycle."""
    architecture: Dict[str, any]
    evaluation: EvaluationResult
    composite_score: float
    summary: str


class ArchitectureAnalyzer:
    """Compute a composite score and generate a simple summary."""

    def analyze(self, architecture: Dict[str, any], evaluation: EvaluationResult) -> AnalysisReport:
        # Weighted composite: emphasise performance, reward novelty,
        # penalise complexity.  We normalise the scores between 0 and 1.
        composite = (
            0.6 * evaluation.performance +
            0.3 * evaluation.novelty -
            0.1 * evaluation.complexity
        )
        composite = max(0.0, min(1.0, composite))
        summary = (
            f"Architecture {architecture.get('id', 'unknown')} achieved a "
            f"performance score of {evaluation.performance:.2f}, "
            f"novelty score of {evaluation.novelty:.2f} and "
            f"complexity score of {evaluation.complexity:.2f}. "
            f"Composite score: {composite:.2f}."
        )
        return AnalysisReport(architecture, evaluation, composite, summary)
