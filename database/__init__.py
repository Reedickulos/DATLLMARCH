"""Database API package.

This package provides a simple file‑based database stub.  It does not
use a real database backend; instead it reads and writes JSON to
``database/results.json`` specified in the configuration.  The API is
designed to mirror a subset of the functionality of ASI‑Arch's
MongoDB service, allowing the pipeline to sample parent
architectures and persist new results.
"""

from .mongodb_api import DatabaseAPI  # noqa: F401
