"""Structural checks on a generated .docx -- the things Word silently rejects.

    python check_docx.py file.docx

Run this before handing any generated docx to the user. A docx that Word refuses
to open is worse than no file at all, and hand-written OOXML fails in ways that
look fine in a text editor: an element one position out of order, a background
without its display flag, or light text that never got its colour applied.

Exit code 0 = sane, 1 = something is wrong.
"""
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

AFTER_SHD = ["w:tabs", "w:spacing", "w:ind", "w:jc", "w:rPr", "w:sectPr",
             "w:outlineLvl", "w:contextualSpacing", "w:wordWrap"]
BEFORE_SHD = ["w:pStyle", "w:numPr", "w:pBdr", "w:keepNext", "w:keepLines",
              "w:pageBreakBefore", "w:widowControl"]

DARK = re.compile(r'<w:color w:val="(0[0-9A-Fa-f]{5}|1[0-9A-Fa-f]{5}|'
                  r'2[0-9A-Fa-f]{5}|3[0-9A-Fa-f]{5})"')


def main():
    path = sys.argv[1]
    bad = 0
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        for name in names:
            if name.endswith((".xml", ".rels")):
                try:
                    ET.fromstring(z.read(name))
                except ET.ParseError as e:
                    print("  MALFORMED %s: %s" % (name, e))
                    bad += 1
        print("1. XML well-formed         : %s" % ("OK" if not bad else "FAILED"))

        doc = z.read("word/document.xml").decode("utf-8")
        settings = (z.read("word/settings.xml").decode("utf-8")
                    if "word/settings.xml" in names else "")

    m = re.search(r"<w:document\b[^>]*>(\s*<[a-zA-Z:]+)", doc)
    first = m.group(1).strip() if m else "(none)"
    has_bg = "<w:background" in doc
    if has_bg and "background" not in first:
        print("2. w:background placement   : FAILED (not the first child)")
        bad += 1
    else:
        print("2. w:background placement   : %s" % ("OK" if has_bg else "n/a (light)"))

    if has_bg and "displayBackgroundShape" not in settings:
        print("3. displayBackgroundShape   : FAILED (Word will not paint the page)")
        bad += 1
    else:
        print("3. displayBackgroundShape   : %s" % ("OK" if has_bg else "n/a (light)"))

    viol = 0
    for m in re.finditer(r"<w:pPr>(.*?)</w:pPr>", doc, re.S):
        inner = m.group(1)
        i = inner.find("<w:shd")
        if i < 0:
            continue
        viol += sum(1 for t in AFTER_SHD if 0 <= inner.find("<%s" % t) < i)
        viol += sum(1 for t in BEFORE_SHD if inner.find("<%s" % t) > i)
    print("4. w:shd ordering in w:pPr  : %s" % ("OK" if not viol else "%d VIOLATIONS" % viol))
    bad += viol

    para = len(re.findall(r"<w:p[ >]", doc))
    shaded = len(re.findall(r"<w:shd\b", doc))
    if has_bg and shaded != para:
        print("5. shaded / total paragraphs: %d / %d  MISMATCH" % (shaded, para))
        bad += 1
    else:
        print("5. shaded / total paragraphs: %d / %d  OK" % (shaded, para))

    print("6. native equations (oMath) : %d" % len(re.findall(r"<m:oMath[ >]", doc)))

    dark = DARK.findall(doc)
    if has_bg and dark:
        print("7. leftover dark run colours: %d  FAILED %s"
              % (len(dark), sorted(set(dark))))
        bad += 1
    else:
        print("7. leftover dark run colours: %d  OK" % len(dark))

    print()
    print("VERDICT: " + ("all structural checks passed" if not bad
                         else "%d problem(s) -- do NOT deliver this file" % bad))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
