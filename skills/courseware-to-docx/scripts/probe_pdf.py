"""Decide whether a PDF's text layer can be trusted, before reading 30 pages of images.

    uv run --with pymupdf python probe_pdf.py <pdf> [--pages 1-5]

Reports per page: characters of extractable text, how many of them are CJK, and
how many images are on the page. Then it gives a verdict.

The failure this is built to catch: courseware exported with a *subsetted font
whose ToUnicode map is missing*. The text layer is not empty -- it is full of
plausible-looking Latin garbage ("ThHCTab", "C= EPJ", "Sit ba"). A naive check
for "has text?" passes and you end up reading nonsense. So the test is not
"is there text" but "is the text recognisably the language the document is in".

Exit codes: 0 = text layer usable, 2 = must render pages to images.
"""
import argparse
import re
import sys

CJK = re.compile(r"[㐀-䶿一-鿿豈-﫿]")


def parse_pages(spec, count):
    if not spec:
        return list(range(count))
    a, _, b = spec.partition("-")
    return [i - 1 for i in range(int(a), int(b or a) + 1) if 1 <= i <= count]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--pages", help="e.g. 1-5; default is the whole file")
    ap.add_argument("--probe-only", action="store_true",
                    help="accepted for symmetry; this script only ever probes")
    args = ap.parse_args()

    import pymupdf

    doc = pymupdf.open(args.pdf)
    pages = parse_pages(args.pages, doc.page_count)
    print("%s -- %d pages, probing %d" % (args.pdf, doc.page_count, len(pages)))
    print()
    print("  page   chars   cjk   latin   images")
    print("  " + "-" * 40)

    total_chars = total_cjk = total_imgs = 0
    for i in pages:
        page = doc[i]
        text = page.get_text()
        cjk = len(CJK.findall(text))
        latin = len(re.findall(r"[A-Za-z]", text))
        imgs = len(page.get_images(full=True))
        total_chars += len(text)
        total_cjk += cjk
        total_imgs += imgs
        print("  %4d  %6d  %5d  %6d  %6d" % (i + 1, len(text), cjk, latin, imgs))
    doc.close()

    print()
    print("  totals: %d chars, %d cjk, %d images over %d pages"
          % (total_chars, total_cjk, total_imgs, len(pages)))
    print()

    per_page = total_chars / max(len(pages), 1)
    cjk_ratio = total_cjk / max(total_chars, 1)

    if per_page < 50 and total_imgs >= len(pages):
        print("VERDICT: scanned/image-only -> render the pages and read them as images")
        return 2
    if total_cjk >= 20 and cjk_ratio > 0.15:
        print("VERDICT: text layer looks usable (%.0f%% CJK) -> try extracting text first"
              % (cjk_ratio * 100))
        return 0
    if per_page >= 50:
        print("VERDICT: text layer is NOT trustworthy -- %d chars/page but only %.1f%% CJK."
              % (per_page, cjk_ratio * 100))
        print("         Classic symptom of a subsetted font with no Unicode map:")
        print("         the text is not empty, it is Latin garbage. Render and read images.")
        return 2
    print("VERDICT: too little text to judge -- render the pages and look")
    return 2


if __name__ == "__main__":
    sys.exit(main())
