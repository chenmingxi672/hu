"""Split one marked-up notes file into the "original" and "supplemented" versions.

    python split_supp.py notes.md --original out_orig.md --supplemented out_supp.md

Write the notes ONCE, with everything you added wrapped in

    <!--SUPP-->
    ...新补的证明、解释、注记...
    <!--/SUPP-->

The original version drops those blocks; the supplemented version keeps
everything. Keeping a single source means the two versions can never drift --
if you later fix a typo in the shared text, both files get the fix, and the
"original" version provably contains nothing you wrote yourself.

Both markers must be on their own lines. Unterminated blocks are reported rather
than silently dropped.
"""
import argparse
import re
import sys

BLOCK = re.compile(r"^[ \t]*<!--SUPP-->[ \t]*\n.*?^[ \t]*<!--/SUPP-->[ \t]*\n?",
                   re.S | re.M)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--original", required=True)
    ap.add_argument("--supplemented", required=True)
    args = ap.parse_args()

    with open(args.src, encoding="utf-8") as f:
        text = f.read()

    opens = text.count("<!--SUPP-->")
    closes = text.count("<!--/SUPP-->")
    if opens != closes:
        print("WARNING: %d opening markers but %d closing markers -- a block is "
              "unterminated and will not be stripped correctly" % (opens, closes))

    orig = BLOCK.sub("", text)
    orig = re.sub(r"\n{4,}", "\n\n\n", orig)          # collapse the gap left behind

    with open(args.supplemented, "w", encoding="utf-8") as f:
        f.write(text)
    with open(args.original, "w", encoding="utf-8") as f:
        f.write(orig)

    print("supplement blocks : %d" % opens)
    print("supplemented      : %s  (%d chars)" % (args.supplemented, len(text)))
    print("original          : %s  (%d chars, %d chars of additions removed)"
          % (args.original, len(orig), len(text) - len(orig)))
    if opens:
        print()
        print("NOTE: the original version should contain ONLY what the courseware "
              "itself says. Skim it once to confirm no addition leaked through.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
