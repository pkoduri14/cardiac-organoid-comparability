"""Reproduce the original v1.1 evaluation, never using the revised corpus labels.

Python standard library only. Run from any directory:
    python reproduce_validation_v11.py
    python reproduce_validation_v11.py --output-dir validation_v11/results
The optional output directory contains derived results, never input annotations.
"""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUTS = HERE / "validation_v11"
LABEL_COLUMN = "your_classification (potentially_comparable OR failure code)"
REASON_TO_CODE = {
    "eligible yield": "potentially_comparable",
    "not primary": "not_primary",
    "seeded input": "defined_input_ratio",
    "2D substrate": "substrate_2D_denominator",
    "alternate lineage": "alternate_lineage",
    "subtype spec": "regional_identity_spec",
    "disease model": "disease_or_KO",
    "toxicant dosed": "toxicant_perturbation",
    "no value reported": "no_value_reported",
}


def read_unique(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    ids = [r["arm_id"] for r in rows]
    if any(not key for key in ids) or len(set(ids)) != len(ids):
        raise ValueError(f"Missing or duplicate arm identifier: {path.name}")
    return {r["arm_id"]: r for r in rows}


def agreement(a, b):
    if not a or len(a) != len(b):
        raise ValueError("Agreement requires two nonempty, equally sized label lists")
    n = len(a)
    ca, cb = Counter(a), Counter(b)
    labels = sorted(set(a) | set(b), key=str)
    matches = sum(x == y for x, y in zip(a, b))
    marginal = sum(ca[k] * cb[k] for k in labels)
    denominator = n * n - marginal
    kappa = (n * matches - marginal) / denominator if denominator else None
    matrix = [[sum(x == i and y == j for x, y in zip(a, b)) for j in labels] for i in labels]
    return {"n": n, "matches": matches, "agreement": matches / n, "kappa": kappa,
            "labels": labels, "confusion_matrix_rows_reference": matrix}


def evaluate(reference, annotation):
    if set(reference) != set(annotation):
        raise ValueError("Reference and annotation must contain exactly the same arm IDs")
    comparisons = []
    for arm_id, row in reference.items():
        # final_classification is binary. Exact agreement requires final_reason.
        expected = REASON_TO_CODE[row["final_reason"]]
        observed = annotation[arm_id][LABEL_COLUMN]
        if observed not in REASON_TO_CODE.values():
            raise ValueError(f"Unclassified or invalid original label for {arm_id}: {observed!r}")
        comparisons.append({"arm_id": arm_id, "frozen_reference_label": expected,
                            "original_v11_annotator_label": observed,
                            "exact_agreement": expected == observed,
                            "binary_agreement": (expected == "potentially_comparable") == (observed == "potentially_comparable")})
    a = [r["frozen_reference_label"] for r in comparisons]
    b = [r["original_v11_annotator_label"] for r in comparisons]
    return {"comparison": "Original delivered-v1.1 annotations versus frozen pre-correction reference",
            "reference_commit": "06c9d6de28c81a9b83bcab3f1706d71bba735f20",
            "primary_label": agreement(a, b),
            "binary_eligibility": agreement([x == "potentially_comparable" for x in a],
                                             [x == "potentially_comparable" for x in b]),
            "unclassified_count": 0,
            "same_arms_as_v10": True,
            "v111_followup_results": None,
            "note": "These statistics are not post-adjudication scores or validation of revised v1.1.1 rules."}, comparisons


def verify_manifest():
    manifest = json.loads((INPUTS / "manifest.json").read_text(encoding="utf-8"))
    for row in manifest["frozen_files"]:
        path = INPUTS / row["name"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != row["sha256"]:
            raise ValueError(f"Frozen input changed: {row['name']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    verify_manifest()
    result, comparisons = evaluate(read_unique(INPUTS / "frozen_reference.csv"),
                                   read_unique(INPUTS / "blinded_annotation.csv"))
    assert result["primary_label"]["n"] == 54
    assert result["primary_label"]["matches"] == 47
    assert result["binary_eligibility"]["matches"] == 48
    assert abs(result["primary_label"]["kappa"] - 0.8120338140228741) < 1e-12
    assert abs(result["binary_eligibility"]["kappa"] - 0.7801899592944367) < 1e-12
    if args.output_dir:
        out = args.output_dir.resolve()
        if out == INPUTS.resolve():
            raise ValueError("Use a results subdirectory, not the frozen-input directory")
        out.mkdir(parents=True, exist_ok=True)
        (out / "original_results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        with (out / "comparisons.csv").open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(comparisons[0]))
            writer.writeheader()
            writer.writerows(comparisons)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
