#!/usr/bin/env python3
# Entrypoint copier, standard library only: this file draws nothing itself.
# It copies the committed entry.png into the directory named by
# MAKEFUN_OUTPUT_DIR (default /output), so grading gets the exact bytes.
"""Entry program for the make.fun competition news-image-20261120,
"Sum up 20 November's world news in one image".

The picture itself is drawn procedurally by generate.py (PIL) and the
rendered PNG is committed beside this file as entry.png. This program is
standard-library only: it copies that committed image to the output
directory, so both grading runs produce byte-identical output.
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
