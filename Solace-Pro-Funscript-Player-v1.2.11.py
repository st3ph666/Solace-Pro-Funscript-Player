#!/usr/bin/env python3
"""Compatibility launcher for Solace Pro Funscript Player v1.2.11."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from solace_pro_player.main import main

if __name__ == "__main__":
    raise SystemExit(main())
