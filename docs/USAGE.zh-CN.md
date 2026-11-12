# KiteSkill 中文使用指南

[English](USAGE.en.md) · [返回首页](../README.md)

## 选择入口

任务明确时直接用对应模块；不明确时用 `$kite-research`。各模块的 `SKILL.md`
使用英文执行说明以便跨客户端使用，包含中英文触发词；用户交流与交付语言跟随请求。
中英文说明文档不影响你用中文调用。

| 你已有的材料 | 推荐调用 | 应得到的交付物 |
|---|---|---|
| 一个宽泛方向、几篇论文 | `$kite-ideation` | 最近工作对比、机制问题、候选假设、最小试验 |
| 主张或关键词 | `$kite-literature` | 检索记录、真实文献、主张—原文证据表 |
| 明确方法和研究问题 | `$kite-experiments` | 公平对照、关键消融、统计单位、资源预算 |
| 结果、图表、中文初稿 | `$kite-writing` | 有证据支持的论文正文或精确润色稿 |
| CSV、方法描述 | `$kite-figures` | 图的论证目标、源代码、导出文件、图注 |
| 完整稿件或审稿意见 | `$kite-review` | 按重要性排序的问题，或逐点回复与修改位置 |

## 可直接复制的调用

```text
用 $kite-ideation 分析这个方向。先比较最接近的原始研究，再给出具体机制问题、
可证伪的主张，以及一个能决定是否值得继续的小型真实数据实验。
```

```text
用 $kite-literature 为以下引言主张找文献。逐条列出 DOI、题名、年份、原文位置、
实际支持范围和全文可获取情况，不用摘要推测未读的全文结论。
```

```text
用 $kite-writing 根据这些结果写论文的 Results 和 Discussion。
重点是方法与证据，不把环境配置和运行日志写进正文；英文风格遵循目标期刊。
```

```text
用 $kite-review 处理这封审稿意见。区分已完成修改和拟补实验，
把每条意见映射到真实证据与稿件位置，并完成当前已授权的修改。
```

## DOI 核验

CSV 至少包含 `doi`，可选 `title,year,first_author`；`first_author` 填第一作者姓氏
或团体作者全名。字段名用小写。元数据匹配只针对实际提供的字段。

```bash
python skills/kite-literature/scripts/verify_doi.py references.csv --output research-output/doi-report.json
```

状态：`resolved_only` 仅解析到记录；`metadata_match` 所提供字段匹配；
`needs_review` 有字段差异；`unverified` 格式、网络或提供方查询尚未核验。
Crossref 未找到不代表论文不存在。年份接受记录中的正式出版或在线出版年，
但期刊参考文献应采用哪一个仍需人工确认。题名标准化后不完全相同会标记复核。
每条记录均标记 `claim_support: not_checked`；引文支持需要阅读原文。

## CSV 绘图

```bash
python -m pip install "matplotlib>=3.8,<4"
python skills/kite-figures/scripts/plot_csv.py results.csv --kind line --x budget --y score --series method --xlabel "Budget" --ylabel "Score" --output research-output/figures/result
```

`--kind` 可选 `line/scatter/bar`；`bar` 的 x 可为类别，其余使用数值 x。
误差列增加 `--yerr sd --error-label "supplied SD"`。不自动算均值或区间。
同一序列中的重复 x 在 line/bar 中会停止，要求先明确汇总方案；scatter 可显示重复点。
缺失值和无穷值不会静默删除。输出同前缀的 PDF、SVG、PNG 和来源 JSON。
已有输出默认不覆盖，需要明确传入 `--overwrite`。

`examples/demo.csv` 仅用于工具演示，数值为合成数据，不能用于论文证据。
把上面命令的 `results.csv` 换为 `examples/demo.csv` 可以试画。

## 能力边界

安装本套件不等于安装数据库连接、文献下载后端或图片生成模型。运行环境没有检索、
渲染或 GPU 能力时，模块会说明具体缺口，继续完成不依赖它的工作。
可选框架按需启用，不会预先下载权重，也不会默认上传论文或实验材料。

项目笔记和产出存入你的项目目录；不要写回安装的技能文件或公开的 KiteSkill 仓库。
单个句子润色无需全套文献—实验流程，整篇论文才需要阶段交接和证据整理。
