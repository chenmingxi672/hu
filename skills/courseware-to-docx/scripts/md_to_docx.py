"""Markdown -> .docx with native Word equations, via pandoc.

    uv run --no-project --python 3.12 --with pypandoc-binary python md_to_docx.py in.md out.docx

Why pandoc: python-docx is the obvious choice for writing docx, but it depends on
lxml, and lxml's native DLL is blocked by application control policy on some
Windows machines ("DLL load failed while importing etree"). pandoc ships as a
self-contained binary and converts $...$ / $$...$$ LaTeX into real OMML equation
objects -- double-clickable and editable in Word, not plain text.

The numbers that matter after converting: the oMath count. If it is 0, the maths
came through as literal text and something is wrong with the delimiters.
"""
import re
import sys
import zipfile

import pypandoc


def main():
    src, dst = sys.argv[1], sys.argv[2]
    print("pandoc " + pypandoc.get_pandoc_version())

    pypandoc.convert_file(
        src, "docx", outputfile=dst,
        extra_args=["--standalone",
                    "--from=markdown+pipe_tables+tex_math_dollars"],
    )

    with zipfile.ZipFile(dst) as z:
        doc = z.read("word/document.xml").decode("utf-8")
    n_math = len(re.findall(r"<m:oMath[ >]", doc))
    n_para = len(re.findall(r"<w:p[ >]", doc))
    print("wrote %s" % dst)
    print("  paragraphs     : %d" % n_para)
    print("  native equations: %d  %s"
          % (n_math, "" if n_math else "<-- ZERO! check the $ delimiters"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
