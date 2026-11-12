# Evidence design / 证据设计

## Minimal useful experiment plan

| Claim | Rival explanation | Comparison/intervention | Unit and pairing | Metric/interval | Falsifier | Budget/stop |
|---|---|---|---|---|---|---|

Use this table to remove experiments that do not change a decision. A mechanism
ablation should distinguish the proposed mechanism from capacity, training time,
data leakage, tuning or implementation advantages. Simply removing a component
can confound all of these; add matched controls when needed.

## Statistical choices

- Pair conditions when they share meaningful experimental units. Bootstrap at the
  independent unit or appropriate cluster, preserving pairs; document the resampling
  unit and interval method. Do not resample individual tokens as independent model runs.
- Show raw points or distributions when feasible. Match aggregation to the claim;
  macro and micro averages answer different questions. Define every denominator.
- Distinguish exploratory subgroup/sensitivity work from prespecified primary tests.
  Report the family of tests and multiplicity strategy when relevant.
- Prefer interpretable effects and uncertainty to a standalone p-value. A wide
  interval does not support a precise effect claim.

## Resource and provenance record

Record source data/version, split identifiers, code revision, model/weights,
configuration, seed, device, elapsed time, memory and energy/cost if actually
measured. Never label estimated cost as metered consumption. Keep credentials and
private endpoints out of shared artifacts.

## Device evidence classes

| Observation | What it supports | What remains untested |
|---|---|---|
| CUDA loads; model answers a prompt | Runtime smoke test | Accuracy, safety or defense effectiveness |
| Matched task on an edge device | Deployment latency/memory in that setting | Independent replication or training benefit |
| Prespecified evaluation in a genuinely distinct setting | Bounded external validation | Universal generalization |

If the user requests replication, specify what is independently repeated (data,
implementation, seeds, hardware, team/site) and why it addresses the original claim.
