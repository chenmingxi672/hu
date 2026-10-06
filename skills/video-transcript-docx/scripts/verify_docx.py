"""Check generated docx files before handing them to the user.

    python verify_docx.py <file-or-directory> [--stale AR,IR,OBC] [--expect Obsidian,AI]

Hand-written OOXML is easy to get subtly wrong, and a docx that Word refuses to
open is worse than no file at all -- so always run this before delivering. It
verifies the zip part list, parses every XML part, and optionally counts
leftover mis-transcriptions and their corrected forms.

Exit code 0 = all files sane; 1 = something is wrong.
"""
import argparse
import glob
import os
import sys
import xml.etree.ElementTree as ET
import zipfile

REQUIRED = [
    "[Content_Types].xml",
    "_rels/.rels",
    "word/document.xml",
    "word/_rels/document.xml.rels",
    "word/styles.xml",
    "word/settings.xml",
]


def check(path, stale, expect):
    problems = []
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        for part in REQUIRED:
            if part not in names:
                problems.append("missing part: " + part)
        for name in names:
            if name.endswith((".xml", ".rels")):
                try:
                    ET.fromstring(z.read(name))
                except ET.ParseError as e:
                    problems.append("malformed XML in %s: %s" % (name, e))
        doc = z.read("word/document.xml").decode("utf-8")
        settings = z.read("word/settings.xml").decode("utf-8")

    # Surface the title line: Chinese passed as a command-line argument can come
    # back mangled, and a mojibake title is easy to miss until the user opens it.
    title = ""
    try:
        root = ET.fromstring(doc)
        ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        for t in root.iter(ns + "t"):
            if t.text and t.text.strip():
                title = t.text.strip()
                break
    except ET.ParseError:
        title = "(unreadable)"

    if 'w:background' in doc and "displayBackgroundShape" not in settings:
        problems.append("has w:background but settings.xml lacks displayBackgroundShape "
                        "-- Word will not paint the page background")

    stale_hits = {t: doc.count(t) for t in stale if doc.count(t)}
    expect_hits = {t: doc.count(t) for t in expect if doc.count(t)}
    return problems, stale_hits, expect_hits, title


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="a .docx file or a directory of them")
    ap.add_argument("--stale", default="",
                    help="comma separated leftovers that should NOT appear")
    ap.add_argument("--expect", default="",
                    help="comma separated corrected forms that SHOULD appear")
    args = ap.parse_args()

    if os.path.isdir(args.target):
        files = sorted(glob.glob(os.path.join(args.target, "*.docx")))
    else:
        files = [args.target]
    if not files:
        print("no docx files found")
        return 1

    stale = [s for s in args.stale.split(",") if s]
    expect = [e for e in args.expect.split(",") if e]
    bad = 0

    for f in files:
        problems, stale_hits, expect_hits, title = check(f, stale, expect)
        status = "OK" if not problems else "PROBLEM"
        print("%-44s %-8s %8d bytes" % (os.path.basename(f), status, os.path.getsize(f)))
        print("      title: " + title[:60])
        for p in problems:
            print("    ! " + p)
            bad += 1
        if stale_hits:
            print("    ! stale terms present: " + ", ".join(
                "%s=%d" % kv for kv in sorted(stale_hits.items())))
            bad += 1
        if expect and not expect_hits:
            print("    ! none of the expected corrected terms appear -- did the "
                  "correction rules actually fire?")
            bad += 1
        elif expect_hits:
            print("      corrected terms: " + ", ".join(
                "%s=%d" % kv for kv in sorted(expect_hits.items())))

    print()
    print("VERDICT: " + ("all files sane" if not bad else "%d problem(s)" % bad))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
