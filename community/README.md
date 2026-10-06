# 社区生态

社区围绕 DeepSeek / DeepSeek Harness（DSH）做的 skill。官方那批见
[`../official/`](../official/)。

**这里的条目大多只拿到了名字（市场没返回描述）**，所以"一句话"多是按名字归纳的，
标了 `仅名称` 的**未经内容核实**，用前请自己看一眼。少数几条（主要来自 clawhub）拿到了
原作者写的描述，标 `描述可得`。

> ⚠️ **生态变动很快。** DSH 还在 pre-stable 阶段、breaking change 频繁，不少 skill 自带
> "上线版本门禁"就是为此。装机量低的条目尤其可能已经过期。

## 一、插件开发（社区里最卷的一类）

DSH 的插件体系基于 **Cordis**。官方那三条是参考，社区这些更偏"手把手"和"工作流"。

| skill | 作者 | 装机 | 说明 | 核实 |
|---|---|---|---|---|
| `dsh-plugin-development` | nanmicoder | 168 | 插件开发 | 仅名称 |
| **DSH Plugin Development** | liupengyang-1008 | — | 12 个模板、23 条踩坑、给 AI 配对开发用的提示词；**带强制前置版本门禁**，会拿活源码自校对自己的说法 | 描述可得 |
| `plugin-write` / `plugin-test` / `plugin-workflow` / `plugin-release` | oh-my-dsh | 145 / 140 / 138 / 136 | 写 / 测 / 工作流 / 发布 四件套 | 仅名称 |
| `submit-dsh-plugin` | imsai-sh | 25 | 提交插件（来自 `awesome-deepseek-harness-plugins`） | 仅名称 |
| **DeepSeek-Harness-cordis-plugin-builder** | kiwifruit13 | — | 从零构建 Cordis 插件的完整参考；含"插件加载失败（PENDING/FAILED）"排查 | 描述可得 |
| `build-deepseek-harness-plugin` | oil-oil | 9 | 构建插件 | 仅名称 |
| `deepseek-harness-plugin-creator` | win4r | 7 | 插件创建器 | 仅名称 |
| `dsh-plugin-dev` | zimodzh | 6 | 插件开发 | 仅名称 |
| `dsh-plugin-lint` | cat-xierluo | 5 | 插件 lint | 仅名称 |
| `deepseek-harness-plugin` | harcochen | 4 | 插件指南 | 仅名称 |
| `creating-dsh-plugins` | dsh-io | 4 | 创建插件 | 仅名称 |
| `dsh-plugin-guide` | perrylink | 4 | 插件指南 | 仅名称 |
| `dsh-write-plugin` / `dsh-test-plugin` | omdsh-dev | 4 / 4 | 写 / 测插件 | 仅名称 |
| `dsh-runtime` | dmitry-fomin | 3 | 运行时（来自 `dsh-plugin-claude-code`） | 仅名称 |
| `dsh-plugin-builder` | kingjly | 3 | 插件构建器 | 仅名称 |
| `dsh-plugin-dev-skill` | green-dalii | 2 | 插件开发 | 仅名称 |
| `deepseek-harness-plugin-dev` | alber70g | 1 | 插件开发 | 仅名称 |
| `publish-dsh-plugin` | ramenne | 1 | 发布插件 | 仅名称 |
| `dsh-dual-plugin-guide` | fectivnfy112357 | 1 | 双插件指南 | 仅名称 |
| `dsh-dev-full-skill` | xjiafei | 1 | 开发全流程 | 仅名称 |

## 二、部署 / 启动 / 排错

**这一组是中文作者做的最实用的一批**，尤其前三条——DSH 在 Windows 上的部署坑很多，
它们把坑列成了清单。

| skill | 作者 | 说明 | 核实 |
|---|---|---|---|
| **deepseek-harness-windows-deploy** | potfromsky | Windows 上以源码方式（pnpm monorepo）部署/构建/启动/排错：safe-delete 钩子冲突、pnpm 路径损坏、工作区持久化、EPERM 符号链接、端口 3080 等已知坑与**已验证命令** | 描述可得 |
| **deepseek-harness-desktop-shell** | potfromsky | 把本地已跑的 DSH Web UI（默认 `127.0.0.1:3080`）用 Electron 套成桌面应用：前置依赖、最小可运行壳、打包分发 | 描述可得 |
| **fore-vip-ds-harness** | onsoul | 傻瓜式本地启动助手：一句话讲清 DSH 是什么 → 引导拿 API Key → 按系统装 Node、配 npm 国内镜像、装并启动 dsh → 生成桌面快捷方式 | 描述可得 |
| `deepseek-harness` | henryz838978 | 装机 50，同名总览 | 仅名称 |
| `dsh-plugin-upgrade` | bruc3van | 插件升级（来自 `dsh-doctor`） | 仅名称 |
| `harness-doctor` | dongsheng123132 | 体检/诊断 | 仅名称 |
| `dsh-update-guide` | fabian-698 | 升级指南 | 仅名称 |
| `dshx` | dongsheng123132 | 装机 1 | 仅名称 |

**插件市场 / 找插件**（几个作者各自做了一套"插件商店"）：

| skill | 作者 | 装机 |
|---|---|---|
| `dsh-plugin-store` | dshmarketplace | 3 |
| `dsh-plugin-finder` | dshmarketplace | 1 |
| `dsh-plugin-finder-python` | dshmarketplace | 1 |
| `install-dsh-plugin` | yelebai | 1 |

