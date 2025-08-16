"""Architecture evaluator.

This module defines an evaluator that calls a local LLaMA 3 model via
the Ollama HTTP API to score candidate architectures.  It attempts
to extract a JSON object with ``performance``, ``novelty`` and
``complexity`` scores from the model's output.  If the call fails or
parsing does not succeed, random scores are generated as a fallback.
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from typing import Dict, Any

import requests


@dataclass
class EvaluationResult:
    """Container for architecture evaluation metrics."""
    performance: float
    novelty: float
    complexity: float
    raw_response: str


class ArchitectureEvaluator:
    """Score architectures using a local LLaMA 3 model.

    Parameters
    ----------
    config : dict
        Configuration dictionary loaded from ``config.json``.  Must
        contain at least the ``model`` name and a boolean flag
        ``use_local_model`` indicating whether to call Ollama.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        self.model = config.get('model', 'llama3')
        self.use_local = config.get('use_local_model', True)

    def _call_llm(self, prompt: str) -> str:
        """Call the Ollama generate API and return the raw response text.

        Raises
        ------
        requests.RequestException
            If the HTTP request fails.
        ValueError
            If the response does not contain a 'response' field.
        """
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        r = requests.post(url, json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()
        if 'response' not in data:
            raise ValueError(f"Unexpected response from LLM API: {data}")
        return data['response']

    def evaluate(self, architecture: Dict[str, Any]) -> EvaluationResult:
        """Return evaluation metrics for a candidate architecture.

        The prompt requests the LLM to return a JSON object with
        numeric fields ``performance``, ``novelty`` and ``complexity``
        each in the range [0, 1].  These values are meant to capture
        how strong the architecture is relative to a baseline, how
        different it is from known designs, and how computationally
        complex it might be.  In practice you may design your own
        scoring rubric.

        If anything goes wrong during the LLM call, random scores are
        generated as a fallback.

        Parameters
        ----------
        architecture : dict
            Candidate architecture description.

        Returns
        -------
        EvaluationResult
            The resulting metrics and raw model output.
        """
        prompt = (
            "You are an expert model architect. Given the following "
            "architecture description in JSON, assess its quality.\n"
            "Architecture: " + json.dumps(architecture) + "\n"
            "Return a JSON object with keys 'performance', 'novelty' "
            "and 'complexity', each between 0 and 1, representing your "
            "estimates of how strong, novel and complex this design is. "
            "Do not include any additional commentary.\n"
        )
        raw = ''
        if self.use_local:
            try:
                raw = self._call_llm(prompt)
                # Try to extract JSON from the model's response.
                # Some models wrap JSON in triple backticks; remove them.
                cleaned = raw.strip().strip('```').strip()
                metrics = json.loads(cleaned)
                return EvaluationResult(
                    performance=float(metrics.get('performance', 0.0)),
                    novelty=float(metrics.get('novelty', 0.0)),
                    complexity=float(metrics.get('complexity', 0.0)),
                    raw_response=raw,
                )
            except Exception:
                # Fall back to random values.
                pass
        # Generate random scores if LLM call is disabled or fails.
        return EvaluationResult(
            performance=random.random(),
            novelty=random.random(),
            complexity=random.random(),
            raw_response=raw or 'fallback',
        )
