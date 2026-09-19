import csv
import importlib.util
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('validation', ROOT / 'reproduce_validation_v11.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.ref = v.read_unique(v.INPUTS / 'frozen_reference.csv')
        self.ann = v.read_unique(v.INPUTS / 'blinded_annotation.csv')

    def test_frozen_inputs_and_results(self):
        v.verify_manifest()
        result, rows = v.evaluate(self.ref, self.ann)
        self.assertEqual(result['primary_label']['matches'], 47)
        self.assertEqual(result['binary_eligibility']['matches'], 48)
        self.assertEqual(sum(not r['exact_agreement'] for r in rows), 7)
        self.assertAlmostEqual(result['primary_label']['kappa'], .8120338140228741)
        self.assertAlmostEqual(result['binary_eligibility']['kappa'], .7801899592944367)

    def test_exact_uses_reason_not_binary_classification(self):
        ref = deepcopy(self.ref)
        for row in ref.values():
            row['final_classification'] = 'deliberately_unusable_binary_column'
        result, _ = v.evaluate(ref, self.ann)
        self.assertEqual(result['primary_label']['matches'], 47)

    def test_missing_arm_rejected(self):
        self.ann.pop(next(iter(self.ann)))
        with self.assertRaises(ValueError):
            v.evaluate(self.ref, self.ann)

    def test_invalid_label_rejected(self):
        self.ann[next(iter(self.ann))][v.LABEL_COLUMN] = 'invented'
        with self.assertRaises(ValueError):
            v.evaluate(self.ref, self.ann)

    def test_duplicate_arm_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'duplicate.csv'
            p.write_text('arm_id,label\na,x\na,y\n', encoding='utf-8')
            with self.assertRaises(ValueError):
                v.read_unique(p)

    def test_degenerate_kappa_is_unavailable(self):
        self.assertIsNone(v.agreement(['x'], ['x'])['kappa'])


if __name__ == '__main__':
    unittest.main()
