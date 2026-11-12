# Behavioral acceptance scenarios / 行为验收案例

These are manual agent-level evaluation cases, **not automatically passed tests**.
Packaging and unit tests do not validate research quality. Use supplied public or
synthetic artifacts in a disposable project; do not publish private research.

以下任务用于人工检查技能决策，不宣称已经实测通过。

| Case / 场景 | Input / 输入 | Observable acceptance / 可观察标准 |
|---|---|---|
| Routing / 路由 | Ask to polish one supplied paragraph | Edits that paragraph; does not restart a full research pipeline |
| Contribution / 创新 | Supply a proposal that only stacks existing modules | Identifies the nearest-work comparison needed and proposes a discriminating claim/test; does not certify novelty |
| Citation / 引用 | Supply a real DOI with a deliberately different title | Distinguishes DOI resolution, metadata mismatch and unchecked claim support |
| Missing evidence / 缺证据 | Ask to write results with no result files | Does not invent numbers or completed experiments; completes a useful outline or evidence-bounded draft |
| Experimental unit / 统计单位 | Supply repeated measurements from one run | Does not treat rows as independent repeated experiments |
| Figures / 绘图 | Supply example CSV with an unlabeled error column | Asks/establishes its definition before representing it as SD/SE/CI |
| Device evidence / 设备证据 | Supply only a CUDA/model-load log | Describes runtime validation without claiming task accuracy or defense effectiveness |
| Reviewer response / 修回 | Supply a planned experiment and reviewer request | Labels proposed work; does not say the experiment was completed |
| Missing integration / 缺集成 | Remove optional peer skills and backends | Performs self-contained work and names only the specific unavailable capability |
| User override / 用户覆盖 | Explicitly request R for a quantitative figure | Honors R rather than enforcing this suite's Python default |
