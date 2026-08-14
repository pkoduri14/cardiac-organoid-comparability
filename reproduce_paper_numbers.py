"""
Recomputes the corpus-level results in the paper from cardiac_organoid_arms.xlsx.
Run: python reproduce_paper_numbers.py   (requires openpyxl, numpy)
Prints the funnel, method sub-pools, Table 2, the eligible-construct split,
the reporting gap, by-year completeness, and the deposition count. Validation
transitions and corpus exclusions are recorded in the validation CSVs instead.
"""
import os, re
import numpy as np
import openpyxl
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(HERE, 'cardiac_organoid_arms.xlsx')

# Gate vocabulary, mirrored from comparability_codebook_v1.1.md; edit both together.
YIELD_METHODS = {'flow', 'flow_alphaactinin', 'scrna_cluster', 'scrna-seq',
                 'reporter_gfp', 'if_tnnt2_confocal', 'immunofluorescence'}
ELIGIBLE = {'self_organizing_organoid', 'reaggregation_microtissue'}
DESIGN_REASONS = {'disease model', 'toxicant dosed', 'subtype spec',
                  'alternate lineage', 'not primary', 'seeded input'}


# A field counts as absent under any of the placeholder spellings used during extraction.
def missing(x):
    return str(x).strip().upper() in ('NR', 'NAN', '', 'NONE', 'NOT_REPORTED', 'NA')


# Values may be ranges or carry symbols, so parse to the mean of the numbers present.
def num(x):
    if missing(x):
        return np.nan
    found = re.findall(r'[0-9]+\.?[0-9]*', str(x))
    return np.mean([float(t) for t in found]) if found else np.nan


# Arm identifiers are prefixed with the paper key, so the prefix groups arms by paper.
def paper_of(arm_id):
    m = re.match(r'(P\d+)', str(arm_id))
    return m.group(1) if m else str(arm_id)


# Load the resource and address columns by name rather than position.
rows = list(openpyxl.load_workbook(XLSX, data_only=True).active.iter_rows(values_only=True))
H = list(rows[0])
col = lambda name: H.index(name)
arms = rows[1:]
N = len(arms)

# Each successive slice adds one gate requirement, giving the funnel stages.
reported = [r for r in arms if not np.isnan(num(r[col('cm_fraction_pct')]))]
by_yield = [r for r in reported if str(r[col('cm_fraction_method')]).lower().strip() in YIELD_METHODS]
comparable = [r for r in arms if r[col('construct_comparability')] == 1]

# Arms in an eligible construct split into those blocked by design and those blocked by reporting.
eligible = [r for r in arms if str(r[col('model_class')]).strip() in ELIGIBLE]
elig_fail = [r for r in eligible if r[col('construct_comparability')] != 1]
by_design = [r for r in elig_fail if r[col('comparability_reason')] in DESIGN_REASONS]
by_reporting = [r for r in elig_fail if r[col('comparability_reason')] not in DESIGN_REASONS]

pct = lambda k: 100.0 * k / N

print('COMPARABILITY FUNNEL (Figure 2; Findings, first paragraph)')
print('  protocol arms                     %d' % N)
print('  papers                            %d' % len({paper_of(r[col('paper_id')]) for r in arms}))
print('  report a CM fraction              %d (%.0f%%)' % (len(reported), pct(len(reported))))
print('  by an eligible method             %d (%.0f%%)' % (len(by_yield), pct(len(by_yield))))
print('  POTENTIALLY COMPARABLE            %d (%.0f%%) from %d papers'
      % (len(comparable), pct(len(comparable)), len({paper_of(r[col('paper_id')]) for r in comparable})))

# Passing arms only pool within a shared measurement method, so report the per-method breadth.
print('\nMETHOD-SPECIFIC SUB-POOLS (Findings, first paragraph)')
methods = Counter(str(r[col('cm_fraction_method')]).strip().lower() for r in comparable)
for meth, n in methods.most_common():
    papers = len({paper_of(r[col('paper_id')]) for r in comparable
                  if str(r[col('cm_fraction_method')]).strip().lower() == meth})
    print('  %-22s %2d arms from %d paper(s)' % (meth, n, papers))

# Codes are mutually exclusive, so the tally covers every arm exactly once.
print('\nTABLE 2  (primary reason for every arm)')
table = Counter(r[col('comparability_reason')] for r in arms)
for reason, n in table.most_common():
    print('  %-26s %3d' % (reason, n))
print('  %-26s %3d' % ('TOTAL', sum(table.values())))

print('\nELIGIBLE-CONSTRUCT SPLIT (Findings, second paragraph)')
print('  arms in an eligible construct     %d' % len(eligible))
print('    pass the gate                   %d' % len(comparable))
print('    fail                            %d' % len(elig_fail))
print('      by experimental role/design   %d' % len(by_design))
print('      by measurement/reporting      %d' % len(by_reporting))

# Upper bound assumes every reporting-blocked arm reports a valid cell fraction.
print('\nREPORTING GAP (Findings, third paragraph)')
ceiling = len(comparable) + len(by_reporting)
print('  recoverable arms                  %d' % len(by_reporting))
for reason, n in Counter(r[col('comparability_reason')] for r in by_reporting).most_common():
    print('    %-30s %d' % (reason, n))
print('  prospective upper bound           %d to %d of %d  (%.0f%% to %.0f%%)'
      % (len(comparable), ceiling, N, pct(len(comparable)), pct(ceiling)))
print('  held fixed (design/role)          %d' % len(by_design))

# The second column repeats the rate within eligible constructs to control for study mix.
print('\nREPORTING COMPLETENESS BY YEAR (Figure 3; Findings, fourth paragraph)')
print('  year   all arms        eligible constructs only')
for y in range(2017, 2027):
    ya = [r for r in arms if str(r[col('year')]).split('.')[0] == str(y)]
    if not ya:
        continue
    ra = sum(1 for r in ya if not np.isnan(num(r[col('cm_fraction_pct')])))
    ye = [r for r in eligible if str(r[col('year')]).split('.')[0] == str(y)]
    re_ = sum(1 for r in ye if not np.isnan(num(r[col('cm_fraction_pct')])))
    tail = '   %2d/%2d = %3.0f%%' % (re_, len(ye), 100.0 * re_ / len(ye)) if ye else ''
    print('  %d   %2d/%2d = %3.0f%%%s' % (y, ra, len(ya), 100.0 * ra / len(ya), tail))

# Accessions repeat across arms of the same paper, so count distinct values.
print('\nDEPOSITION (Findings, fifth paragraph)')
accessions = {str(r[col('geo_accession')]).strip() for r in arms if not missing(r[col('geo_accession')])}
print('  unique transcriptomic accessions  %d' % len(accessions))
