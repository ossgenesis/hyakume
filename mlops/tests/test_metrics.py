import numpy as np
import pytest

from stonescan_ml.evaluation.metrics import best_f1, compute_image_report


def test_perfect_separation_gives_auroc_1():
    scores = np.array([0.1, 0.2, 0.8, 0.9])
    labels = np.array([0, 0, 1, 1])
    r = compute_image_report(scores, labels)
    assert r.image_auroc == pytest.approx(1.0)
    assert r.image_ap == pytest.approx(1.0)
    assert r.image_f1_best == pytest.approx(1.0)


def test_inverted_scores_give_auroc_0():
    scores = np.array([0.9, 0.8, 0.2, 0.1])
    labels = np.array([0, 0, 1, 1])
    r = compute_image_report(scores, labels)
    assert r.image_auroc == pytest.approx(0.0)


def test_best_f1_threshold_falls_in_valid_range():
    scores = np.array([0.05, 0.15, 0.45, 0.55, 0.85])
    labels = np.array([0,    0,    1,    1,    1])
    f1, thr = best_f1(scores, labels)
    assert 0 <= f1 <= 1
    assert scores.min() <= thr <= scores.max()


def test_shape_mismatch_rejected():
    with pytest.raises(ValueError):
        compute_image_report(np.zeros(3), np.zeros(4))


def test_non_binary_labels_rejected():
    with pytest.raises(ValueError):
        compute_image_report(np.array([0.1, 0.9]), np.array([0, 2]))
