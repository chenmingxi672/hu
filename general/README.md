# 模型无关 · 在 DeepSeek 下实测可用

这一组不是"DeepSeek 生态专用"，而是**不依赖任何模型专有能力、换成 DeepSeek 一样跑得通**
的通用 Agent Skill。

## 判据怎么定的

"DeepSeek 能不能用"这件事很容易变成空谈，所以这里只用**可验证**的标准：

1. **不依赖模型专有能力** —— skill 只靠文件读写、跑命令、读写网页这类通用工具。
   如果一条 skill 需要某个模型独有的能力（专属工具调用格式、Artifacts 之类的宿主特性），
   就不该收进来。
2. **实测跑过** —— 下面这些**全部是在跑 DeepSeek 的会话里实际执行过的**。
   本仓库就是在这样一次会话里建起来的：**这个会话本身就跑在 DeepSeek 模型上**
   （`deepseek-flash[1m]`），写作过程中用到了文件工具、命令执行、联网检索。
3. 反过来说，**没有实测过的通用 skill 不收**——那属于"看着应该能用"，不是"能用"。

## 一、本仓库真收录的（见 [`../skills/`](../skills/)）

这两条是**从零写出来的、跑过完整流水线**的 skill，内容已收录进本仓库，clone 即可用。

| skill | 版本 | 做什么 |
|---|---|---|
| [`courseware-to-docx`](../skills/courseware-to-docx/) | v1.3.0 | 课件 PDF → 定稿 docx：探文字层、渲染读图、**补全被"同理可证""由另页例可知"略去的证明**、拆成**原文版 / 补充证明版**两份、深浅主题、结构自检。公式是 Word 原生对象 |
| [`video-transcript-docx`](../skills/video-transcript-docx/) | v1.1.0 | 视频/音频 → 中文文字稿 docx：探字幕、yt-dlp 取音频、免安装 ffmpeg 转 16k wav、本地 FunASR 转写、专有名词定向纠错、按话题分段、深/浅双主题 |

这两条都自带**「把这次的教训写回本技能」机制**——每次跑完必须把当趟的坑落回对应步骤并递增
版本号。这和官方 `dsh-archive-agent-notes` / `agent-experience` 是同一类思路。

## 二、本机装了、也跑过的通用 skill

| skill | 版本 | 做什么 | 来源 |
|---|---|---|---|
| `pdf-to-notes` | v1.2.0 | 读"读不出文字"的 PDF（扫描件、字体缺 Unicode 映射的乱码课件）并整理成笔记 | 同上一组，同一路子写的，**尚未收录** |
| `daily-book-story` | v1.0.0 | 把一本书按天写成连载（故事化正文 + 独立概念册），交付纯文本 | 同上，**尚未收录** |
| `office-transform` | v1.0.0 | 从 xlsx/docx/pdf/pptx 的**结构性选区**派生出新文件，**绝不动原件**：xlsx 区域转 csv/md/xlsx、docx 段落抽取与替换、pdf 拆页、pptx 幻灯片/形状/表格单元格抽取与编辑 | 客户端自带 |
| `skill-creator` | v1.0.0 | 从零创建 skill、改造已有 skill、跑评测与优化 | 客户端自带 |
| `find-skills` | v1.0.0 | 搜 skill 市场、发现可安装的 skill | 客户端自带 |
| `cherry-browser` | v1.0.0 | 操作用户可见的浏览器（导航、截图、表单、点击、认证站点） | 客户端自带 |
| `cherry-tool-guide` | v1.6.0 | 客户端自带工具与内置 shell 的路由说明（什么时候用 `bun`/`uv`/`rg` 等） | 客户端自带 |
| `code-mate-deepseek-harness` | — | **无头运行 DeepSeek Harness**，把仓库任务委派给它 | 客户端自带，**本身就是给 DeepSeek 用的** |

> **"来源"这一列怎么判断的**：客户端自带的 skill 会带一个 `.version` 文件，自己写的不带。
> 这是**一个经验判据、不是权威依据**——所以第 1、2 行标了"尚未收录"，我没有替它们下结论，
> 想收进 `../skills/` 说一声即可。

## 三、想找更多通用 skill

通用 skill 的市场很大（skills.sh 上装机量上百万的一大把），本清单**不做通用推荐**——
那会变成另一个项目。要用的时候：

- 在客户端里说"帮我找个能做 X 的 skill"，走 `find-skills`
- 或者直接搜市场

真正**只有 DeepSeek 生态才有的**东西，才是这份清单的价值所在，看
[`../official/`](../official/) 和 [`../community/`](../community/)。
