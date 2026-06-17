"""Stage 3 of the pipeline: load checkpoint, compute clean metrics, dump report."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from anomalib.data import MVTecAD
from anomalib.engine import Engine
from anomalib.models import Patchcore
from torchvision.transforms.v2 import Compose, Resize

from stonescan_ml.config import Config
from stonescan_ml.evaluation.metrics import compute_image_report
from stonescan_ml.utils.logging import get_logger

log = get_logger("evaluate")


def main() -> None:
    cfg = Config.load()
    ckpt_dir = Path("models/checkpoints") / cfg.train.model / cfg.data.category
    ckpts = list(ckpt_dir.rglob("*.ckpt"))
    if not ckpts:
        raise FileNotFoundError(f"no checkpoint under {ckpt_dir}")
    ckpt = max(ckpts, key=lambda p: p.stat().st_mtime)
    log.info("Loading checkpoint: %s", ckpt)

    datamodule = MVTecAD(
        root=cfg.data.root,
        category=cfg.data.category,
        eval_batch_size=cfg.train.batch_size,
        num_workers=cfg.train.num_workers,
        augmentations=Compose([Resize((cfg.data.image_size, cfg.data.image_size), antialias=True)]),
        seed=cfg.train.seed,
    )
    model = Patchcore.load_from_checkpoint(str(ckpt))
    engine = Engine(accelerator=cfg.train.accelerator, devices=cfg.train.devices)

    predictions = engine.predict(model=model, datamodule=datamodule)

    scores: list[float] = []
    labels: list[int] = []
    for batch in predictions:
        scores.extend(batch["pred_scores"].cpu().numpy().tolist())
        labels.extend(batch["label"].cpu().numpy().astype(int).tolist())

    report = compute_image_report(np.asarray(scores), np.asarray(labels))
    out = Path("reports/eval_report.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report.to_dict(), indent=2))
    log.info("Eval report → %s", out)
    log.info(json.dumps(report.to_dict(), indent=2))


if __name__ == "__main__":
    main()
