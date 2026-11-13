# 人文写作与学术论证 (humanities-writing)

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0.1-blue.svg?style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blueviolet.svg?style=flat-square" alt="Python">
  <img src="https://img.shields.io/badge/Agents-Antigravity%20%7C%20Claude%20%7C%20Codex-orange.svg?style=flat-square" alt="Platform">
</p>

> **让学术论证更清楚，让中文表达更自然，同时保留证据、原意和作者声音。**

`humanities-writing` 是一套专为**中文人文社科论文（文史哲、社科、法学、传媒等）与一般中文深度写作**设计的全流程智能体技能（Agent Skill）。

针对通用大模型在学术写作中常见的“编造引文”、“机械化套话”、“生搬硬套模板”以及“过度修改抹杀作者原意与推断强度”等核心痛点，本项目通过**学术模式**与**一般写作模式**双轨协调规则，在严格遵从学术规范与概念边界的前提下，恢复中文自然流动的表达力。

---

## ✨ 核心特性

- 🎯 **双轨工作流模式**：
  - **学术模式**：专注研究问题提炼、理论与材料契合度、细读分析、章节推进、学术摘要翻译与投稿格式核对。保留必要术语、辨析句式（如合理的“不是……而是……”）及结构化功能路标。
  - **一般写作模式**：面向随笔、知识讲解、图书或项目前言。打破八股套话，保留作者真情实感、第一人称视角与生动场景，拒绝机械化总结与廉价升华。
- 🛡️ **事实与证据共享底线**：
  - **严禁虚构**：绝不无中生有编造文献、页码、数据、历史细节或个人经历。未核实内容显式标注“待查证”。
  - **边界清晰**：明确区分“可核实事实”、“文献观点”、“作者推论”与“未知信息”。只读到摘要时，绝不伪装已通读全文进行论证拆解。
  - **原意保护**：语言审校不得擅自加强结论强度、不得删除论证限定词、不得将相关关系篡改为因果关系。受保护的引语、术语和原作者声音绝不为文风牺牲。
- 🔍 **多源学术检索与本地保守审校**：
  - 内置开箱即用的轻量级 Python 工具链：`review.py` 提供不改变原意的离线启发式审校诊断；`search.py` 支持知网 (CNKI)、万方、Crossref、OpenAlex、Semantic Scholar、Google Scholar 等多源文献聚合检索适配。

---

## 📂 项目结构

```
humanities-writing/
├── SKILL.md                  # 核心技能规范定义与全局协调规则（Agent 入口）
├── requirements.txt          # 可选依赖（仅针对特定网页解析适配器）
├── LICENSE                   # 开源许可协议 (MIT)
├── agents/                   # 智能体平台元数据配置
│   └── openai.yaml           # OpenAI Codex / GPTs 交互元数据
├── references/               # 10 篇核心学术规则与理论参考手册
│   ├── academic-workflow.md  # 学术论文全流程指南（选题、框架、论证）
│   ├── general-writing.md    # 一般中文写作指南（随笔、讲解、前言）
│   ├── literature-workflow.md# 文献与材料分析规范（阅读边界、综述）
│   ├── style-review.md       # 自然语言审校标准（去模板化、虚假客观性诊断）
│   ├── writing-functions.md  # 写作功能部件规范（引言、过渡、结语）
│   ├── translation-formatting.md # 摘要英译与规范核对
│   ├── theory-frameworks.md  # 常用人文社科理论框架速查
│   ├── terminology-bilingual.md # 汉英学术术语对照表
│   ├── tools.md              # 配套脚本使用说明与配置手册
│   └── provenance.md         # 来源、合并演进与版本说明
├── scripts/                  # 审校与检索工具套件
│   ├── review.py             # 离线文本保守审校诊断工具（零第三方依赖）
│   ├── search.py             # 多源文献聚合检索工具
│   ├── lib/                  # 检索核心算法（去重、打分、引文格式化、Schema）
│   └── sources/              # 数据源适配器（CNKI、万方、OpenAlex、Crossref 等）
├── examples/                 # 交互展示与实战提示词
│   ├── prompt-templates.md   # 5 大典型场景即用型 Prompt 模板库
│   └── showcase.html         # 效果对比交互展示页面
└── docs/                     # 验证基线与发布指南
    ├── verification-summary.md  # 自动化验证基线与测试说明
    ├── verification-v1.0.1.json # 自动化测试结果机器可读文件
    └── marketplace-upload-guide.md # Skill 市场/平台打包发布说明
```