**云上部署** —— ⚠️ **会真的产生费用**：

| skill | 作者 | 说明 |
|---|---|---|
| **huawei-cloud-ecs-dsh-deploy** | huaweicloud / huaweicloudskill | 华为云 Flexus X 部署 DSH。作者自己标了"部署涉及实际费用，执行前必须与用户确认区域/规格/计费方式" |

## 三、OCR 与文档解析

两条都来自同一作者，都是**从 DSH 的 Settings 图形界面装官方 OCR 插件**：

| skill | 作者 | 说明 | 核实 |
|---|---|---|---|
| **DeepSeek Harness PaddleOCR GUI Setup** | aidenwu0209 | 配 PaddleOCR 插件：截图/扫描件/PDF 转文字、中文 CJK、PDF→Markdown、表格公式版面与阅读顺序 | 描述可得 |
| **DeepSeek Harness Unlimited-OCR GUI Setup** | aidenwu0209 | 配 Unlimited-OCR 插件：长文档 OCR、PDF/OFD/Office/纯文本/扫描图 → Markdown；支持百度云或本地 SGLang / OpenAI 兼容服务 | 描述可得 |

> 这两条和本仓库 `../skills/` 里的课件/视频 skill 是同一片需求（**读不出文字的 PDF**），
> 区别是它们走 DSH 的原生 OCR 插件，本仓库那两个走渲染读图 + ASR。

## 四、子代理 / 协作 / 路由

| skill | 作者 | 说明 | 核实 |
|---|---|---|---|
| **ODSH-Interop** | mikoribbit | OpenClaw ↔ DSH 的路由决策：按任务大小和预估 token 成本判断该自己干还是转交 DSH；含 envelope 契约、通知频道配置、可选的 SQLite 审计账本（`dsh.db`）查询 | 描述可得 |
| `deepseek-harness-subagent` | x22x22 | 子代理 | 仅名称 |
| `dsh-native-playbook` | cyanseek | 原生玩法手册 | 仅名称 |
| `dsh-community-plugins` | hubaking | 社区插件一览 | 仅名称 |
| `dsh-runner` | bestdeejay-design | 运行器 | 仅名称 |
| `dsh-web-ui-web-qa` | zhu1090093659 | Web UI 的 web QA | 仅名称 |
| `use-dsh-harmony` | memorax-ai | 装机 2 | 仅名称 |
| `yashi-dsh-config-sync` | kagurazakayashi | 配置同步 | 仅名称 |
| `review-it` | 9ashwin | 来自 `dsh-floway` | 仅名称 |

## 五、DeepSeek API / 模型集成（不限于 DSH）

如果你的场景只是"在别的客户端里用 DeepSeek"，这一组更相关：

| skill | 作者 | 装机 | 说明 | 核实 |
|---|---|---|---|---|
| `deepseek` | okou-ai | 282 | 装机最高的一条 DeepSeek skill | 仅名称 |
| `write-notes-like-deepseek` | czm15053 | 226 | 按 DeepSeek 的风格写笔记 | 仅名称 |
| `deepseek-websearch` | redfox-data | 98 | 联网搜索 | 仅名称 |
| `deepseek-balance` | wmy2981 | 54 | 查余额 | 仅名称 |
| **DeepSeek Integration** | barisoezcan1905 | — | 把 DeepSeek API 接进 agent，做代码生成、解题、分析，端点可配（原站名字拼成了 `Intergration`） | 描述可得 |
| **Deepseek聊天** | thcjp | — | 中文对话、自动化配置与参数设置、工作流与批处理 | 描述可得 |
| `deepseek-plugin` | stepupgaming | 1 | 装机 1 | 仅名称 |
| `token-stats-skill` | baijian | 4 | token 统计 | 仅名称 |

## 六、别人也在做同类合集

搜的时候顺手发现两个社区自建的 DSH 合集，值得一看：

- `imsai-sh/awesome-deepseek-harness-plugins`
- `dominic789654/awesome-deepseek-harness`

## 安装串（按需自取）

```
clawhub:liupengyang-1008/dsh-plugin-development
clawhub:potfromsky/skills/deepseek-harness-windows-deploy
clawhub:potfromsky/skills/deepseek-harness-desktop-shell
clawhub:onsoul/skills/fore-vip-ds-harness
clawhub:kiwifruit13/skills/cordis-plugin-builder
clawhub:aidenwu0209/skills/dsh-paddleocr-skills-setup
clawhub:aidenwu0209/skills/dsh-unlimited-ocr-skill-setup
clawhub:mikoribbit/skills/odsh-interop
clawhub:huaweicloudskill/skills/huawei-cloud-ecs-dsh-deploy
clawhub:barisoezcan1905/deepseek
clawhub:thcjp/deepseek-chat

skills.sh:nanmicoder/dsh-agent-teams/dsh-plugin-development
skills.sh:oh-my-dsh/dsh-plugin-upgrade-skill/plugin-write
skills.sh:imsai-sh/awesome-deepseek-harness-plugins/submit-dsh-plugin
skills.sh:henryz838978/deepseek-harness/deepseek-harness
skills.sh:okou-ai/okou-skills/deepseek
skills.sh:czm15053/write-notes-like-deepseek/write-notes-like-deepseek
skills.sh:redfox-data/redfox-community/deepseek-websearch
skills.sh:wmy2981/skills/deepseek-balance
```
