from pathlib import Path

import pytest
from pydantic import ValidationError

from stonescan_ml.config import Config


def test_load_params_yaml():
    cfg = Config.load(Path(__file__).parents[1] / "params.yaml")
    assert cfg.data.image_size > 0
    assert cfg.train.coreset_sampling_ratio <= 1
    assert cfg.train.batch_size >= 1


def test_invalid_coreset_ratio_rejected(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text(
        "data: {source: mvtec_ad, category: tile, url: 'x', root: r, image_size: 256}\n"
        "train: {coreset_sampling_ratio: 5.0}\n"
        "evaluate: {metrics: []}\n"
        "export: {formats: [onnx]}\n"
    )
    with pytest.raises(ValidationError):
        Config.load(bad)
