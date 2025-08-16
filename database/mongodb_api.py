"""File‑based database stub inspired by ASI‑Arch.

In the original ASI‑Arch framework the database layer provides a
MongoDB interface for storing architectures, results and the
evolutionary lineage.  This lightweight stub implements only two
operations:

* ``sample_parent`` returns the most promising architecture from the
  stored results or a default baseline if none exist.
* ``save_result`` appends a new analysis report to the JSON file on
  disk.

You can extend this class to support candidate sets, FAISS similarity
search and other advanced features as needed.
"""

from __future__ import annotations

import json
import os
from typing import Dict, List, Any


class DatabaseAPI:
    """Persist and retrieve architecture discovery results."""

    def __init__(self, config: Dict[str, Any]) -> None:
        self.file_path = config.get('database_path', 'database/results.json')
        # Ensure the directory exists.
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        # Initialise an empty file if it doesn't exist.
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def _load_all(self) -> List[Dict[str, Any]]:
        with open(self.file_path, encoding='utf-8') as f:
            return json.load(f)

    def _save_all(self, data: List[Dict[str, Any]]) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def sample_parent(self) -> Dict[str, Any]:
        """Return the best previous architecture or a default baseline.

        In a full implementation this method would query the database for
        the highest‑scoring architectures and sample one according to
        some strategy.  Here we simply return the last stored
        architecture with the highest composite score.  If the file is
        empty, we return a baseline architecture dictionary.
        """
        data = self._load_all()
        if not data:
            # Default baseline architecture.
            return {
                'id': 'baseline',
                'hidden_size': 512,
                'num_layers': 6,
                'num_heads': 8,
            }
        # Find the entry with the highest composite score.
        best = max(data, key=lambda x: x.get('composite_score', 0))
        # Each entry stores the full architecture under 'architecture'.
        return best.get('architecture', {
            'hidden_size': 512,
            'num_layers': 6,
            'num_heads': 8,
        })

    def save_result(self, report: Any) -> None:
        """Append an analysis report to the results file."""
        # Convert dataclasses to plain dicts.
        entry = {
            'architecture': report.architecture,
            'evaluation': {
                'performance': report.evaluation.performance,
                'novelty': report.evaluation.novelty,
                'complexity': report.evaluation.complexity,
                'raw_response': report.evaluation.raw_response,
            },
            'composite_score': report.composite_score,
            'summary': report.summary,
        }
        data = self._load_all()
        data.append(entry)
        self._save_all(data)
