# KiteSkill

**把科研问题、文献证据、实验和论文连接起来的个人 SCI 科研技能套件。**

[English](README.en.md) · [中文使用指南](docs/USAGE.zh-CN.md) ·
[English guide](docs/USAGE.en.md) · [参考项目与工具](THIRD_PARTY.md)

KiteSkill 提供 7 个可以独立安装、直接调用的 Agent Skills，优先面向 Codex，
也可把完整技能目录装入支持 `SKILL.md` 的其他智能体。它将科研工作流重新组织为
自己的 `kite-*` 模块，不要求先安装整套第三方科研框架。

## 模块

| 调用名称 | 负责什么 | 示例 |
|---|---|---|
| [`$kite-research`](skills/kite-research/SKILL.md) | 总入口：判断项目阶段、衔接模块、继续已有工作 | 用我的 KiteSkill，基于当前项目推进下一项关键工作 |
| [`$kite-ideation`](skills/kite-ideation/SKILL.md) | 选题、机制分析、创新边界、可检验假设 | 从最接近的原始文献寻找可验证的机制贡献 |
| [`$kite-literature`](skills/kite-literature/SKILL.md) | 检索、精读、证据映射、引用与元数据核验 | 为这些主张找真实来源，列出原文位置和支持范围 |
| [`$kite-experiments`](skills/kite-experiments/SKILL.md) | 对照、消融、统计、鲁棒性、效率、资源与小型试验 | 围绕这个主张设计有决定性的比较和机制实验 |
| [`$kite-writing`](skills/kite-writing/SKILL.md) | 起草、重构、中英翻译、学术润色 | 根据已有结果写引言，保持科学含义和引用准确 |
| [`$kite-figures`](skills/kite-figures/SKILL.md) | Python 数据图、多面板图、方法示意图与导出检查 | 用真实 CSV 绘制论文图，提供源代码、PDF/SVG/PNG |
| [`$kite-review`](skills/kite-review/SKILL.md) | 投稿前审查、统计和证据审查、逐点回复、修回 | 检查主张—证据是否一致，并修改审稿回复 |

## 为科研需求做的取舍

- 优先具体的科学或机制贡献；组合模块、改名指标、更多算力本身不等于创新。
- 比较要可信、条件要可比；主实验、必要消融和成本分析围绕明确主张展开。
- 引用真实且相关。完整研究论文可按 30–50 篇已核验文献规划，服从学科、期刊和论证需要，不凑数。
- 中文讨论自然简洁，英文正文按目标期刊调整。论文正文突出方法、证据和解释，运行日志放到复现材料。
- 定量绘图默认 Python；显式指定其他后端时遵从用户。实际查看导出图后再交付。
- A100/Orin 等资源按具体研究问题使用；设备与存储状态现场检查，不把环境冒烟测试当作研究效果。
- 只为所需任务加载对应模块；保留已有授权，不人为添加每阶段确认流程。

## 本地安装

需要 Python 3.10+ 和 Git。安装器仅使用 Python 标准库，不安装模型、GPU 运行时或付费服务。

```bash
git clone https://github.com/sungkites/KiteSkill.git
cd KiteSkill
python scripts/install.py
python scripts/install.py --check
```

默认安装到 `$CODEX_HOME/skills`，未设置时为 `~/.codex/skills`。从下一轮对话开始调用；
如果客户端未刷新技能列表，再重新打开会话或重启客户端。

只安装指定模块：

```bash
python scripts/install.py --skills kite-writing kite-figures
```

其他支持 Agent Skills 的客户端：指定其技能目录，例如
`python scripts/install.py --dest ~/.claude/skills`。
智能体的工具、权限和自动发现行为以实际客户端为准。

## 更新与本地修改保护

```bash
git pull --ff-only
python scripts/install.py --update
python scripts/install.py --check
```

安装器不覆盖不同内容的未托管同名目录；已托管技能存在本地修改时停止并指出冲突。
更新前将旧版本移至技能目录的父目录下 `kite-skill-backups/`，再安装校验后的新副本。
更新批次失败会尝试恢复已移动的旧版本。重复安装相同内容不会重写技能文件。
维护副本与已安装副本分开，长期修改建议在仓库内进行，再通过安装器更新。

也可以让支持 GitHub 技能安装的智能体从本仓库的 `skills/kite-*` 完整目录安装。
只复制 `SKILL.md` 会遗漏参考文件、界面信息和工具脚本。

## 如何调用

```text
用 $kite-research 继续当前论文，只推进当前缺少的关键工作。

用 $kite-ideation 分析这些文献，提出有机制依据的研究问题和最小验证实验。

用 $kite-writing 把这段中文改为学术英文，保持数字、因果强度和引文含义。

用 $kite-figures 读取 results.csv，先明确图要支持的结论，再画图并检查导出文件。
```

无需记住全部名称，明确说“用我的 KiteSkill”可交给总入口判断。
单个模块不依赖其他 Kite 模块才能工作。

## 随包工具与可选依赖

| 能力 | 工具/依赖 | 边界 |
|---|---|---|
| 安装、更新和内容核验 | `scripts/install.py`；标准库 | 不修改无关技能或客户端配置 |
| DOI 字段核验 | `skills/kite-literature/scripts/verify_doi.py`；标准库、Crossref 网络访问 | 对比 DOI、题名、年份、第一作者姓氏；不证明引文支持、完整作者顺序或研究有效性 |
| CSV 基础绘图 | `skills/kite-figures/scripts/plot_csv.py`；matplotlib | 按现有值绘制，不自动聚合、推断置信区间或进行显著性检验 |
| 结构检查与测试 | `requirements-dev.txt` | 检查技能打包、安装行为和工具；不代表科研判断能力已获验证 |

绘图时按需安装：`python -m pip install "matplotlib>=3.8,<4"`。
文献检索、文件渲染和模型调用使用客户端已有能力。
Zotero MCP、PaperQA、SciencePlots、AutoIllustrate 等是可选扩展，见
[工具来源表](THIRD_PARTY.md)，不会随安装器自动下载。

## 开发与验证

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
```

GitHub Actions 配置了 Windows/Linux 的同一组检查；实际运行状态以 Actions 为准。
[行为验收案例](docs/ACCEPTANCE.md) 是可复用的人工验收任务，不表示它们已被智能体实测通过。

## 来源与许可

本仓库代码和技能说明采用 MIT 许可。技能是结合个人科研需求编写的独立工作流，
没有把上游仓库整体复制改名。参考项目、可选后端及其边界在
[THIRD_PARTY.md](THIRD_PARTY.md) 说明；这些外部项目继续适用各自的许可证。

技能提供研究辅助，不保证创新性、SCI 分区或录用。作者需要核对数据、引用和最终科学结论。
