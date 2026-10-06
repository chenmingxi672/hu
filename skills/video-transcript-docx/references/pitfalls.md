# 踩过的坑

这些都是实测撞出来的，不是推测。按"症状 → 原因 → 处理"排。

## 依赖与网络

### `error: can't find Rust compiler`

```
× Failed to build `tokenizers==0.10.3`
error: can't find Rust compiler
```

**原因**：`uv` 在依赖没有版本下界时，可能一路回退到很老的版本。这里退到了 2021 年的
`transformers 4.12.2`，连带 `tokenizers 0.10.3`——那版没有预编译轮子，只能从源码编译，
于是要 Rust。

**处理**：显式写下界 `--with "transformers>=4.40,<5"`。

**别误判**：第一反应容易怪"Python 版本太新"，但换到 Python 3.10 报的是**同一个错**。
看到"要编译、缺编译器"，先怀疑依赖解析结果太老，而不是环境缺东西。

### 缺 torch

```
ModuleNotFoundError: FunASR requires PyTorch before using AutoModel.
```

**原因**：`funasr` 的依赖声明里**根本没有 torch**（PyPI 元数据里只有 `torch_complex`，
没有 `torch`）。它默认你自己装好。

**处理**：`--with torch --with torchaudio`。

### 下载卡死（境外源）

**症状**：日志几分钟不更新，进程还活着，CPU 几乎为 0。

**原因**：`files.pythonhosted.org` 在校园网/无代理环境下极慢。torch 两百多 MB，
实测卡了四分半没动静。

**处理**：`$env:UV_DEFAULT_INDEX = "https://pypi.tuna.tsinghua.edu.cn/simple"`
（PowerShell）。实测同一批 64 个包，境外源卡 4 分钟，清华源 **7 秒**装完。

**判断"真卡"还是"在下东西"**：看日志文件的 `LastWriteTime` 是不是当前时间。
差几秒 = 正常；差几分钟且 CPU 不动 = 真卡。

### ModelScope 反而不用管

三个模型（Paraformer / VAD / 标点）都从 ModelScope 拉，本来就是国内源，速度没问题。
首次约 1 GB，之后缓存在本地。

## 系统策略

### lxml 被应用程序控制策略拦截

```
ImportError: DLL load failed while importing etree: 应用程序控制策略已阻止此文件
```

**原因**：Windows 应用程序控制策略（WDAC / Smart App Control 之类）拦截了 lxml 的原生
DLL。实测单独 `import lxml.etree` 就失败，稳定复现；而 torch / numpy / scipy 的原生库
都正常加载。

**后果**：**任何依赖 lxml 的库都不能用**，首当其冲是 `python-docx`。

**处理**：不要跟系统策略较劲，也不要让用户去关安全策略。docx 本身就是个 ZIP 装几个
XML，用标准库 `zipfile` 直接写，见 `scripts/make_docx.py`。反而更灵活——深色背景、
段落底纹这些 python-docx 本来也表达不了，一样得手写 XML。

## 命令行

### 中文参数（实测**没问题**，但还是要核一眼）

一度怀疑 PowerShell 5.1 把中文参数传给原生程序会乱码，所以绕道写脚本。**实测推翻了**：
`--title "如何利用AI学习任何复杂知识…"` 直接传，docx 里的标题完全正确。

不过终端代码页、PowerShell 版本、调用方式都可能影响这件事，所以**不要靠猜**：
`verify_docx.py` 会把每份文档的标题行打出来，交付前扫一眼就知道有没有变乱码。
真出问题时的退路是把标题写进 `.py` 源码或 UTF-8 文件，而不是走命令行。

## 热词（hotword）

### 标准模型不支持热词

`iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch` **不支持**
`hotword` 参数。要用 **SeACo-Paraformer**
（`iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch`），
多下一个 990 MB 的模型。

### 热词只管它词表里有的词

实测：`markdown`、`红黑树` 修好了；`Obsidian`、`Gemini`、`Cursor`、`Kruskal` 这类
词表里没有的外来专名，**热词完全带不动**。机制上它需要词能切成模型认识的子词单元。

### 热词会被误插

实测把"哎，怎么…"这句里的"怎么"插成了"怎脑图"，因为热词表里有"脑图"。
热词不是免费的，加完要回读一遍，看有没有插到不相干的地方。
