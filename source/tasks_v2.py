"""Corrected, explicitly *synthetic* sequence-rule instrument (E16).

This is a new dataset/version; it does not change the historical T2/E0-E15 results.
Each input has six position-specific one-hots and a two-way rule cue.
Split by unique underlying sequence *before* creating either task, so no
sequence can be in training and held-out splits even across different rules.
"""

import numpy as np

ALPHABET = 8
LENGTH = 6
DIM = LENGTH * ALPHABET + 2
RULES = ("copy_first", "copy_last")


def make_stream(seed: int, n_sequences: int = 2048):
    """Return task -> split -> (X float32, y int64, sequences int8)."""
    if not 10 <= n_sequences <= ALPHABET ** LENGTH:
        raise ValueError("n_sequences must be between 10 and 8**6")
    rng = np.random.default_rng(seed + 16000)
    # Sampling without replacement guarantees disjoint inputs among splits.
    ids = rng.choice(ALPHABET ** LENGTH, n_sequences, replace=False)
    powers = ALPHABET ** np.arange(LENGTH - 1, -1, -1)
    seq = ((ids[:, None] // powers) % ALPHABET).astype(np.int8)
    x = np.zeros((n_sequences, DIM), dtype=np.float32)
    x[np.arange(n_sequences)[:, None],
      (np.arange(LENGTH)[None, :] * ALPHABET + seq)] = 1.0
    cuts = (int(.70 * n_sequences), int(.85 * n_sequences))
    splits = {"train": slice(0, cuts[0]),
              "val": slice(cuts[0], cuts[1]),
              "test": slice(cuts[1], None)}
    result = {}
    for rule_index, name in enumerate(RULES):
        x_task = x.copy()
        x_task[:, LENGTH * ALPHABET + rule_index] = 1.0
        labels = seq[:, 0 if rule_index == 0 else -1].astype(np.int64)
        result[name] = {split: (x_task[idx], labels[idx], seq[idx])
                        for split, idx in splits.items()}
    return result
