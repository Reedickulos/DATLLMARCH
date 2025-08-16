"""Architecture evolver.

This module implements a toy architecture evolution algorithm.  In a
full ASI‑Arch implementation the evolver would reason about
transformer architectures, attention mechanisms and other neural
building blocks.  Here we represent an architecture as a simple
dictionary with a few hyper‑parameters and apply small random
perturbations to those parameters to produce new candidates.
"""

from __future__ import annotations

import copy
import random
from typing import Dict, Any


class ArchitectureEvolver:
    """Generate new candidate architectures by evolving a parent.

    Each architecture is represented as a dict with a handful of
    numeric hyper‑parameters.  The evolver makes a copy of the parent
    and adds gaussian noise to the hyper‑parameters to create a new
    candidate.
    """

    def __init__(self, noise_scale: float = 0.1) -> None:
        self.noise_scale = noise_scale

    def evolve(self, parent: Dict[str, Any]) -> Dict[str, Any]:
        """Return a mutated copy of the parent architecture.

        Parameters
        ----------
        parent : dict
            Dictionary describing the parent architecture.  Should
            contain numeric hyper‑parameters such as ``hidden_size`` and
            ``num_layers``.  Any other fields are copied verbatim.

        Returns
        -------
        dict
            A new architecture dict with slightly perturbed
            hyper‑parameters.
        """
        candidate = copy.deepcopy(parent)
        # Define which keys to mutate.  Unknown keys are copied as‑is.
        numeric_keys = {
            'hidden_size': (32, 2048),
            'num_layers': (1, 48),
            'num_heads': (1, 32),
        }
        for key, (low, high) in numeric_keys.items():
            if key in candidate and isinstance(candidate[key], (int, float)):
                # Add integer noise scaled to the range size.
                range_size = high - low
                noise = int(random.gauss(0, self.noise_scale) * range_size)
                new_value = candidate[key] + noise
                # Clamp to valid range.
                candidate[key] = int(max(low, min(high, new_value)))
            else:
                # If missing, initialise with a sensible default mid‑range.
                candidate[key] = int((low + high) / 2)
        # Tag the architecture with a new id for tracking.
        candidate['id'] = f"arch_{random.randint(0, 10_000_000):07d}"
        return candidate
