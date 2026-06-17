"""Stage 4 of the pipeline: export trained model to ONNX for cloud GPU serving."""
from __future__ import annotations

from pathlib import Path

from anomalib.deploy import ExportType
from anomalib.engine import Engine
from anomalib.models import Patchcore

from stonescan_ml.config import Config
from stonescan_ml.utils.logging import get_logger

log = get_logger("export")


def main() -> None:
    cfg = Config.load()
    ckpt_dir = Path("models/checkpoints") / cfg.train.model / cfg.data.category
    ckpts = list(ckpt_dir.rglob("*.ckpt"))
    if not ckpts:
        raise FileNotFoundError(f"no checkpoint under {ckpt_dir}")
    ckpt = max(ckpts, key=lambda p: p.stat().st_mtime)

    serving_dir = Path("serving") / cfg.train.model / cfg.data.category
    serving_dir.mkdir(parents=True, exist_ok=True)

    model = Patchcore.load_from_checkpoint(str(ckpt))
    engine = Engine()

    for fmt in cfg.export.formats:
        log.info("Exporting %s → %s", fmt, serving_dir)
        if fmt == "onnx":
            engine.export(
                model=model,
                export_type=ExportType.ONNX,
                export_root=str(serving_dir),
            )
        else:
            # TensorRT engine builds run as a separate CUDA post-step on a box
            # matching the serving GPU node, not here.
            log.warning("Skipping format handled outside this step: %s", fmt)


if __name__ == "__main__":
    main()
