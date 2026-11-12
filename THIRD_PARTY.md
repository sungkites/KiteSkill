# Sources and optional integrations / 参考来源与可选集成

KiteSkill's instructions and helper code are independently authored. The projects
below informed the modular design or are useful optional integrations. No upstream
skill bundle, model, template or helper source is vendored in this release.
This file records conceptual attribution and discovery links, not a claim that
all integrations are installed, tested or interchangeable.

本版为独立编写的模块和工具，没有整体复制第三方技能。下列项目是流程参考或可选工具，
不代表它们已经安装、兼容性已验证，或本仓库拥有它们的代码。需要复制上游材料时应另行
核查对应文件的许可和署名要求。许可证信息核查日期：2026-11-12。

## Workflow references / 流程参考

| Project | Role in KiteSkill | License / note |
|---|---|---|
| [K-Dense scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | Scientific writing, evidence-aware hypotheses, critical analysis, statistics and scientific visualization informed module boundaries | MIT; formerly claude-scientific-skills |
| [K-Dense claude-scientific-writer](https://github.com/K-Dense-AI/claude-scientific-writer) | Writing-centered workflow and venue-specific adaptation | MIT; optional external service dependencies |
| [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills) | Bilingual manuscript work, reference checks, figure inspection and reviewer-response task coverage | Apache-2.0; community project, no Nature affiliation implied |
| [Orchestra AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | Ideation, ML experiment-to-paper workflow and domain engineering capabilities | MIT |
| [ResearchPilot-Skills](https://github.com/LMDHQ-0420/ResearchPilot-Skills) | Research-stage decomposition and claim–experiment–manuscript handoff | MIT |
| [luwill/research-skills](https://github.com/luwill/research-skills) | Results-first paper drafting, proposals and literature-citation discipline | No repository license identified in this check; link/reference only, not redistributed |
| [jt1024/academic-polish](https://github.com/jt1024/academic-polish) | Separating grammar, style, logic and terminology in polishing tasks | Link/reference only; inspect current license before reuse |
| [Codex scientific writing skill](https://github.com/StickTaTa/codex-scientific-writing-skill) | Example of focused Codex packaging rather than requiring a full ecosystem | Link/reference only; retains upstream attribution |

## Optional tools / 可选工具

| Project | Useful capability | What installing KiteSkill does |
|---|---|---|
| [gpt_academic](https://github.com/binary-husky/gpt_academic) | Academic UI, polishing, PDF/LaTeX reading/translation | Does not install it |
| [paper-search-mcp](https://github.com/openags/paper-search-mcp) | Multi-source discovery and accessible PDF retrieval | Uses it only if available in the host |
| [Zotero MCP](https://github.com/54yyyu/zotero-mcp) | Connect the user's Zotero library | Does not configure a library or API key; community server |
| [PaperQA](https://github.com/Future-House/paper-qa) | Source-grounded scientific-document questions | Optional full-text analysis backend |
| [STORM](https://github.com/stanford-oval/storm) | Multi-perspective topic research and cited reports | Optional background synthesis, not automatic systematic-review certification |
| [GPT Researcher](https://github.com/assafelovic/gpt-researcher) | Web/document research reports | Optional research backend; scholarly sources still need selection |
| [SciencePlots](https://github.com/garrettj403/SciencePlots) | matplotlib styles | Optional styles; bundled plot helper works without it |
| [AutoIllustrate](https://github.com/SakanaAI/AutoIllustrate) | Editable draw.io method figures | Optional diagram backend; no automatic installation |
| [PaperVizAgent](https://github.com/google-research/papervizagent) | Reference-driven academic illustration pipeline | Optional conceptual illustration backend |
| [paperbanana-skill](https://github.com/PlutoLei/paperbanana-skill) | Figure/deck agent skills and configured generation pipeline | Optional community project; not a vendored component |
| [PlotNeuralNet](https://github.com/HarisIqbal88/PlotNeuralNet) | Code-generated neural architecture diagrams | Optional LaTeX/TikZ route |
| [AI-Scientist-v3](https://github.com/SakanaAI/AI-Scientist-v3) | Coding-agent experiments, baselines, ablations and paper generation | Architecture reference/optional framework; not automatically launched |
| [HKUDS AI-Researcher](https://github.com/HKUDS/AI-Researcher) | Autonomous research development and experimental workflows | Architecture reference/optional framework; not automatically launched |

## APIs and libraries actually used / 实际调用的接口与依赖

- DOI helper: [Crossref REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/).
  Crossref is one metadata provider, not a claim-support or study-validity authority.
- Plot helper: [Matplotlib](https://matplotlib.org/), installed separately by the user.
- Package validator: [PyYAML](https://pyyaml.org/), a development dependency.
- UI metadata and skill packaging follow the host's Agent Skills conventions.
  No promise is made that every host implements the same tools or UI fields.

External services retain their own terms, credentials, access conditions and costs.
KiteSkill's MIT license applies only to this repository's original material.
