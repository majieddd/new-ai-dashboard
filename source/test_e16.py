"""E16 data and mechanism invariants; run with unittest discover."""
import unittest

import numpy as np
import torch

from tasks_v2 import ALPHABET, DIM, LENGTH, RULES, make_stream
from run_e16 import Base, TaskAdapter, evaluate


class TaskV2Tests(unittest.TestCase):
    def test_reproducible_and_oracle(self):
        for seed in (1, 7, 42, 123, 999):
            a, b = make_stream(seed), make_stream(seed)
            for rule in RULES:
                for split in ("train", "val", "test"):
                    X, y, seq = a[rule][split]
                    self.assertTrue(np.array_equal(X, b[rule][split][0]))
                    self.assertEqual(X.shape[1], DIM)
                    self.assertEqual(X.dtype, np.float32)
                    self.assertEqual(y.dtype, np.int64)
                    self.assertTrue(np.all((X[:, :48].reshape(-1, LENGTH, ALPHABET).sum(-1)) == 1))
                    self.assertTrue(np.all(X[:, -2:].sum(-1) == 1))
                    self.assertTrue(np.array_equal(X[:, :48].reshape(-1, LENGTH, ALPHABET).argmax(-1), seq))
                    oracle = seq[:, 0 if rule == "copy_first" else -1]
                    self.assertTrue(np.array_equal(y, oracle))
                    self.assertEqual(len(np.unique(y)), ALPHABET)
                pools = [{tuple(s) for s in a[rule][split][2]} for split in ("train", "val", "test")]
                for i in range(3):
                    for j in range(i + 1, 3):
                        self.assertFalse(pools[i] & pools[j])
            # Same sequence partition across rules prevents cross-task leakage.
            for split in ("train", "val", "test"):
                self.assertTrue(np.array_equal(a[RULES[0]][split][2], a[RULES[1]][split][2]))

    def test_zero_adapter_identity_and_task_isolation(self):
        base = Base()
        model = TaskAdapter(base)
        a = make_stream(7)
        old = torch.from_numpy(a[RULES[0]]["test"][0])
        new = torch.from_numpy(a[RULES[1]]["test"][0])
        with torch.no_grad():
            self.assertTrue(torch.equal(model(old), base(old)))
            self.assertTrue(torch.equal(model(new), base(new)))
            model.adapter.weight.fill_(0.5)
            self.assertTrue(torch.equal(model(old), base(old)))

    def test_cpu_pilot_no_test_tuning_and_counts(self):
        row = evaluate(7, torch.device("cpu"), old_steps=2, new_steps=2)
        self.assertEqual(set(row["arms"]), {"frozen", "full_finetune", "scheduled_adapter"})
        self.assertEqual(row["arms"]["scheduled_adapter"]["old_test"], row["before"]["old_test"])
        self.assertGreater(row["arms"]["scheduled_adapter"]["total_params"],
                           row["arms"]["full_finetune"]["total_params"])
        self.assertGreater(row["split_sizes"]["train"], row["split_sizes"]["test"])


if __name__ == "__main__":
    unittest.main()
