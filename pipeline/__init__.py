"""Architecture discovery pipeline package.

This package contains a very lightweight implementation of a
multi-agent pipeline inspired by the ASI-Arch framework.  Each module
encapsulates a specific phase of the discovery cycle: evolution,
evaluation and analysis.  The `pipeline` module orchestrates the
overall loop.
"""

from .pipeline import ArchitecturePipeline  # noqa: F401
