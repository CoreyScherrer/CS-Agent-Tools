"""Entrypoint so the tool runs as `python -m ma` with no install step."""

import sys

from .cli.main import main

if __name__ == "__main__":
    sys.exit(main())
