# Humanities Writing and Academic Argumentation (`humanities-writing`)

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0.1-blue.svg?style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blueviolet.svg?style=flat-square" alt="Python">
  <img src="https://img.shields.io/badge/Agents-Antigravity%20%7C%20Claude%20%7C%20Codex-orange.svg?style=flat-square" alt="Platform">
</p>

> **Clarifying academic arguments and restoring natural Chinese expression while strictly preserving evidence, original intent, and the author's authentic voice.**

`humanities-writing` is an Agent Skill crafted for Chinese humanities and social science research (philosophy, history, literature, sociology, law, communication studies, etc.) and in-depth non-fiction writing.

Addressing widespread LLM pitfalls in academic writing—such as fabricated citations, boilerplate jargon, rigid template imposition, and unauthorized alterations that weaken epistemic caveats—this project introduces a dual-track coordination architecture: **Academic Mode** and **General Writing Mode**.

---

## ✨ Key Highlights

- **Dual-Track Mode Architecture**:
  - **Academic Mode**: Specializes in refining research questions, matching theoretical frameworks with empirical materials, close reading, structured chapter transitions, abstract translation, and formatting audits. Preserves essential terminology, necessary distinctions (e.g. valid "not... but..."), and functional signposts.
  - **General Writing Mode**: Designed for essays, explanatory knowledge articles, and book forewords. Dispenses with cliché tropes while retaining first-person perspective, authentic sentiment, and vivid scenes.
- **Evidence Protection & Non-Fabrication Guarantee**:
  - Strictly prohibits fabricating authors, literature, dates, data, or personal anecdotes.
  - Clearly distinguishes between verifiable facts, source viewpoints, authorial inferences, and unknown information.
  - Guarantees that language polishes never exaggerate certainty or misrepresent correlation as causation.
- **Standalone Python Toolkit**:
  - `review.py`: Non-invasive, offline diagnostic text reviewer with zero third-party dependencies.
  - `search.py`: Multi-source literature retrieval supporting CNKI, Wanfang, Crossref, OpenAlex, Semantic Scholar, and Google Scholar.

---

## 🚀 Quick Start

### Installing into Agentic IDEs

#### Google Antigravity
```bash
# Global installation (available across all workspaces)
git clone https://github.com/liangshengsheng12333/humanities-writing.git ~/.gemini/antigravity/skills/humanities-writing

# Or local installation within current project
git clone https://github.com/liangshengsheng12333/humanities-writing.git .gemini/skills/humanities-writing
```

#### Claude Code / OpenAI Codex
Clone directly into your agent's skills directory:
```bash
git clone https://github.com/liangshengsheng12333/humanities-writing.git skills/humanities-writing
```

Call the skill via prompt:
> *"Use humanities-writing to review the following humanities paper draft. Focus on logical continuity between claims and evidence without rewriting the full text."*

---

## 📜 License

Licensed under the [MIT License](LICENSE).
See [`references/provenance.md`](references/provenance.md) for full origin and merging disclosures.
