#!/usr/bin/env python3

import os
import sys


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from deck_to_pptx_lib.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
