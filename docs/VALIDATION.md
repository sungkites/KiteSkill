# Release validation / 版本验证

Version: 0.1.0. Local verification date: 2026-11-12.

本记录区分已经执行的检查与尚未验证的能力；不将打包测试等同于科研判断验证。

| Check / 检查 | Observed result / 已观察结果 |
|---|---|
| Official skill-creator quick validation | All 7 skill folders passed |
| Repository metadata, local links and Python syntax | Passed with no reported errors |
| Helper unit/integration tests on Windows, Python 3.13 | 20 passed |
| Installation into an isolated directory | All 7 installed and matched source hashes |
| Managed update and backup | Tested, including local-edit/unmanaged collision protection and rollback after simulated manifest-write failure |
| Live DOI lookup | Crossref resolved `10.1038/s41586-021-03819-2`; supplied title/year/first-author fields matched; claim support was not checked |
| Plot helper smoke test | Synthetic example exported PDF, SVG, PNG and provenance JSON; PNG and rendered PDF inspected, SVG parsed |

The repository configures Windows/Linux GitHub Actions. Its actual run status is
reported by GitHub, not inferred from this local record. Optional external research
frameworks were not installed or tested as part of this release. Behavioral cases
in [ACCEPTANCE.md](ACCEPTANCE.md) remain manual evaluation scenarios.

本版没有验证模型的创新判断、录用预测或全自动论文质量，也没有运行个人研究项目。
演示图只检查绘图工具，不构成研究结果。