---

## 🚀 快速上手

### 1. 在智能体环境中使用 (Agentic Workspaces)

#### 🔹 Google Antigravity
克隆或下载本仓库至 Antigravity 的技能目录：
```bash
# 全局安装（所有工作区通用）
git clone https://github.com/liangshengsheng12333/humanities-writing.git ~/.gemini/antigravity/skills/humanities-writing

# 或当前项目内局部安装
git clone https://github.com/liangshengsheng12333/humanities-writing.git .gemini/skills/humanities-writing
```

#### 🔹 Claude Code / OpenAI Codex
直接将仓库克隆至你的 Agent 工作区或 Skills 目录：
```bash
git clone https://github.com/liangshengsheng12333/humanities-writing.git skills/humanities-writing
```
在对话中直接通过 `$humanities-writing` 或自然语言唤醒：
> *“使用 humanities-writing，对以下论文段落进行审阅，重点指出论据与论点之间的逻辑断层，不改写全文。”*

---

### 2. 本地独立工具使用 (CLI Scripts)

本项目核心规则完全无需任何依赖。如果你需要运行配套脚本，仅需 Python 3.10+：

#### 📝 本地文本审校 (`review.py`)
离线对 Markdown 或纯文本进行保守审校，检查空洞套话、过度概括及未声明的假设，绝不私自覆写源文件：
```bash
# 学术模式审阅
python scripts/review.py your_paper.md --mode academic

# 一般写作模式审阅（随笔/讲解）
python scripts/review.py your_essay.md --mode general

# 输出 JSON 格式诊断结果
python scripts/review.py your_paper.md --format json
```

#### 🔎 学术文献聚合检索 (`search.py`)
支持多数据源检索并自动格式化输出 GB/T 7714、Chicago 或 MLA 格式引文：
```bash
# 安装可选网页解析依赖（如需解析特定网页源）
pip install -r requirements.txt

# 列出所有已支持的数据源配置状态
python scripts/search.py --list-sources

# 聚合搜索学术文献并输出 GB/T 7714 格式
python scripts/search.py "数字人文 记忆场所" --style gbt7714 --format markdown
```

---

## 💡 典型提示词示例 (Prompt Showcase)

详细模板请参阅 [`examples/prompt-templates.md`](examples/prompt-templates.md)。

````markdown
使用 humanities-writing，润色下面的中文人文社科论文片段。
要求：
1. 保留专业术语、直接引语、文献出处及所有论证限定词；
2. 严格维持原有判断强度，不擅自加强结论或将相关改因果；
3. 不编造新增文献或论点；
4. 直接交付修改稿，重要问题在正文后简要附注。

【待润色片段】：
...
````

---

## 🧪 质量验证与基线

本项目核心 Skill 已通过官方 Agent 规范结构验证以及 **27 项自动化严苛测试**，覆盖：
- 引用保护与跨行引文括号隔离
- 论据保守去重与元数据完整性
- 标题编号智能识别与非侵入式审校
- TLS 传输加密与异常安全降级

详见 [`docs/verification-summary.md`](docs/verification-summary.md) 及 [`docs/verification-v1.0.1.json`](docs/verification-v1.0.1.json)。

---

## 📄 开源许可与来源说明

- 本项目基于 [MIT License](LICENSE) 开源。
- 演进来源与合并边界详见 [`references/provenance.md`](references/provenance.md)。

欢迎为人文社科研究者与深度中文创作者贡献更多理论速查词条与工具适配器！
