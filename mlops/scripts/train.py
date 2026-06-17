"""Stage 2 of the pipeline: train the anomaly model."""
from __future__ import annotations

import json
from pathlib import Path

from stonescan_ml.config import Config
from stonescan_ml.training.anomaly import train_patchcore
from stonescan_ml.utils.logging import get_logger

log = get_logger("train")


def main() -> None:
    cfg = Config.load()
    output_dir = Path("models/checkpoints") / cfg.train.model / cfg.data.category
    result = train_patchcore(cfg, output_dir)

    metrics_path = Path("reports/train_metrics.json")
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.write_text(json.dumps(result["metrics"], indent=2))
    log.info("Wrote %s", metrics_path)


if __name__ == "__main__":
    main()
