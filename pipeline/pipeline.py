"""Simple architecture discovery pipeline.

This module wires together the evolver, evaluator and analyzer to
perform a single cycle of architecture discovery.  It uses a
file-based database to store results and optionally integrates with
DAT LLM via the shared LLaMA 3 model running on Ollama.

Example usage:

```python
from pipeline import ArchitecturePipeline
import json

config = json.load(open('config.json'))
pipeline = ArchitecturePipeline(config)
report = pipeline.run_cycle()
print(report)
```
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Optional

from .evolve import ArchitectureEvolver
from .eval import ArchitectureEvaluator, EvaluationResult
from .analyze import ArchitectureAnalyzer, AnalysisReport
from ..database.mongodb_api import DatabaseAPI


@dataclass
class ArchitecturePipeline:
    """Orchestrates a single architecture discovery cycle.

    Parameters
    ----------
    config : dict
        Configuration dictionary loaded from ``config.json``.
    """

    config: Dict[str, Any]

    def __post_init__(self) -> None:
        self.evolver = ArchitectureEvolver()
        self.evaluator = ArchitectureEvaluator(self.config)
        self.analyzer = ArchitectureAnalyzer()
        self.db = DatabaseAPI(self.config)

    def run_cycle(self) -> AnalysisReport:
        """Run a single evolution–evaluation–analysis loop.

        Returns
        -------
        AnalysisReport
            A report containing the candidate architecture, its
            evaluation metrics and a summary analysis.
        """
        # Step 1: sample a parent architecture from the database.  If
        # none exists we start from a default baseline.
        parent_arch = self.db.sample_parent()

        # Step 2: evolve the parent into a new candidate.
        candidate_arch = self.evolver.evolve(parent_arch)

        # Step 3: evaluate the candidate using the configured LLM.
        evaluation: EvaluationResult = self.evaluator.evaluate(candidate_arch)

        # Step 4: analyse the result and compute summary metrics.
        report: AnalysisReport = self.analyzer.analyze(candidate_arch, evaluation)

        # Persist the report to the database.
        self.db.save_result(report)

        return report



def main() -> None:
    """Entry point for command-line usage."""
    # Determine the path to the top-level config.  When running as a
    # module (e.g. ``python -m DATLLM_ASI_Arch.pipeline.pipeline``)
    # ``__file__`` points into the ``pipeline/`` directory.  We
    # construct the root directory two levels above and load
    # ``config.json`` from there.
    import os
    # The repository root is the parent directory of this ``pipeline``
    # package.  ``__file__`` points to ``.../DATLLM_ASI_Arch/pipeline/pipeline.py``.
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    config_path = os.path.join(root_dir, 'config.json')
    with open(config_path, encoding='utf-8') as f:
        config = json.load(f)
    pipeline = ArchitecturePipeline(config)
    num_cycles = config.get('num_cycles', 1)
    for i in range(num_cycles):
        report = pipeline.run_cycle()
        print(f"\nCycle {i + 1} report:\n{report}\n")


if __name__ == '__main__':
    main()
