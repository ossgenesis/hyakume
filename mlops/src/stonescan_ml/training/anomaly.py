"""Anomalib PatchCore training, wrapped to log to MLflow.

Why this thin wrapper instead of `anomalib train` CLI directly:
  - We control the config object (typed), so notebooks and scripts share it.
  - We choose what gets logged to MLflow (params, metrics, model, sample
    visualizations) so runs are comparable across months.
  - The same function is callable from scripts/train.py AND from tests AND
    from a future Airflow/Prefect task.
"""
from __future__ import annotations

from pathlib import Path

import mlflow
from anomalib.data import MVTecAD
from anomalib.engine import Engine
from anomalib.models import Patchcore
from torchvision.transforms.v2 import Compose, Resize

from stonescan_ml.config import Config
from stonescan_ml.utils.logging import get_logger
from stonescan_ml.utils.seed import seed_everything

log = get_logger(__name__)


def _resize(image_size: int) -> Compose:
    return Compose([Resize((image_size, image_size), antialias=True)])


def train_patchcore(cfg: Config, output_dir: Path) -> dict:
    """Train PatchCore on MVTec AD, log to MLflow, return metrics dict."""
    seed_everything(cfg.train.seed)
    output_dir.mkdir(parents=True, exist_ok=True)

    datamodule = MVTecAD(
        root=cfg.data.root,
        category=cfg.data.category,
        train_batch_size=cfg.train.batch_size,
        eval_batch_size=cfg.train.batch_size,
        num_workers=cfg.train.num_workers,
        augmentations=_resize(cfg.data.image_size),
        seed=cfg.train.seed,
    )

    model = Patchcore(
        backbone=cfg.train.backbone,
        layers=cfg.train.layers,
        coreset_sampling_ratio=cfg.train.coreset_sampling_ratio,
        num_neighbors=cfg.train.num_neighbors,
    )

    engine = Engine(
        max_epochs=cfg.train.max_epochs,
        accelerator=cfg.train.accelerator,
        devices=cfg.train.devices,
        default_root_dir=str(output_dir),
    )

    mlflow.set_experiment(f"stonescan-{cfg.train.model}")
    with mlflow.start_run() as run:
        mlflow.log_params({
            "model": cfg.train.model,
            "backbone": cfg.train.backbone,
            "category": cfg.data.category,
            "image_size": cfg.data.image_size,
            "batch_size": cfg.train.batch_size,
            "coreset_ratio": cfg.train.coreset_sampling_ratio,
            "seed": cfg.train.seed,
        })

        log.info("Fitting PatchCore on category=%s", cfg.data.category)
        engine.fit(model=model, datamodule=datamodule)

        log.info("Running test set evaluation")
        test_results = engine.test(model=model, datamodule=datamodule)
        metrics = test_results[0] if test_results else {}
        for k, v in metrics.items():
            if isinstance(v, (int, float)):
                mlflow.log_metric(k, float(v))

        ckpt_path = output_dir / "weights" / "lightning" / "model.ckpt"
        if ckpt_path.exists():
            mlflow.log_artifact(str(ckpt_path), artifact_path="model")

        log.info("MLflow run: %s", run.info.run_id)
        return {"run_id": run.info.run_id, "metrics": metrics}
