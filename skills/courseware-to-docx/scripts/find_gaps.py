"""Scan a markdown notes file for places where a proof was skipped or hand-waved.

    python find_gaps.py notes.md

Lecturers and textbook editors routinely replace a proof with a one-line gesture
-- "the rest is symmetric", "by the example on p.XX", "obviously". Those are
exactly the steps a reader cannot reconstruct later, so they are worth finding
and filling in. This script does not judge; it lists candidates with context so
you can go read each one and decide.

Reading the hits properly matters more than the regex: some are legitimate
("we repeat the argument above" is fine when the construction really is
identical), and some hide a whole missing proof. Open the file and look.
"""
import re
import sys

# Ordered roughly from "clearly a skip" to "might be fine".
PATTERNS = [
    (r"另页", "引用了别页的例子 —— 那个例子多半没写出来"),
    (r"同理可证|同理|同样可证|同样可|仿照|类似地|类推", "对称/重复论证 —— 要确认真的对称"),
    (r"读者自[证行]|留作练习|不赘|从略|略去", "明确省略"),
    (r"由.{0,8}例可知|见.{0,6}例|参考.{0,6}例", "引用他处结论"),
    (r"显然|易见|容易看出|不难", "断言未证 —— 可能是真显然，也可能是跳了一大步"),
    (r"前面已[证经]|之前已|如上|同上", "回指前文 —— 确认前文真的证过"),
]


def main():
    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()

    total = 0
    for pat, why in PATTERNS:
        hits = [(i + 1, ln) for i, ln in enumerate(lines) if re.search(pat, ln)]
        if not hits:
            continue
        print("=" * 70)
        print("模式 %-28s  %s" % ("/" + pat + "/", why))
        print("命中 %d 处" % len(hits))
        for n, ln in hits:
            print("  L%-4d %s" % (n, ln.strip()[:110]))
        total += len(hits)
        print()

    print("=" * 70)
    print("共 %d 处候选。逐条回原文看，判断哪些是真的缺口。" % total)
    print("判断标准：读者能不能只靠这份稿子把这一步补出来？")
    print("不能 → 补。能（真的只是重复同一个构造）→ 留原话即可。")
    print()

    # The pass above only finds *phrases* that gesture at a proof. An item that
    # simply states its conclusions -- or worse, promises "证明：" and then gives
    # one line -- is invisible to it, because there is no telltale phrase to
    # match. Walk the headings instead and look at what follows, two ways:
    # no proof at all, or a proof that stops almost immediately.
    print("=" * 70)
    print("完整性检查：以下条目的证明缺失或只有一两句")
    head = re.compile(r"^\s*(?:\*\*|#{1,6}\s*)\s*"
                      r"((?:例|定理|引理|性质|推论|命题)[^*#\n]{0,40})")
    # headings of any kind end a block; stopping only at same-kind headings
    # would swallow the next section's proof and hide the gap
    boundary = re.compile(r"^\s*(?:#{1,6}\s|\*\*|>)")
    skip = re.compile(r"公理|定义")          # axioms and definitions are not proved

    marks = [(i, head.match(ln).group(1).strip())
             for i, ln in enumerate(lines) if head.match(ln)]
    missing = 0
    for idx, (i, title) in enumerate(marks):
        end = len(lines)
        for j in range(i + 1, len(lines)):
            if boundary.match(lines[j]):
                end = j
                break
        if skip.search(title):
            continue
        body = "\n".join(lines[i:end])
        at = body.rfind("证明")
        if at < 0:
            reason = "没有证明"
        else:
            tail = re.sub(r"\s", "", body[at + 2:])
            if len(tail) < 80:
                reason = "写了「证明：」但后面只有 %d 字" % len(tail)
            else:
                continue
        print("  L%-4d %-34s %s" % (i + 1, title[:34], reason))
        missing += 1
    if not missing:
        print("  （无）")
    print()
    print("这些是完全没有证明、或证明被一句话带过的条目 —— 比「同理可证」更严重，必须补。")


if __name__ == "__main__":
    main()
