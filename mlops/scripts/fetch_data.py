"""Stage 1: download dataset(s) into data/raw/.

Anomalib's bundled MVTec mirror is dead, so we pull a per-category archive
from a HuggingFace mirror and extract it into the layout Anomalib expects:
  <root>/<category>/{train,test,ground_truth}/...
After extraction, training-time `datamodule.prepare_data()` finds the data
and skips the download path.
"""
from __future__ import annotations

import shutil
import tarfile
from pathlib import Path

from huggingface_hub import hf_hub_download

from stonescan_ml.config import Config
from stonescan_ml.utils.logging import get_logger

log = get_logger("fetch")


def fetch_mvtec_from_hf(repo: str, archive: str, root: Path, category: str) -> Path:
    category_dir = root / category
    if category_dir.exists() and (category_dir / "train").exists():
        log.info("Already present: %s", category_dir)
        return category_dir

    root.mkdir(parents=True, exist_ok=True)
    log.info("Downloading %s/%s", repo, archive)
    local_archive = hf_hub_download(
        repo_id=repo,
        filename=archive,
        repo_type="dataset",
        local_dir=str(root / "_archive"),
    )
    log.info("Extracting → %s", root)
    with tarfile.open(local_archive) as tar:
        tar.extractall(path=root, filter="data")
    shutil.rmtree(root / "_archive", ignore_errors=True)
    if not category_dir.exists():
        raise RuntimeError(f"expected {category_dir} after extraction; not found")
    return category_dir


def main() -> None:
    cfg = Config.load()
    if cfg.data.source != "mvtec_ad":
        raise NotImplementedError(f"source not implemented: {cfg.data.source}")
    if not (cfg.data.hf_repo and cfg.data.hf_archive):
        raise ValueError("data.hf_repo and data.hf_archive must be set in params.yaml")

    out = fetch_mvtec_from_hf(
        repo=cfg.data.hf_repo,
        archive=cfg.data.hf_archive,
        root=cfg.data.root,
        category=cfg.data.category,
    )
    log.info("Data ready at: %s", out)


if __name__ == "__main__":
    main()
