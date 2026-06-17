"""Typed configuration loaded from params.yaml.

Validating config at startup catches typos (`bacth_size`) before a 4-hour
training run, and gives every downstream function a stable, autocompletable
shape instead of `dict[str, Any]`.
"""
from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field


class DataConfig(BaseModel):
    source: Literal["mvtec_ad", "marble_mcs", "local"] = "mvtec_ad"
    category: str = "capsule"
    hf_repo: str | None = None
    hf_archive: str | None = None
    root: Path
    image_size: int = Field(256, ge=64, le=1024)


class TrainConfig(BaseModel):
    model: Literal["patchcore", "efficient_ad", "padim"] = "patchcore"
    backbone: str = "wide_resnet50_2"
    layers: list[str] = ["layer2", "layer3"]
    coreset_sampling_ratio: float = Field(0.1, gt=0, le=1)
    num_neighbors: int = Field(9, ge=1)
    max_epochs: int = Field(1, ge=1)
    batch_size: int = Field(32, ge=1)
    num_workers: int = Field(4, ge=0)
    seed: int = 1337
    accelerator: Literal["auto", "cpu", "gpu", "mps"] = "auto"
    devices: int | str = 1


class EvaluateConfig(BaseModel):
    metrics: list[str]
    num_visualization_samples: int = 8
    threshold_method: Literal["adaptive", "manual"] = "adaptive"


class ExportConfig(BaseModel):
    formats: list[Literal["onnx", "tensorrt"]]
    opset: int = 17
    dynamic_axes: bool = True


class Config(BaseModel):
    data: DataConfig
    train: TrainConfig
    evaluate: EvaluateConfig
    export: ExportConfig

    @classmethod
    def load(cls, path: Path | str = "params.yaml") -> "Config":
        with open(path) as f:
            raw = yaml.safe_load(f)
        return cls(**raw)
