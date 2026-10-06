# 官方出品 · `deepseek-ai/deepseek-harness`

DeepSeek 官方账号 **`deepseek-ai`** 在 skills.sh 上发布的整套 skill，仓库名
`deepseek-ai/deepseek-harness`。这是本清单里**最该优先看**的一批：官方维护、跟着 DSH
一起演进、命名统一（`dsh-` 前缀 = DeepSeek Harness）。

下表的数字是 skills.sh 上的装机量，可以当作一个粗糙的使用度参考。

## 一、代码质量与提交前检查

| skill | 装机 | 一句话 |
|---|---|---|
| `dsh-code-review` | 97 | 代码审查工作流 |
| `dsh-find-simplifications` | 90 | 找可简化的地方（能删的复杂度） |
| `dsh-pre-push-checks` | 72 | push 前跑一遍的检查清单 |
| `dsh-trim-cot-leakage` | 80 | 清理思维链泄漏——把不该出现在产物里的推理痕迹去掉 |
| `dsh-prose-standard` | 78 | 文字/文档的表达规范 |
| `dsh-ci-test-reliability` | 31 | 让 CI 里的测试不再时好时坏 |
| `dsh-speed-up-perf` | 22 | 性能提速 |

## 二、文档

| skill | 装机 | 一句话 |
|---|---|---|
| `dsh-translate-docs` | 62 | 文档翻译 |
| `dsh-doc` | 53 | 写文档 |
| `dsh-doc-standards` | 20 | 文档规范 |
| `dsh-doc-site-sync` | 18 | 文档站与仓库内容同步 |
| `dsh-create-upgrade-guide` | 11 | 生成升级指南 |

## 三、Agent 自身的经验与交接

| skill | 装机 | 一句话 |
|---|---|---|
| `dsh-archive-agent-notes` | 69 | 把 Agent 的笔记归档 |
| `agent-experience` | 7 | Agent 经验沉淀 |

> 这两个和本仓库 `skills/courseware-to-docx` 里的「第八步：把这次的教训写回本技能」
> 是同一类思路——**让 Agent 把自己跑过的经验留下来**。

## 四、Git 与 PR

| skill | 装机 | 一句话 |
|---|---|---|
| `dsh-merging-stacked-prs` | 63 | 合并 stacked PR（一个 PR 摞在另一个上） |

## 五、界面

| skill | 装机 | 一句话 |
|---|---|---|
| `dsh-client-ui-ux` | 13 | 客户端 UI/UX |

## 六、Cordis 插件框架

DSH 的插件体系叫 **Cordis**。这三条是官方给的插件框架参考。

| skill | 装机 | 一句话 |
|---|---|---|
| `cordis-plugin-development` | 4 | 开发 Cordis 插件 |
| `editing-cordis-compositions` | 4 | 编辑 composition（组合式配置） |
| `cordis-composition-reference` | 2 | composition 的参考手册 |

## 七、Office 文档

| skill | 装机 | 一句话 |
|---|---|---|
| `office-docx` | 2 | Word 文档 |
| `office-xlsx` | 1 | Excel 表格 |
| `office-pptx` | 1 | PowerPoint 演示 |

## 八、其他

| skill | 装机 | 一句话 |
|---|---|---|
| `record-browser-gif` | 62 | 把浏览器操作录成 GIF |

## 完整安装串

按 `install_source` 的规律，直接用任意一条：

```
skills.sh:deepseek-ai/deepseek-harness/dsh-code-review
skills.sh:deepseek-ai/deepseek-harness/dsh-find-simplifications
skills.sh:deepseek-ai/deepseek-harness/dsh-pre-push-checks
skills.sh:deepseek-ai/deepseek-harness/dsh-trim-cot-leakage
skills.sh:deepseek-ai/deepseek-harness/dsh-prose-standard
skills.sh:deepseek-ai/deepseek-harness/dsh-ci-test-reliability
skills.sh:deepseek-ai/deepseek-harness/dsh-speed-up-perf
skills.sh:deepseek-ai/deepseek-harness/dsh-translate-docs
skills.sh:deepseek-ai/deepseek-harness/dsh-doc
skills.sh:deepseek-ai/deepseek-harness/dsh-doc-standards
skills.sh:deepseek-ai/deepseek-harness/dsh-doc-site-sync
skills.sh:deepseek-ai/deepseek-harness/dsh-create-upgrade-guide
skills.sh:deepseek-ai/deepseek-harness/dsh-archive-agent-notes
skills.sh:deepseek-ai/deepseek-harness/agent-experience
skills.sh:deepseek-ai/deepseek-harness/dsh-merging-stacked-prs
skills.sh:deepseek-ai/deepseek-harness/dsh-client-ui-ux
skills.sh:deepseek-ai/deepseek-harness/cordis-plugin-development
skills.sh:deepseek-ai/deepseek-harness/editing-cordis-compositions
skills.sh:deepseek-ai/deepseek-harness/cordis-composition-reference
skills.sh:deepseek-ai/deepseek-harness/office-docx
skills.sh:deepseek-ai/deepseek-harness/office-xlsx
skills.sh:deepseek-ai/deepseek-harness/office-pptx
skills.sh:deepseek-ai/deepseek-harness/record-browser-gif
```

来源：<https://skills.sh/deepseek-ai/deepseek-harness>

> **核实程度**：全部为 `仅名称`——skills.sh 对这批条目没有返回描述字段，上表的"一句话"
> 是按名字归纳的，**未逐条核实正文**。装之前建议先看一眼原 skill。
