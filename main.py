#!/usr/bin/env python3
"""Entry program for the make.fun news-image-20261123 competition.

Writes the front page of THE WORLD TODAY for Monday 23 November 2026
to /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png).

The page was typeset in-session by render.py (PIL, Liberation fonts,
original illustrations generated in-session) at 2048x2048, Lanczos
downscaled to 1024x1024 and saved as JPEG quality 93 with 4:4:4 chroma.
The grader sandbox runs Python 3.13 standard library only, with no
network and no PIL, so this program ships the rendered image beside it
and copies it byte-identically to the output directory -- the pattern
the kit's starter documents ("its image is the entry.png beside this
file, and the program copies it to /output/entry.png").

The copy is deterministic: the same bytes are written on every run.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
MAX_BYTES = 1048576
JPEG_MAGIC = b"\xff\xd8\xff"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"

    if not SOURCE.is_file():
        print(f"error: shipped image {SOURCE} is missing", file=sys.stderr)
        return 1
    data = SOURCE.read_bytes()
    if data[:3] != JPEG_MAGIC and data[:8] != PNG_MAGIC:
        print("error: entry.png has neither JPEG nor PNG magic bytes",
              file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"error: entry.png is {len(data)} bytes, over the 1 MiB cap",
              file=sys.stderr)
        return 1

    # shutil.copyfile copies raw bytes: no re-encode, no metadata change,
    # so the output is byte-identical to the shipped image on every run.
    if target.is_file() and target.read_bytes() == data:
        print(f"{target} already holds the entry image "
              f"({len(data)} bytes, sha256={hashlib.sha256(data).hexdigest()})")
        return 0
    shutil.copyfile(SOURCE, target)
    written = target.read_bytes()
    if written != data:
        print("error: copied bytes differ from the shipped image",
              file=sys.stderr)
        return 1

    print(f"wrote {target}  {len(data)} bytes  "
          f"sha256={hashlib.sha256(data).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
