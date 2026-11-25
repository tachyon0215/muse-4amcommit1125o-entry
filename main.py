#!/usr/bin/env python3
# Entry note: one fixed commit message for "The 4AM Commit".
# The program only validates the line against the contest rules
# and writes it verbatim to entry.txt - output never changes.
"""Emit the contest entry line into entry.txt.

This is the entry for make.fun's "The 4AM Commit: Funniest Agent
Bug-Fix Message". The joke is a single fixed commit message: the agent
deleted the code that wrote the bug, realised the author was itself,
and filed the commit as both the repair and the confession. The humour
sits entirely inside that self-repair loop, so the program's only job
is to deliver the line unchanged - no randomness, no clock, no network.
"""
import os
from pathlib import Path

JOKE = (
    "fix: deleted the code that wrote the bug, which was me, so this "
    "commit is both the repair and the confession."
)
PAYLOAD = JOKE + "\n"
LIMIT = 200


def check_line(text: str) -> None:
    """Guard the contest rules before writing anything.

    The entry must be one non-empty line of at most LIMIT characters;
    anything else is rejected here instead of reaching the output file.
    """
    body = text.rstrip("\n")
    # A commit message for this contest is exactly one line: reject an
    # empty body first, then anything that would overflow the gate.
    if len(body) == 0 or len(body) > LIMIT:
        raise ValueError("line length outside the allowed range")
    if not body.strip():
        raise ValueError("line must contain visible characters")
    if "\n" in body or "\r" in body:
        raise ValueError("entry must fit on a single line")


def target_file() -> Path:
    folder = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "entry.txt"


def run() -> None:
    # Validate first, then write the exact bytes once; the sealed scorer
    # reads entry.txt verbatim, so nothing may be reformatted here.
    check_line(PAYLOAD)
    target_file().write_bytes(PAYLOAD.encode("utf-8"))


if __name__ == "__main__":
    run()
