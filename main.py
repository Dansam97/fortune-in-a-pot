#!/usr/bin/env python3
"""Fortune in a Pot — writes one kind, funny fortune for a houseplant.

The entry program for the make.fun bounty
u-golden-heron-44-fortune-in-a-pot-ded981e9: a single line of at most
120 characters, telling a houseplant's fortune, written to
<output dir>/entry.txt where the output dir comes from
MAKEFUN_OUTPUT_DIR (default /output).
"""

import os
import sys

FORTUNE = (
    "Your next leaf will unfurl fashionably late, dressed in green, "
    "and steal the whole windowsill."
)


MAX_CHARS = 120


def validated_text() -> str:
    """Return the fortune after checking it against the gate rules.

    The gate accepts UTF-8 text of 1 to 120 characters that is not only
    white space; the judge wants one line that reads cleanly aloud, so a
    stray newline or padding inside the text is a defect too.
    """
    text = FORTUNE
    text.encode("utf-8")  # raises if the text is not UTF-8 encodable
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"fortune must be 1-{MAX_CHARS} characters, got {len(text)}")
    if not text.strip():
        raise ValueError("fortune must not be only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("fortune must be a single line")
    if text != text.strip():
        raise ValueError("fortune must not carry leading or trailing padding")
    return text


def main() -> int:
    text = validated_text()
    payload = (text + "\n").encode("utf-8")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as fh:
        fh.write(payload)
    with open(path, "rb") as fh:  # read back: the bytes on disk must match
        if fh.read() != payload:
            raise IOError("entry.txt read-back does not match the fortune bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
