#!/usr/bin/env python3
import sys
from argparse import ArgumentParser
from logging import getLogger
from pathlib import Path
from subprocess import run

import coloredlogs

logger = getLogger(__name__)
coloredlogs.install()


def encode(src: Path, dst: Path):
    CMD = (
        "HandBrakeCLI",
        "--main-feature",
        "--preset",
        "Fast 1080p30",
        "-i",
        str(src),
        "-o",
        str(dst),
    )
    run(CMD, check=True, capture_output=True, encoding="utf8")


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("INDIR", help="Directory containing dvds.", type=Path)
    parser.add_argument(
        "--outdir", help="Directory to save m4vs if different from INDIR.", type=Path
    )
    parser.add_argument(
        "--dry-run", help="Don't encode, just print.", action="store_true"
    )
    args = parser.parse_args()

    if args.dry_run:
        coloredlogs.set_level("DEBUG")

    VIDEOS = args.INDIR.expanduser()
    OUTDIR = (args.outdir or VIDEOS).expanduser()

    process = list(VIDEOS.glob("*.iso"))
    process += [x for x in VIDEOS.glob("*") if x.is_dir() and (x / "VIDEO_TS").is_dir()]

    # we search this way around as sometimes we have manually split the dvd up,
    # e.g. by episode, and we want to catch this and avoid re-encoding.

    m4vs = list(OUTDIR.glob("*.m4v"))
    failed = []

    for video in process:
        if any(video.stem in x.name for x in m4vs):
            logger.debug(f"Skipping {video} as already encoded.")
        else:
            encoded = OUTDIR / (video.stem + ".m4v")
            logger.info(f"Encoding {video} to {encoded}.")
            if not args.dry_run:
                try:
                    encode(video, encoded)
                except Exception as e:
                    failed.append((video, e.stdout))

    if failed:
        sys.stderr.write("Some failed:")
        sys.stderr.write("\n".join("\t->\t".join(str(a) for a in x) for x in failed))
        sys.exit(1)
