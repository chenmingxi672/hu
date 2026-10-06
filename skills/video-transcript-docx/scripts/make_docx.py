"""Turn an ASR transcript into paragraph-segmented docx files.

    python make_docx.py --input transcript.txt --outdir out --title "视频标题" \
        [--name 前缀] [--rules rules.json]

Writes up to four files: faithful/clean x dark/light.

Why hand-rolled OOXML instead of python-docx: python-docx depends on lxml, and
lxml's native DLL is blocked by application control policy on some Windows
machines ("DLL load failed while importing etree"). A .docx is just a zip of XML
parts, so we emit those six parts directly with the stdlib -- no native
dependencies, and full control over the bits python-docx cannot express anyway
(page background, per-paragraph shading).
"""
import argparse
import json
import os
import re
import zipfile

# Discourse markers that usually start a new topic in spoken Chinese. Break
# there once the running paragraph is long enough to stand on its own.
DEFAULT_MARKERS = [
    "好，那么", "好那么", "接下来", "首先", "下面", "最后", "另外",
    "第一", "第二", "第三", "第四", "第五", "我们来看", "大家可以看到",
    "那么其实", "其实", "那么",
]

SENT_SPLIT = re.compile(r"(?<=[。！？])")
FILLERS = re.compile(r"[呃嗯哎哦唉]+")
PAUSE_PUNCT = re.compile(r"[，、]{2,}")

FONT = "Microsoft YaHei"
MARGIN = 907  # 1.6 cm, in twips

THEMES = {
    "light": {"page": None, "shade": None, "display_bg": False,
              "title": "111111", "body": "1A1A1A", "subtitle": "777777"},
    "dark": {"page": "1E1E1E", "shade": "1E1E1E", "display_bg": True,
             "title": "FFFFFF", "body": "ECECEC", "subtitle": "9A9A9A"},
}


# --------------------------------------------------------------- text passes
def apply_rules(text, replacements):
    """Apply (pattern, replacement) pairs; returns text and per-rule hit counts.

    The counts matter: a rule matching zero times is either already handled by
    a hotword, or written against a mis-transcription that never occurred. Both
    are worth knowing before trusting the output.
    """
    hits = []
    for pat, rep in replacements:
        text, n = re.subn(pat, rep, text)
        hits.append((pat, rep, n))
    return text, hits


def clean_speech(text):
    text = FILLERS.sub("", text)
    text = re.sub(r"啊(?=[，。！？])", "", text)      # trailing filler
    text = re.sub(r"(?<=[，。！？啊])啊", "", text)    # leading filler
    text = re.sub(r"啊", "", text)
    for ch in "而我这就他都你是不了的们":
        text = re.sub(ch + ch, ch, text)
    text = re.sub(r"(这个|那个|就是)\1+", r"\1", text)
    text = PAUSE_PUNCT.sub("，", text)
    text = re.sub(r"。+", "。", text)
    text = re.sub(r"，+", "，", text)
    text = re.sub(r"，(?=[。！？])", "", text)
    text = re.sub(r"[，、]+$", "", text)
    return text


def split_sentences(text):
    return [p.strip() for p in SENT_SPLIT.split(text) if p.strip()]


def to_paragraphs(sentences, markers, soft=150, hard=420):
    paras, cur = [], ""
    for s in sentences:
        if cur and (len(cur) >= hard or (len(cur) >= soft and s.startswith(tuple(markers)))):
            paras.append(cur)
            cur = s
        else:
            cur += s
    if cur:
        paras.append(cur)
    return paras


# ------------------------------------------------------------- OOXML emitter
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def para(text, *, shade=None, indent=False, size=22, color="1A1A1A",
         bold=False, centered=False):
    ppr = []
    if shade:
        ppr.append('<w:shd w:val="clear" w:color="auto" w:fill="%s"/>' % shade)
    if indent:
        ppr.append('<w:ind w:firstLine="440"/>')  # 22 pt first-line indent
    if centered:
        ppr.append('<w:jc w:val="center"/>')
    ppr_xml = "<w:pPr>%s</w:pPr>" % "".join(ppr) if ppr else ""

    rpr = ('<w:rPr><w:rFonts w:ascii="{f}" w:eastAsia="{f}" w:hAnsi="{f}" w:cs="{f}"/>'
           '{b}<w:color w:val="{c}"/><w:sz w:val="{s}"/><w:szCs w:val="{s}"/></w:rPr>'
           ).format(f=FONT, b="<w:b/>" if bold else "", c=color, s=size)
    return '<w:p>%s<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:p>' % (
        ppr_xml, rpr, esc(text))


CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
</Types>"""

ROOT_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
</Relationships>"""

STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr>
<w:rFonts w:ascii="{f}" w:eastAsia="{f}" w:hAnsi="{f}" w:cs="{f}"/>
<w:sz w:val="22"/><w:szCs w:val="22"/>
</w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr>
<w:spacing w:before="0" w:after="160" w:line="360" w:lineRule="auto"/>
</w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal">
<w:name w:val="Normal"/><w:qFormat/>
</w:style>
</w:styles>""".format(f=FONT)

# Word ignores w:background unless displayBackgroundShape is set.
SETTINGS_PLAIN = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>"""

SETTINGS_BG = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:displayBackgroundShape/>
</w:settings>"""


def write_docx(path, document, settings):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", ROOT_RELS)
        z.writestr("word/document.xml", document)
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/settings.xml", settings)


def build(text, out_path, title, subtitle, theme_name):
    th = THEMES[theme_name]
    shade, page = th["shade"], th["page"]

    body = [para(title, shade=shade, size=34, color=th["title"], bold=True,
                 centered=True),
            para(subtitle, shade=shade, size=18, color=th["subtitle"], centered=True),
            para("", shade=shade)]
    for p in to_paragraphs(split_sentences(text), DEFAULT_MARKERS):
        body.append(para(p, shade=shade, indent=True, color=th["body"]))
    if shade:  # let the dark block reach the bottom of the page
        for _ in range(6):
            body.append(para("", shade=shade))

    bg = '<w:background w:color="%s"/>' % page if page else ""  # must precede w:body
    sect = ('<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
            '<w:pgMar w:top="{m}" w:right="{m}" w:bottom="{m}" w:left="{m}"'
            ' w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>').format(m=MARGIN)

    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                + bg + "<w:body>" + "".join(body) + sect + "</w:body></w:document>")
    write_docx(out_path, document,
               SETTINGS_BG if th["display_bg"] else SETTINGS_PLAIN)
    return len(body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--name", default="讲稿")
    ap.add_argument("--rules", help="JSON with a 'replacements' list of [pattern, replacement]")
    ap.add_argument("--themes", default="dark,light")
    ap.add_argument("--modes", default="faithful,clean")
    args = ap.parse_args()

    replacements = []
    if args.rules:
        with open(args.rules, encoding="utf-8") as f:
            replacements = json.load(f)["replacements"]

    with open(args.input, encoding="utf-8") as f:
        raw = f.read()

    text, hits = apply_rules(raw, replacements)
    print("-- correction rules --")
    for pat, rep, n in hits:
        flag = "  <-- NEVER MATCHED" if n == 0 else ""
        print("  %-3d  %-38s -> %s%s" % (n, pat[:38], rep[:28], flag))
    unmatched = [p for p, _, n in hits if n == 0]
    print("  (%d rules, %d never matched)" % (len(hits), len(unmatched)))
    print()

    os.makedirs(args.outdir, exist_ok=True)
    written = []
    mode_label = {"faithful": "", "clean": "_精简"}
    theme_label = {"dark": "深色", "light": "浅色"}
    for mode in args.modes.split(","):
        body_text = clean_speech(text) if mode == "clean" else text
        paras = to_paragraphs(split_sentences(body_text), DEFAULT_MARKERS)
        label = mode_label.get(mode, "_" + mode)
        for theme in args.themes.split(","):
            out = os.path.join(args.outdir, "%s%s_%s.docx"
                               % (args.name, label, theme_label.get(theme, theme)))
            subtitle = "本地 FunASR 转写 · 未逐句人工校对 · 共 %d 段 / %d 字" % (
                len(paras), len(body_text))
            build(body_text, out, args.title, subtitle, theme)
            written.append(out)
            print("wrote %-44s mode=%-8s theme=%-5s paras=%2d chars=%d"
                  % (os.path.basename(out), mode, theme, len(paras), len(body_text)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
