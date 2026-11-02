# Attribution and license scope

NVARC authors: **Ivan Sorokin and Jean-Francois Puget (NVIDIA KGMoN)**.
The approach derives from the ARChitects solution. This project contributes
an attributed 2026 execution port, update-sensitivity design, exact-source
repeat carriers, engineering diagnostics and documentary evidence.

## Exact artifacts

1. https://www.kaggle.com/code/sorokin/arc2-qwen3-unsloth-flash-lora-batch4-queue
   — source Version10, preserved in `nvarc_port/vendor/author-v10.ipynb`.
2. https://www.kaggle.com/code/sorokin/pip-install-unsloth-flash-patch
   — dependency notebook Version2, preserved in `nvarc_port/vendor/dependency-v2.ipynb`.
3. https://www.kaggle.com/models/sorokin/qwen3_4b_grids15_sft139/transformers/bfloat16/1
   — external model Version1; weights are not included.

`nvarc_port/NOTICE` records a signed-in Kaggle license-field inspection on
28 October2026 showing Apache-2.0 for these three artifact-specific releases.
That dated observation is retained; it is not presented as a fresh license
inspection of every dependency or the entire upstream GitHub repository.
The separate 2 November Chat Amunia review reported current search-visible
Apache-2.0 text for the source notebook, while its dependency/model license
fields remained unreadable. That review supplements, rather than replaces,
the dated primary inspection. The root NVARC GitHub repository's missing
LICENSE is not substituted for these artifact-specific declarations.

The full Apache-2.0 text is retained at `nvarc_port/LICENSE`. Original project
NVARC wrapper additions and these publication documents use Apache-2.0.
Upstream copyright and attribution remain attached. External packages and
model assets retain their own licenses; a notebook label does not relicense
all installed dependencies. Built distributions and weights are excluded.

The original scaffold and public symbolic-pilot files remain separate project
history. The selected Zenodo package is scoped to NVARC carriers and study
evidence, not a blanket relicensing of every repository file. ARC Prize's
separate requirements for submitter-authored methods are not certified solely
by this source archive or its Apache-2.0 metadata.
