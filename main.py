#!/usr/bin/env python3
"""One-Sentence Absurd Invention Pitch.

Writes a single sentence pitching a ridiculous invention that fixes a tiny
everyday annoyance to /output/entry.txt. Python standard library only, no
network access, no external files read at run time: the sentence lives in
this file. Deterministic: the same bytes are written on every run.
"""

import os
import shutil
import stat

SENTENCE = (
    "The Weeping Hinge cures squeaky doors by crying a single tear of "
    "lubricant every time one opens, keeping the house silent and faintly "
    "haunted."
)

OUTPUT_DIR = "/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "entry.txt")


def validate(sentence):
    """Guard: exactly one sentence, 1-220 chars, not only whitespace."""
    if not sentence or not sentence.strip():
        raise ValueError("sentence must not be empty or only whitespace")
    if len(sentence) > 220:
        raise ValueError(
            "sentence is %d characters, over the 220 limit" % len(sentence)
        )
    if sentence != sentence.strip():
        raise ValueError("sentence must not have leading/trailing whitespace")
    # Exactly one sentence: a single terminal period, no other sentence
    # breaks ('.', '!' or '?') anywhere else in the text.
    if not sentence.endswith("."):
        raise ValueError("sentence must end with a single terminal period")
    body = sentence[:-1]
    if any(ch in body for ch in ".!?"):
        raise ValueError("sentence must contain exactly one sentence")
    if "\n" in sentence or "\r" in sentence:
        raise ValueError("sentence must be a single line")


def main():
    validate(SENTENCE)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Clear the CONTENTS of /output only; never remove /output itself.
    for name in os.listdir(OUTPUT_DIR):
        path = os.path.join(OUTPUT_DIR, name)
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(SENTENCE + "\n")
    os.chmod(OUTPUT_FILE, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)


if __name__ == "__main__":
    main()
