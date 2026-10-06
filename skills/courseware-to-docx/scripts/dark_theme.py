"""Re-skin a .docx as dark-background/light-text (or just fix its CJK font).

    python dark_theme.py in.docx out.docx [--theme dark|light]

Pure standard library -- python-docx is unusable where lxml is blocked.

Why three separate mechanisms, all at once. A .docx has no notion of "page
background colour"; dark mode has to be assembled from parts, and each part is
ignored by some reader:

  * <w:background> on the document paints the whole page -- but Word only
    honours it when <w:displayBackgroundShape/> is also set in settings.xml.
  * <w:shd> on every paragraph is what the viewers that ignore the page
    background actually render. Without it you get light text on white.
  * A light colour in styles.xml docDefaults is what runs without an explicit
    colour inherit. Setting it per-run instead would be fragile and huge.

Order matters. OOXML validates element *sequence*: inside <w:pPr>, <w:shd> has to
sit after the border element and before <w:spacing>/<w:ind>/<w:jc>; inside
<w:rPr>, <w:color> has to sit before <w:sz>. Inserting at a naive offset yields a
file Word opens with "the file cannot be opened because there are problems with
the contents". Hence insert_ordered().
"""
import argparse
import re
import zipfile

# tags that must come after w:shd inside w:pPr
AFTER_SHD = [
    "w:tabs", "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap",
    "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE", "w:autoSpaceDN",
    "w:bidi", "w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind",
    "w:contextualSpacing", "w:mirrorIndents", "w:suppressOverlap", "w:jc",
    "w:textDirection", "w:textAlignment", "w:textboxTightWrap", "w:outlineLvl",
    "w:divId", "w:cnfStyle", "w:rPr", "w:sectPr", "w:pPrChange",
]

THEMES = {
    "dark": {"bg": "1E1E1E", "fg": "ECECEC", "line": "9A9A9A", "page": True},
    "light": {"bg": None, "fg": "1A1A1A", "line": "BFBFBF", "page": False},
}

CJK_FONT = "Microsoft YaHei"


def insert_ordered(inner, element, after_tags):
    """Insert `element` into `inner` as late as the schema allows."""
    pos = len(inner)
    for tag in after_tags:
        m = re.search(r"<%s[ />]" % re.escape(tag), inner)
        if m and m.start() < pos:
            pos = m.start()
    return inner[:pos] + element + inner[pos:]


def add_eastasia_font(xml):
    """Pandoc's reference doc ships no CJK font, so Chinese falls back to
    whatever the reader picks -- often something ugly. Pin it."""
    def fix(m):
        attrs = m.group(1)
        if "w:eastAsia" in attrs:
            return m.group(0)
        return attrs.rstrip() + ' w:eastAsia="%s"/>' % CJK_FONT
    return re.sub(r"<w:rFonts\b([^>]*?)/>", fix, xml)


def theme(text, th):
    shad = '<w:shd w:val="clear" w:color="auto" w:fill="%s"/>' % th["bg"]

    if th["page"]:
        # w:background must be the first child of w:document
        text = re.sub(r"(<w:document\b[^>]*>)",
                      r'\1<w:background w:color="%s"/>' % th["bg"], text, count=1)

    def shade_ppr(m):
        inner = m.group(1)
        if "<w:shd" in inner:
            return m.group(0)
        return "<w:pPr>" + insert_ordered(inner, shad, AFTER_SHD) + "</w:pPr>"

    if th["page"]:
        text = re.sub(r"<w:pPr>(.*?)</w:pPr>", shade_ppr, text, flags=re.S)
        text = re.sub(r"<w:p>(?=<w:r|<w:bookmarkStart|<w:proofErr|<w:hyperlink|</w:p>)",
                      "<w:p><w:pPr>%s</w:pPr>" % shad, text)

    # any explicit run colour -> the theme foreground
    text = re.sub(r"<w:color\b[^>]*/>", '<w:color w:val="%s"/>' % th["fg"], text)
    text = re.sub(r"<w:color\b[^>]*>\s*</w:color>",
                  '<w:color w:val="%s"/>' % th["fg"], text)
    text = add_eastasia_font(text)
    # table rules: black lines vanish on a dark page
    text = re.sub(
        r'(w:(?:top|left|bottom|right|start|end|insideH|insideV|between|bar)\b'
        r'[^>]*?w:color=")[0-9A-Fa-f]{6}(")',
        lambda m: m.group(1) + th["line"] + m.group(2), text)
    return text


def theme_styles(text, th):
    text = re.sub(r"(<w:docDefaults>.*?<w:rPr>)",
                  lambda m: m.group(1) + '<w:color w:val="%s"/>' % th["fg"],
                  text, count=1, flags=re.S)
    text = re.sub(r"<w:color\b[^>]*/>", '<w:color w:val="%s"/>' % th["fg"], text)
    text = add_eastasia_font(text)
    text = re.sub(
        r'(w:(?:top|left|bottom|right|start|end|insideH|insideV|between|bar)\b'
        r'[^>]*?w:color=")[0-9A-Fa-f]{6}(")',
        lambda m: m.group(1) + th["line"] + m.group(2), text)
    return text


def theme_settings(text, th):
    if not th["page"] or "displayBackgroundShape" in text:
        return text
    return re.sub(r"(<w:settings\b[^>]*>)",
                  r"\1<w:displayBackgroundShape/>", text, count=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--theme", choices=["dark", "light"], default="dark")
    args = ap.parse_args()
    th = THEMES[args.theme]

    with zipfile.ZipFile(args.src) as z:
        items = {n: z.read(n) for n in z.namelist()}

    items["word/document.xml"] = theme(
        items["word/document.xml"].decode("utf-8"), th).encode("utf-8")
    if "word/styles.xml" in items:
        items["word/styles.xml"] = theme_styles(
            items["word/styles.xml"].decode("utf-8"), th).encode("utf-8")
    if "word/settings.xml" in items:
        items["word/settings.xml"] = theme_settings(
            items["word/settings.xml"].decode("utf-8"), th).encode("utf-8")

    with zipfile.ZipFile(args.dst, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in items.items():
            z.writestr(name, data)

    doc = items["word/document.xml"].decode("utf-8")
    print("wrote %s  (theme=%s)" % (args.dst, args.theme))
    print("  page background  : %s" % ("yes" if "<w:background" in doc else "none"))
    print("  shaded paragraphs: %d / %d"
          % (len(re.findall(r"<w:shd\b", doc)), len(re.findall(r"<w:p[ >]", doc))))
    print("  native equations : %d" % len(re.findall(r"<m:oMath[ >]", doc)))


if __name__ == "__main__":
    main()
