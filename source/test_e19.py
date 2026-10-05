"""E19 leakage, route and causal-control smoke tests."""
import copy
import unittest
from pathlib import Path

import numpy as np
import torch
from torch import nn

from run_e19 import (Adapter, DIM, choose_feedback, normal, pick,
                     read_corpus, to_tensors)
from sklearn.feature_extraction.text import HashingVectorizer


class E19Tests(unittest.TestCase):
    def test_corpus_hash_counts_and_disjoint_splits(self):
        data = Path("C:/Users/Majied/.kr8/.scratch/new-ai-e19")
        if not data.exists():
            self.skipTest("Pinned AG News corpus not downloaded; pass the --data-dir to runner")
        train, test, cleaning = read_corpus(data)
        self.assertEqual(cleaning["train_test_collision_rows"], 10)
        self.assertEqual(cleaning["train_internal_duplicate_rows"], 151)
        for seed in (31, 37, 41, 43, 47):
            split = pick(train, test, seed)
            seen = [normal(row["text"]) for key in ("a_train", "a_val", "b_train", "b_val")
                    for row in split[key]]
            self.assertEqual(len(seen), len(set(seen)))
            self.assertFalse(set(seen) & {normal(row["text"]) for row in test})
            self.assertEqual(len(split["b_pool"]), 512)
            self.assertTrue(set(normal(row["text"]) for row in split["b_pool"]) <= set(seen))
            self.assertEqual(len(split["a_train"]), 1600)
            self.assertEqual(len(split["a_val"]), 400)
            self.assertEqual(len(split["a_test"]), 3800)
            self.assertEqual(len(split["b_test"]), 3800)

    def test_adapter_initially_exactly_preserves_base_and_freezes_it(self):
        torch.manual_seed(3)
        x = torch.rand(8, DIM)
        base = nn.Linear(DIM, 2)
        adapter = Adapter(copy.deepcopy(base), x[:4], x[4:])
        self.assertTrue(torch.equal(base(x), adapter(x)))
        self.assertFalse(any(p.requires_grad for p in adapter.base.parameters()))
        self.assertTrue(adapter.delta.weight.requires_grad)
        self.assertEqual(adapter.route(x).shape, (8, 1))

    def test_alarm_is_only_post_label_and_uses_old_validation(self):
        self.assertEqual(choose_feedback([1, 2, 3], [3, 3, 4]), (3, 3))
        self.assertEqual(choose_feedback([1, 2, 3], [0, 1, 2]), (None, 3))
        self.assertEqual(choose_feedback([1, 2, 3], [4, 0, 0]), (1, 3))

    def test_real_text_features_not_phase_cues(self):
        vec = HashingVectorizer(n_features=DIM, ngram_range=(1, 2),
                                alternate_sign=False, norm="l2")
        a = [{"text": "Sports match", "label": 1}]
        b = [{"text": "Sports match", "label": 3}]
        x, y = to_tensors(a, vec, torch.device("cpu"))
        bx, by = to_tensors(b, vec, torch.device("cpu"))
        self.assertTrue(torch.equal(x, bx))
        self.assertEqual(int(y[0]), int(by[0]))
        self.assertEqual(np.count_nonzero(x.numpy()), 3)


if __name__ == "__main__":
    unittest.main()
