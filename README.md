# DeepSeek 能用的 Agent Skills

一份整理过的 **Agent Skill 索引**：只收「在 DeepSeek 上真能用」的 skill——不管是跑在
DeepSeek Harness（DSH）里，还是跑在 Cherry Studio / Claude Code 这类客户端里、把模型
换成 DeepSeek 也一样能用。

> **为什么需要这份清单。** 在 skills.sh 这类市场里搜 "deepseek" 会返回 100+ 条，但**绝大多数
> 是噪音**——只是因为描述里提了一句 DeepSeek 就被匹配上了（比如搜索结果的头部全是
> mattpocock 的通用 skill、syncfusion 的 MAUI 组件）。真正属于 DeepSeek 生态的，需要
> 按发布者和用途筛出来。这份清单做的就是这件事。

## 收录标准

一条 skill 要进来，**必须**满足下面之一，并写清是按哪条收的：

| 判据 | 含义 | 在哪 |
|---|---|---|
| **A · DeepSeek 生态专用** | skill 本身就是为 DeepSeek 或其官方 Agent 框架（DSH / Cordis）写的 | [`official/`](official/) [`community/`](community/) |
| **B · 模型无关且实测可跑** | 不依赖任何模型专有能力（如只认某个模型的工具调用、artifacts），在 DeepSeek 下实测跑通 | [`general/`](general/) |

**明确不收：**

- 只因为描述里出现过 "DeepSeek" 就被搜出来的（判据 A、B 都不满足）
- 依赖模型专有能力、换成 DeepSeek 就废掉的
- 需要付费闭源服务才能跑的——除非在条目里明确标出来

## 目录

```
official/    DeepSeek 官方发布的 skill（deepseek-ai/deepseek-harness），23 条，按用途分类
community/   社区围绕 DeepSeek / DSH 生态做的 skill，按用途分类
general/     模型无关、在 DeepSeek 下实测可用的 skill（含本仓库真收录的 2 个）
skills/      真收录的 skill 本体（clone 下来就能装）
```

## 怎么用

**从市场装**：每条都带一行 `install_source`。在支持 skill 的客户端里直接说"安装这个
skill"并把那串给它（例如 Cherry Studio 里用 `mcp__skills__install_skill`），或者手工把
skill 目录放到 `%APPDATA%\CherryStudio\Data\Skills\`。

**用本仓库真收录的**：把 `skills/<名字>/` 整个目录复制到你的 skills 目录即可。

**关于 DSH（DeepSeek Harness）**：它是 DeepSeek 官方的 Agent 框架，`official/` 和
`community/` 里大量条目是围绕它的。如果你只是想在自己的客户端里换个模型用 DeepSeek，
看 `general/` 就够；真正在用 DSH 的话，`official/` 是必看的。

## 关于第三方内容——本仓库**不搬**第三方代码

- `official/`、`community/`、`general/` **只放索引**（名称 + 来源 + 安装串 + 一句话说明），
  **不镜像代码**。版权归各自作者，而且这批 skill 更新很快，镜像下来很快就过期。
- `skills/` 下**真收录**的内容，逐条标注了作者与许可。
- 想装哪一条，装的是**原作者的最新版**，不是本仓库的副本。

## 核实程度

索引里的条目分两档，我在每条后面标了：

- **`描述可得`** —— 拿到了原作者写的描述，说明是按描述归纳的
- **`仅名称`** —— 市场上只给了名字、没有描述。这类**未经内容核实**，只按名字归类，
  用之前建议先看一眼原 skill。

**这份清单不是"推荐"，是"索引"**——收录不等于背书。装之前请自行看一眼对方的 SKILL.md。

## 贡献

见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

## 许可

本仓库自己写的索引文本（README 与各目录说明）采用 CC BY 4.0。
`skills/` 下各 skill 的许可见其子目录。
