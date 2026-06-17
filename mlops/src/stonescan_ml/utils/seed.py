"""Pin every RNG so two runs with the same code + data + params agree.

Without this, your "reproducible" eval still drifts by a few AUROC points
between runs because of CUDA non-determinism and dataloader shuffling.
"""
from __future__ import annotations

import os
import random

import numpy as np
import torch


def seed_everything(seed: int) -> None:
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
