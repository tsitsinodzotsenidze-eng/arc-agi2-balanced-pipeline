# ARC-AGI-2 public data provenance

Recorded on 2026-10-28. This record covers the official public GitHub data only.

## Source and immutable identifiers

- Official repository: https://github.com/arcprize/ARC-AGI-2
- Pinned commit: `f3283f727488ad98fe575ea6a5ac981e4a188e49` (2025-05-15, `readme updates`). This was the upstream `HEAD` returned by `git ls-remote` when downloaded.
- Pinned data: https://github.com/arcprize/ARC-AGI-2/tree/f3283f727488ad98fe575ea6a5ac981e4a188e49/data
- Git `data` tree: `e43b87b55bfcffa0d13a966a88fe58c3472f5450`
- Git `data/training` tree: `dac7259367cc5099ef6a7b604a50a93affbbee33`
- Git `data/evaluation` tree: `8d04288aac3146b7c47d0b799c18bc9c0217d838`

A shallow HTTPS clone succeeded locally. The source uses individual `data/training/<task_id>.json` and `data/evaluation/<task_id>.json` files. Both `train` and `test` pairs in these public source files include `input` and `output`; test outputs are labels and must be withheld from solver inputs.

## License

The upstream repository includes the Apache License, Version 2.0:

https://github.com/arcprize/ARC-AGI-2/blob/f3283f727488ad98fe575ea6a5ac981e4a188e49/LICENSE

The dataset license is distinct from competition requirements for a winning solution. Consult the current Kaggle rules for those requirements.

## Structural counts and local verification

Counts were calculated from JSON structure without displaying evaluation grids or labels.

| Public split | Task files | Test outputs | SHA-256 of file manifest |
| --- | ---: | ---: | --- |
| Training | 1,000 | 1,076 | `cc81c79f8a10ca3db2bbdd8e95d2fb094eca13e0803cf1eaa272da0a5b7054a6` |
| Evaluation | 120 | 167 | `f79d5dc2892fbcd819431a7dc434257a60ad2614921d9c1e0e1acbe1b4297ea1` |

The manifest hashes above are locally computed verification values, not publisher-issued release checksums. For each split, sort its JSON files by path; concatenate `relative_path + NUL + lowercase_sha256(file_bytes) + LF`, with paths relative to the repository root and UTF-8 encoding; compute SHA-256 of the concatenation. The JSON source files total 6,016,232 bytes.

No published GitHub release or remote Git tag was present when checked. The human-readable changelog records the initial 2025-03-24 release and April corrections, but Git history also includes May changes to evaluation test pairs. The immutable commit and tree identifiers above take precedence over a release date or an assumed test-output count.

Changelog: https://github.com/arcprize/ARC-AGI-2/blob/f3283f727488ad98fe575ea6a5ac981e4a188e49/changelog.md

## Evaluation interpretation

Official guidance reserves public evaluation tasks for testing and warns against inspecting tasks during development or repeatedly changing an algorithm in response to evaluation scores. For this project, freeze implementation and configuration before running public evaluation. Withhold test labels from the solver and use them only for scoring.

Report this as a **public retrospective benchmark**, not a pristine unseen holdout: general ARC knowledge and possible historical exposure cannot be excluded. Record the pinned revision, task/output denominators, frozen code revision, configuration, runtime, and scoring definition with any result.

The official benchmark README defines task success as solving every test input in a task within two attempts per input. The current Kaggle overview instead describes exact-match pass@2 averaged over individual test outputs. Report these separately if both are measured.

## GitHub versus Kaggle identity limitation

The current 2026 Kaggle competition bundle was not downloaded or compared in this provenance check. An unauthenticated request to Kaggle's competition data-list endpoint returned HTTP 401. No hidden competition tasks or labels were obtained.

Therefore, this record does **not** establish that Kaggle's public files are identical to this GitHub revision. File packaging, task pairs, output counts, and source revision must be checked against the actual Kaggle bundle before claiming equivalence. The Kaggle test-challenges file used during a submitted notebook rerun is a separate competition input, not this public evaluation split; derive submission IDs and test order from that runtime input.

## Official references

- Dataset structure and public/private distinctions: https://arcprize.org/arc-agi/2
- Development and evaluation guidance: https://arcprize.org/guide/1
- Pinned dataset README: https://github.com/arcprize/ARC-AGI-2/blob/f3283f727488ad98fe575ea6a5ac981e4a188e49/readme.md
- Current competition overview, scoring, and submission schema: https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/
- Current competition data page: https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/data
- Current competition rules: https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/rules
