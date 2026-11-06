# Additional MIT-0 grant for original ARC2 contributions

**Author:** Tsitsino Dzotsenidze, ORCID [0000-0002-9432-1803](https://orcid.org/0000-0002-9432-1803).  
**Approved:** 6 November 2026.  
**Scope source:** commit `84d84e2a5b8bad8459ed1a04511743df0bf257fe`.

The author grants the permissions in [MIT No Attribution (MIT-0)](LICENSE-MIT-0.txt) as an additional licence for **her independently authored ARC2 code additions and reusable method specifications/pseudocode only**, as identified in [the immutable-source scope map](MIT0_SCOPE_2026-11-06.json). Existing Apache-2.0 grants and third-party notices are retained. No attribution requirement is added to MIT-0; the author credit here is scholarly provenance.

## Included author-owned portions

- Original wrapper, input/deadline adaptation and instrumentation in `driver.py`.
- Original packaging/control code in `build_notebook.py`, `build_b1.py` and `build_update_study.py`.
- Original code in `zero_update_probe.py`, `zero_update_probe_support.py`, `test_wrapper.py`, `test_b1.py` and `test_update_study.py`.
- Corresponding original wrapper/glue portions in the B0/B1/Z1/repeat carriers and `B1_Cell2_CodeOnly.py` / `Z_Cell2_CodeOnly.py`. This does not include the embedded third-party notebook payloads.
- Original method specifications and pseudocode in `../docs/ARC2_UPDATE_STRENGTH_PROTOCOL_2026-10-29.md` and `../docs/ARC2_PRIORITY_AMENDMENT_2026-10-30.md`.

Names are relative to `nvarc_port/` unless an explicit relative path is given. The scope map identifies each reference file by Git blob SHA, together with B1's embedded driver SHA-256 and the excluded upstream notebook payload hashes. Listing a file does not mean every byte is independently authored: inherited source fragments, quoted code and patch-match strings are excluded. The grant applies to the specified original contributions embodied in those unchanged source versions, not solely to future revisions.

## Exclusions and retained rights

This grant does **not** relicense NVARC/ARChitects source, vendored notebooks, dependencies, model weights, benchmark/Kaggle data, synthetic smoke challenge data, hidden predictions or third-party licence/notice text. These retain their applicable terms and authorship.

It does not apply to the combined article's prose, title, Word/PDF, figures or bibliography. It does not cover ARC3 code, external SQLite, upstream overlays, game graphics or LP85 empirical CSV/coordinate records. The prior LP85 author-method grant retains its separate, narrower scope.

No executed notebook or scientific result was changed to record this grant. Existing releases/tags and the three published DOI records are preserved: ARC2 `10.5281/zenodo.23895859`, ARC3 `10.5281/zenodo.23869166`, and the combined paper `10.5281/zenodo.23989843`. The author approval receipt is [recorded separately](AUTHOR_LICENSE_APPROVAL_2026-11-06.json).
