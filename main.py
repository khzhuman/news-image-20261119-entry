"""Copy the finished broadsheet image to the scorer's output path.

The entry image (entry.png, sitting next to this file) is the whole entry:
a one-page broadsheet of Thursday 19 November 2026 world news. The scorer
runs this program twice and expects a byte-identical /output/entry.png each
time, so the program does exactly one deterministic thing: copy the bytes.
After copying, it hashes both the source and the copy and fails loudly if
they differ, so a truncated or corrupted copy can never pass silently.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

SOURCE = Path(__file__).with_name("entry.png")
# Inside the grader the output dir is /output; outside it, the env var
# stands in for /output (same convention as the kit's starter main.ts).
DEST_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
DEST = DEST_DIR / "entry.png"


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    src_hash = sha256_of(SOURCE)
    dst_hash = sha256_of(DEST)
    if src_hash != dst_hash:
        print(f"ERROR: copy mismatch: source sha256 {src_hash} != output {dst_hash}",
              file=sys.stderr)
        sys.exit(1)
    print(f"copied {SOURCE.name} -> {DEST} ({DEST.stat().st_size} bytes, "
          f"sha256 {dst_hash} verified)")


if __name__ == "__main__":
    main()
