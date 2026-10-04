"""Invariant tests for E18 (run before any result interpretation)."""
import hashlib
import unittest

import numpy as np

from run_e18 import ALPHABET, LENGTH, auc, blocks, encode, input_nll, make_data


class E18Tests(unittest.TestCase):
    def test_split_separation_and_rule_shift_pairs(self):
        for seed in (31, 37, 41, 43, 47):
            data = make_data(seed, 64, 32, 32)
            old = np.concatenate([data[k] for k in ("train", "val", "test")])
            self.assertEqual(len({tuple(r) for r in old}), len(old))
            self.assertTrue(np.all(old[:, 0] < 4))
            self.assertTrue(np.all(data["nuisance"][:, 0] >= 4))
            # Changed oracle targets on exactly the same encoded, held-out X.
            old_x = encode(data["test"])
            concept_x = encode(data["test"])
            self.assertEqual(hashlib.sha256(old_x.tobytes()).digest(),
                             hashlib.sha256(concept_x.tobytes()).digest())
            self.assertGreater(np.mean(data["test"][:, 0] != data["test"][:, -1]), .5)

    def test_encoder_positional_and_nuisance_nll(self):
        data = make_data(31, 64, 32, 32)
        x = encode(data["test"])
        self.assertEqual(x.shape, (32, LENGTH * ALPHABET))
        self.assertTrue(np.all(x.reshape(32, LENGTH, ALPHABET).sum(axis=2) == 1))
        old = input_nll(data["train"], data["test"])
        nuisance = input_nll(data["train"], data["nuisance"])
        self.assertEqual(auc(old, old.copy()), .5)
        self.assertGreater(auc(old, nuisance), .9)

    def test_auc_ties_and_block_delays(self):
        self.assertEqual(auc([1, 2], [1, 2]), .5)
        self.assertEqual(auc([1, 2], [3, 4]), 1.0)
        self.assertEqual(auc([3, 4], [1, 2]), 0.0)
        self.assertEqual(blocks(np.array([False] * 31 + [True]), 32).tolist(), [1])
        with self.assertRaises(ValueError):
            blocks(np.array([False] * 31), 32)


if __name__ == "__main__":
    unittest.main()
