"""Pure-numpy metrics so eval doesn't depend on training framework state.

These wrap sklearn but with a stable, documented interface — the eval
harness, the CI gate check, and the production dashboard should all
compute "image AUROC" the same way.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.metrics import (
    average_precision_score,
    f1_score,
    precision_recall_curve,
    roc_auc_score,
)


@dataclass
class EvalReport:
    image_auroc: float
    image_ap: float
    image_f1_best: float
    image_f1_threshold: float
    pixel_auroc: float | None = None
    pixel_ap: float | None = None

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}


def best_f1(scores: np.ndarray, labels: np.ndarray) -> tuple[float, float]:
    """Sweep all thresholds; return (best_f1, threshold_at_best_f1)."""
    precision, recall, thresholds = precision_recall_curve(labels, scores)
    f1 = 2 * precision * recall / (precision + recall + 1e-12)
    idx = int(np.argmax(f1[:-1]))
    return float(f1[idx]), float(thresholds[idx])


def compute_image_report(
    scores: np.ndarray,
    labels: np.ndarray,
    pixel_scores: np.ndarray | None = None,
    pixel_labels: np.ndarray | None = None,
) -> EvalReport:
    if labels.ndim != 1 or scores.shape != labels.shape:
        raise ValueError("scores and labels must be 1-D and the same shape")
    if set(np.unique(labels).tolist()) - {0, 1}:
        raise ValueError("labels must be 0/1")

    img_auroc = float(roc_auc_score(labels, scores))
    img_ap    = float(average_precision_score(labels, scores))
    f1, thr   = best_f1(scores, labels)

    px_auroc = px_ap = None
    if pixel_scores is not None and pixel_labels is not None:
        ps = pixel_scores.ravel()
        pl = pixel_labels.ravel()
        px_auroc = float(roc_auc_score(pl, ps))
        px_ap    = float(average_precision_score(pl, ps))

    return EvalReport(img_auroc, img_ap, f1, thr, px_auroc, px_ap)
