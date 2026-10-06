# 深色 docx 的技术细节

## 为什么不能只用 python-docx

`python-docx` 表达不了页面背景色，本来就得到 XML 层注入。
更关键的是：**它依赖 `lxml`，而 lxml 的原生 DLL 在部分 Windows 机器上被应用程序控制策略拦截**：

```
ImportError: DLL load failed while importing etree: 应用程序控制策略已阻止此文件
```

稳定复现，单独 `import lxml.etree` 也会失败。所以这条路直接堵死——
本 skill 的脚本**全用标准库**（`zipfile` + `re` + `xml.etree`），不碰 lxml。

## 深色由三块拼成，缺一块某些阅读器就不对

`.docx` 里**没有"页面背景色"这个概念**。深色模式是拼出来的，而且每一块都会被某些阅读器忽略：

1. **`<w:background w:color="…"/>`** —— 整页背景。必须是 `w:document` 的**第一个子元素**。
   而且 **Word 只在你同时在 `settings.xml` 里写了 `<w:displayBackgroundShape/>` 时才画它**。
   漏了这个开关，背景等于没设。
2. **每个段落的 `<w:shd w:fill="…"/>`** —— 那些忽略页面背景的阅读器（手机版 Word 等）
   实际渲染的是这个。不铺底纹就是白字白底，什么都看不见。
3. **`styles.xml` 里 `docDefaults` 的 `<w:color>`** —— 没带显式颜色的 run 靠它继承。
   比逐 run 设色可靠得多；逐 run 设还会漏掉公式里的 run。

## 顺序不能乱（这是最常见的翻车点）

OOXML 校验元素的**先后顺序**，顺序错了 Word 直接报"内容有错误，无法打开"。

- 在 `<w:pPr>` 里，`<w:shd>` 必须在 `<w:pBdr>` **之后**、`<w:spacing>` / `<w:ind>` / `<w:jc>` **之前**
- 在 `<w:rPr>` 里，`<w:color>` 必须在 `<w:sz>` **之前**
- `<w:background>` 必须是 `w:document` 的第一个子元素

脚本里的 `insert_ordered()` 就是干这个的：找出"必须排在它后面"的那些标签，
插在最早出现的那个之前。

## 表格

深色底上黑框线是看不见的，要把 `w:top`/`w:left`/… 这些边框元素的 `w:color` 换成浅灰。
**注意区分**：边框的颜色是**属性**（`<w:top w:color="000000"/>`），
文字颜色是**元素**（`<w:color w:val="000000"/>`），正则别写混。

## 中文字体

pandoc 自带的参考文档没有 CJK 字体，中文会退回到阅读器自选，往往难看。
脚本会把所有 `<w:rFonts>` 补上 `w:eastAsia="Microsoft YaHei"`。

## 验证（交付前必做）

```
python check_docx.py out.docx
```

查七项：XML 合法性、`w:background` 位置、`displayBackgroundShape` 开关、
`w:shd` 顺序、底纹段数与段落数是否**完全相等**、公式对象数、残留深色颜色数。

**结构检查过了不等于 Word 打得开**，再做一次真实检验：

```powershell
$word = New-Object -ComObject Word.Application
$word.DisplayAlerts = 0
$doc = $word.Documents.Open($path, $false, $true)   # 只读打开
"pages = " + $doc.ComputeStatistics(2)
$doc.Close([ref]$false)
```

**读得出页数就说明 Word 认这个文件。**

### Word COM 的两个坑（实测踩过）

1. **不要调 `$word.Quit()`**。`New-Object` 可能**附着到你正在运行的 Word 实例**上，
   一 Quit 就把用户正在编辑的文档关了。只 `Close` 自己那一份。
   （实测时 `before` 为空、没有 Word 在跑，所以可以安全收尾；有 Word 在跑就别碰。）
2. **它可能挂死**。实测 `ExportAsFixedFormat` 导出 PDF 连续挂死两次，
   还把 Cherry 界面卡住了，留下一个无窗口的 Word 进程干耗 CPU。
   → **别为了"锦上添花"的视觉确认去冒这个险**。打开验页数就够了。
   真挂住了：按 `MainWindowTitle` 是否为空找出那个隐藏实例，单独 kill 掉。

## 已知局限（交付时要讲清楚）

- **Word 默认不打印页面背景色**。深色版基本只适合屏幕阅读，要打印得给浅色版。
- **部分阅读器不显示段落底纹** → 白底白字。所以**深色和浅色两版都要出**，
  浅色版不是备选，是必需品。
