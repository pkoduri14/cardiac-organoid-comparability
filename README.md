# Cardiac-Organoid Comparability Resource

Data and code accompanying "Making Cardiac-Organoid Literature Comparable: An Arm-Level Framework and Source-Linked Resource," JCDL 2026.

A source-linked resource of 114 papers and 367 protocol arms. Each arm carries an explicit
construct-comparability verdict and, where the arm is not comparable, a single primary failure code.
31 arms (8 percent) pass the gate.

Every arm that passes the gate carries a supporting quotation and a page locator, so each of those
verdicts can be checked against its source. Coverage is partial elsewhere: of the 111 reported
cardiomyocyte fractions, 98 carry a quotation, and among the 80 reported by excluded arms, 67 do.

## Contents

| File | What it is |
|---|---|
| `cardiac_organoid_arms.xlsx` | The resource. One row per protocol arm, 54 fields, including the comparability verdict, its reason, a DOI, and the supporting quotation and page where one was extracted. |
| `comparability_codebook_v1.1.md` | The gate and the eight failure codes, with the priority order used to assign a single primary reason. Includes the v1.0 to v1.1 revision history. |
| `comparability_codebook_v1.1.1.md` | Post-evaluation clarification of v1.1: the same gate and codes, with an explicit rule for derived pan-CM totals. |
| `included_papers.csv` | The 114 included papers with author, year, journal, DOI, and arm count. |
| `data_dictionary.csv` | Field-level definitions for the resource schema. |
| `correction_log.csv` | Every correction made during human re-audit and adjudication, with old value, new value, and the reason, usually a quotation and page. 177 entries. |
| `validation_blinded_annotation.csv` | The second annotator's independent classifications of 54 arms, produced blind to the original labels, with their own extracted values and supporting quotations. |
| `validation_adjudication.csv` | Original label, blinded label, and final adjudicated label for all 54 arms. |
| `reproduce_paper_numbers.py` | Recomputes the corpus-level results in the paper from `cardiac_organoid_arms.xlsx`. |
| `validation_v11/` | The v1.1 re-annotation of the same 54 arms by a new blinded annotator: raw annotations, the codebook as delivered, the frozen reference, and computed results. |
| `reproduce_validation_v11.py`, `tests/` | Recomputes the v1.1 agreement statistics from `validation_v11/`, with input checks. |

Source PDFs are not redistributed. Papers are identified by DOI in `included_papers.csv`.

## Reproducing the paper's numbers

```
pip install openpyxl numpy
python reproduce_paper_numbers.py
```

This prints the comparability funnel, the method-specific sub-pools, Table 2, the eligible-construct
split, the reporting gap, the by-year reporting completeness, and the deposition count. The values
match those reported in the paper.

## Validation status

The comparability labels are one curator's determinations, adjudicated against one blinded second
annotator over 54 arms: the 40 then passing the gate, plus a stratified sample of excluded arms, two
per failure code.

- Exact agreement on the primary classification: 65 percent (35 of 54)
- Agreement on the binary comparable or not-comparable decision: 72 percent (39 of 54)
- Adjudication removed 11 arms and added 2, revising the count from 40 to 31

These statistics characterize the original v1.0 evaluation. Its disagreements informed v1.1.

A new blinded annotator with relevant biomedical training, uninvolved in codebook revision,
subsequently applied the delivered v1.1 to the same 54 arms. Against the frozen adjudicated
reference from commit `06c9d6de28c81a9b83bcab3f1706d71bba735f20`, exact primary-label agreement
was 47/54 (87.0%; Cohen's kappa 0.8120) and binary eligibility agreement was 48/54
(88.9%; kappa 0.7802), with no unclassified arms. This was a new-rater, same-sample
evaluation, not a held-out evaluation on unseen arms. Keep these results separate from v1.0.

These agreement statistics are comparisons against the pre-correction reference. One correction
was applied to the corpus afterwards: the Silver 2023 doxorubicin arm `P57_SILVER_2023_2` moved from
`no value reported` to `toxicant dosed` (see `correction_log.csv`). The raw v1.1 annotations, the
codebook as delivered, and the frozen reference are in `validation_v11/`; run
`python reproduce_validation_v11.py` to recompute the statistics. `comparability_codebook_v1.1.1.md`
is a post-evaluation clarification (derived pan-CM totals) and has not been independently evaluated.

The labels should be treated as provisional and inspectable rather than settled.

## Scope of the comparability verdict

Passing the gate means an arm reports a genuine cardiomyocyte differentiation yield, by an eligible
cell-fraction method, in a construct where the cardiomyocytes differentiated in place.

It does not mean two such values may be pooled. A cardiomyocyte fraction is a ratio, so direct
comparison also requires a matched denominator: the same measurement method, dissociation, gating
strategy, marker definition, cell line, and collection day. The 31 passing arms form method- and
condition-specific sub-pools. The largest single-method pool is 17 flow-cytometry arms from 11
papers.

## How the resource was built

Targeted collection rather than a systematic review. Each paper was then extracted by a large
language model working from a fixed schema, with a supporting quotation required for each
cardiomyocyte fraction. A separate automated pass re-read each source and checked the record against
its quoted evidence. Seven core papers were re-audited field by field by a human reader. The
comparability set was then annotated by a blinded second annotator and adjudicated. The frozen gate
was applied last.

Extraction and automated checking used the same model family, so that pass is quality control rather
than independent validation. The blinded human annotation provides the independent reliability
estimate. Corrections from every stage are in `correction_log.csv`.
