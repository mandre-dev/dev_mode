"""Ponto de entrada (compat) para rodar sem instalar pacote."""

import os
import sys

# Permite `python3 run_dev_mode.py` sem instalar.
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from dev_mode.__main__ import main  # noqa: E402

if __name__ == "__main__":
    main()
