# Cardiac-Organoid Comparability Codebook
**Version:** 1.1

## 0. Purpose and terminology

This codebook defines, for a single **protocol arm** (one construct and condition within a paper),
whether the reported cardiomyocyte (CM) fraction is **potentially comparable** across studies, and
if not, the single primary reason it is not.

The term is "potentially comparable," not "poolable." Passing the gate means an arm reports a
genuine CM differentiation *yield*, by an eligible method, in an eligible construct. It does not
establish that two such values may be pooled. A CM fraction is a ratio, so direct comparison also
requires a matched denominator: the same measurement method, dissociation, gating strategy, marker
definition, cell line, and collection day. Section 4 lists these. Potentially comparable arms
therefore form method- and condition-specific sub-pools.

## 1. Gate

An arm is **potentially comparable** if and only if all five conditions hold, evaluated in order.

1. **Primary experiment.** The paper reports a primary experimental result, not a review,
   protocol-only description, or meta-analysis.
2. **Construct in scope.** The construct is a self-organizing organoid or a reaggregation
   microtissue, meaning a 3D construct in which the CM population is differentiated in place.
3. **Outcome role is a yield.** The reported CM fraction is a differentiation outcome, not a seeded
   composition, a disease or genetic readout, a toxicant response, a regional-subtype result, or an
   alternate-lineage result.
4. **A numerical value is reported.**
5. **Method measures a cell fraction.** Flow cytometry, single-cell or single-nucleus RNA cluster
   proportion, a lineage-reporter percentage, or quantitative whole-construct immunofluorescence
   cell counting all qualify. Image area and other non-cell denominators do not.

Otherwise the arm is **not comparable** and receives exactly one primary failure code. Sections 2
and 3 define the codes and the order in which they are applied.

## 2. Failure codes

The `comparability_reason` column of the resource stores the label in the third column below.
Code and label are one to one; use this table to move between them.

| Code | Definition | Label in the resource |
|---|---|---|
| (gate passed) | The arm satisfies all five conditions in Section 1. | `eligible yield` |
| `not_primary` | Review, protocol-only, or meta-analysis; no primary experimental arm. | `not primary` |
| `defined_input_ratio` | CMs are a seeded input (engineered heart tissue, tri-lineage assembly, CM to non-CM mixing, or any construct assembled from cells differentiated before assembly). The fraction is an input, not a yield. | `seeded input` |
| `substrate_2D_denominator` | The denominator is not a count of cells. This covers 2D, micropatterned, and substrate-attached constructs, and also 3D constructs whose cardiomyocyte content is reported as an image-area percentage rather than a cell fraction. | `2D substrate` |
| `alternate_lineage` | The condition is intended to produce a non-CM lineage (epicardium or WT1+, endothelial or CD31+); CM is not the intended output. | `alternate lineage` |
| `regional_identity_spec` | The reported quantity is a CM subtype fraction (atrial, ventricular, sinoatrial, chamber or heart-field), not a pan-CM yield. | `subtype spec` |
| `disease_or_KO` | Disease model, genetic knockout, or disease perturbation arm in which the reported fraction is the disease effect rather than a protocol yield. | `disease model` |
| `toxicant_perturbation` | An agent is dosed specifically to abolish or distort cardiac differentiation. | `toxicant dosed` |
| `no_value_reported` | The arm is in an eligible construct and its purpose is compatible with reporting a yield, but no numerical CM fraction appears in the source. Added in v1.1. | `no value reported` |

## 3. Multiple codes and choosing the primary one

An arm may satisfy more than one code. Assign exactly one primary code by walking this fixed
priority order from top to bottom and taking the first that applies. The ordering is a tallying
convention that keeps counts reproducible. In every case the operative conclusion is the same: the
arm is not comparable.

1. `not_primary`
2. `defined_input_ratio`
3. `substrate_2D_denominator`
4. `alternate_lineage`
5. `regional_identity_spec`
6. `disease_or_KO`
7. `toxicant_perturbation`
8. `no_value_reported`

## 4. What is needed beyond construct and method

The gate certifies eligibility, not equivalence. When recording an arm, also capture the following.
These support downstream sub-pooling and are not inputs to the gate itself.

- Cell line and pluripotent source.
- Differentiation or collection day.
- Dissociation and gating: the marker used (cTnT/TNNT2, ACTN2, MYH) and the threshold.
- Whether the denominator is the whole construct or a dissociated single-cell suspension.

Two arms are directly poolable only if they share the measurement method and are comparable on these
dimensions.

## 5. Annotator procedure

Work from the full source PDF. Any page hint is a navigation aid only; verify the context yourself.
For each arm:

1. Independently locate and record the CM-fraction value and the method. Do not rely on a
   pre-recorded value.
2. Record your own supporting quotation and page. If the value cannot be located, record
   "not located."
3. Apply the gate in Section 1. If all five conditions hold, the arm is `potentially_comparable`.
4. Otherwise assign the single primary failure code using the order in Section 3.
5. Record any uncertainty in notes.

## 6. Revision history

**v1.0 to v1.1.** A blinded second annotator applied v1.0 to 54 arms. Exact agreement with the
original labels was 65 percent (35 of 54); agreement on the binary comparable or not-comparable
decision was 72 percent (39 of 54). Disagreements concentrated in three under-specified cases, each
now stated explicitly above.

1. **Constructs assembled from pre-differentiated cardiomyocytes.** v1.0 used the phrase
   "differentiated in place" without defining the boundary. v1.1 states in `defined_input_ratio`
   that any construct assembled from cells differentiated before assembly is a seeded input,
   whether or not a fixed ratio was imposed.
2. **Subtype against pan-CM readouts.** v1.0 did not say whether a marker combination denoting a
   subtype, such as SHOX2+cTnT+, counts as a subtype fraction. v1.1 states that
   `regional_identity_spec` turns on the reported quantity rather than the protocol's intent, so a
   pan-CM marker measured under a subtype-directed protocol is still a pan-CM yield.
3. **Arms reporting no value.** v1.0 had no code for an eligible-construct arm with no numerical
   fraction, so such arms matched nothing. v1.1 adds `no_value_reported`.

Agreement was measured while applying v1.0. The figure therefore characterizes that version rather
than the one released here, and it has not been re-measured on v1.1.
