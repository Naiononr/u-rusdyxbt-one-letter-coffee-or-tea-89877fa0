#!/usr/bin/env python3
"""One Letter: Coffee or Tea -- entry for make.fun.

Writes exactly one letter, "A" (coffee), to /output/entry.txt.
Per the competition rules: A for coffee, B for tea, one letter and
nothing else -- no word, no explanation, no punctuation.

Output contract, exact: the file holds a single byte, 0x41 ("A"),
UTF-8 text of 1 to 1 characters, no newline, no trailing whitespace.
Nothing is printed to stdout. A is the chosen letter: coffee is the
bolder, more vivid answer -- dark, strong, energising -- the fuller,
more alive stance in the coffee-against-tea argument, and the letter
that stands first.

Pure stdlib, deterministic, no network, no reads outside this file.
"""

import os
import tempfile

LETTER = "A"  # A = coffee. Coffee is the bolder, more vivid answer:
# dark, strong, energising -- the fuller, more alive stance in the
# coffee-against-tea argument, and the letter that stands first.
OUTPUT_PATH = "/output/entry.txt"


def main() -> None:
    out_dir = os.path.dirname(OUTPUT_PATH)
    os.makedirs(out_dir, exist_ok=True)
    data = LETTER.encode("utf-8")  # exactly 1 byte, no newline
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            # Durability: force the byte to disk before the replace,
            # so the published file can never be a torn/empty write.
            os.fsync(f.fileno())
        # mkstemp creates mode 0600; the grader reads the file as
        # another user, so make it world-readable BEFORE the replace.
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, OUTPUT_PATH)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
