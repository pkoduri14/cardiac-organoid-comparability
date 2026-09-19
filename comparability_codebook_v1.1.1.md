# Cardiac-Organoid Comparability Codebook

**Version:** 1.1.1

**Release status:** Post-evaluation clarification of v1.1. The v1.1 human evaluation used the earlier codebook.

## 0. Purpose and terminology

For each protocol arm (one construct and experimental condition within a paper), determine whether its cardiomyocyte (CM) fraction is potentially comparable and otherwise assign one primary failure code.

Passing establishes minimum eligibility, not pairwise equivalence or poolability. Subsequent comparisons must match biological context, measurement method, denominator, markers, cell line, collection day, dissociation and gating procedures.

## 1. Gate

An arm is potentially comparable only when all five conditions hold.

1. **Primary experiment.** The paper reports a primary experimental result, not a review, protocol-only description or meta-analysis.
2. **Construct in scope.** A self-organizing organoid or reaggregation microtissue in which the CM population differentiates in place. Assembly from predifferentiated CMs does not satisfy this condition.
3. **Outcome role is a yield.** The CM fraction is a differentiation outcome, not a seeded composition, disease or genetic readout, toxicant response, subtype-only result or alternate-lineage result. A relative change, fold change or fraction within CMs is not an absolute pan-CM fraction.
4. **Numerical CM fraction available.** Accept a directly reported pan-CM fraction or a derived total meeting every condition in Section 4. Do not substitute a partial sum of CM subtypes.
5. **Method measures a cell fraction.** Eligible methods include flow cytometry, single-cell/single-nucleus RNA cluster proportions, lineage-reporter percentages and quantitative whole-construct immunofluorescence cell counting. Image area and other non-cell denominators do not qualify. A sequencing-derived fraction describes the sampled, quality-controlled cells, not necessarily every cell in an intact organoid.

Apply the primary-code priority below when a gate fails. If source access or unresolved contradictory evidence prevents a decision, record an unclassified decision with the specific reason. Do not invent a failure code for uncertainty.

## 2. Failure codes

| Code | Definition | Resource label |
|---|---|---|
| `potentially_comparable` | All five gates satisfied. | `eligible yield` |
| `not_primary` | Review, protocol-only description or meta-analysis with no primary experimental arm. | `not primary` |
| `defined_input_ratio` | CMs are seeded inputs, including constructs assembled from predifferentiated CMs, whether or not a fixed mixing ratio is imposed. | `seeded input` |
| `substrate_2D_denominator` | A 2D, micropatterned or substrate-attached construct, or a non-cell denominator such as image area. | `2D substrate` |
| `alternate_lineage` | The condition targets a non-CM lineage; CM is not the intended output. | `alternate lineage` |
| `regional_identity_spec` | The available fraction is subtype-only, not a pan-CM fraction. A derived total satisfying Section 4 is not excluded merely because its components are subtypes. A pan-CM measurement under a subtype-directed protocol remains a pan-CM measurement. | `subtype spec` |
| `disease_or_KO` | Disease model, genetic knockout, or disease perturbation arm in which the reported fraction is the disease effect rather than a protocol yield. | `disease model` |
| `toxicant_perturbation` | An agent is dosed specifically to abolish or distort cardiac differentiation. A control arm does not waive this code. | `toxicant dosed` |
| `no_value_reported` | Eligible construct and compatible outcome role, but no numerical CM fraction in the inspected source materials. Unavailable supplements are not evidence that no value exists. Absence of a reported value does not establish that no measurement was performed. | `no value reported` |

## 3. Primary-code priority

Take the first applicable code, not whichever gives better agreement with another annotation:

1. `not_primary`
2. `defined_input_ratio`
3. `substrate_2D_denominator`
4. `alternate_lineage`
5. `regional_identity_spec`
6. `disease_or_KO`
7. `toxicant_perturbation`
8. `no_value_reported`

Unclassified is a missing decision, not a ninth failure code. Record its count separately.

## 4. Derived pan-CM fractions

An arithmetic sum of reported CM subpopulations can satisfy the numerical and pan-CM requirements only when the source supports all of the following:

1. **CM identity and completeness.** The included categories cover all source-identified CM populations in the assayed sample. Inspect the full cell-category annotation and relevant evidence; atrial plus ventricular is not automatically exhaustive. Do not add an ambiguous population merely because its name suggests cardiac conduction, or omit another CM population to preserve a preferred value.
2. **No overlap.** Categories are mutually exclusive. Overlapping marker-positive fractions cannot be added without supported overlap correction.
3. **Shared whole-sample denominator.** Each component is a fraction of the same sampled cell population, including non-CMs, rather than of CMs alone or of separately enriched populations. Do not combine incompatible denominators.
4. **Same arm and time point.** Components belong to the same condition, assay/sample and collection time. Do not mix time points, treatment conditions or separately summarized samples.
5. **Traceable calculation.** Preserve each component label and value, the addition, source DOI, page/figure/table, denominator, CM measurement day and a `derived` flag. Use reported precision; rounded component percentages yield an approximate derived total. Do not normalize a non-closing composition to 100% or digitize an unreported value without a separately documented method.

Record whether each condition is supported, contradicted or unresolved. If only a partial CM subtype fraction is established, use `regional_identity_spec`, subject to the priority order. If the necessary evidence is inaccessible or contradictory, leave the decision unclassified pending resolution rather than claiming a verified total. Other gates still apply even when the arithmetic is valid.

Example: source-defined disjoint CM categories representing 20% and 30% of the same whole-cell sample give an approximate derived CM fraction of 50%, but only if those categories cover all source-identified CMs. This is not equivalent to adding two percentages each calculated within the CM subset.

## 5. Annotation and provenance

1. Work independently from the paper and supplied supplements. Treat navigation hints as aids, not evidence.
2. Record value, method, construct, supporting quotation, location and notes. Distinguish quoted source text from the curator's calculation or interpretation.
3. Record the measurement-specific day, population and denominator. A general organoid culture day may differ from the day used for sequencing or another assay.
4. For a derived value, complete the Section 4 evidence record.
5. Apply all gates and the primary-code priority. Record missing source access and unresolved evidence explicitly.
6. During blinded evaluation, do not consult reference labels, other annotators' decisions or automated classifications.

## 6. Version and evaluation boundaries

This revision explicitly permits evidence-supported derived totals and clarifies source-access uncertainty. It was written after the v1.1 evaluation and has not been independently evaluated.

Preserve the original v1.1 packet, raw annotations and frozen reference. Its agreement statistics remain historical comparisons against that reference. Subsequent adjudication or follow-up annotation must be recorded separately, with rule version, source packet, date and any repeated-arm selection disclosed. Do not describe automated source checking or curator adjudication as a new blinded human evaluation.
