# MLOps Guide — `mlops/`

A working reference for the StoneScan ML pipeline. Read top-to-bottom the
first time; afterwards use it as a lookup.

---

## 1. Mental model

A modern ML system has **three** versioned artifacts that must travel together:

| Artifact | Tool | What it answers |
|---|---|---|
| Code | git | What logic was used? |
| Data | DVC | What data was used? |
| Model + experiment record | MLflow | What was trained, scored, and why? |

Most "it worked on my laptop" disasters happen because one of these drifted.
This pipeline keeps all three in lockstep:

- The git SHA pins the code.
- A `.dvc` pointer pins the dataset hash.
- An MLflow `run_id` pins the trained weights and every hyperparameter that
  produced them.

When you deploy a model to the cloud inference service, you ship the **run_id**
plus the exported ONNX. Anyone who needs to reproduce or debug it can resurrect
the exact code + data combination from those three handles.

---

## 2. Repository layout

```
mlops/
├── pyproject.toml          # Packaging + dev tooling (single source of truth)
├── requirements.txt        # Mirror of pyproject deps for non-pyproject tools
├── params.yaml             # Hyperparameters — DVC reads these
├── dvc.yaml                # Pipeline DAG: fetch → train → eval → export
├── Makefile                # Everyday commands (`make setup`, `make train`)
├── MLOPS_GUIDE.md          # ← this file
│
├── src/stonescan_ml/       # Importable library code (the only place logic lives)
│   ├── config.py           #   typed Pydantic config loader
│   ├── data/               #   datasets, downloaders, transforms
│   ├── models/             #   custom model code (later)
│   ├── training/           #   training functions, callable from anywhere
│   ├── evaluation/         #   metrics, plotting, report generation
│   ├── export/             #   ONNX exporters for cloud GPU serving
│   └── utils/              #   logging, seeding, IO
│
├── scripts/                # Thin entry points — no logic, just CLI glue
│   ├── fetch_data.py
│   ├── train.py
│   ├── evaluate.py
│   └── export.py
│
├── tests/                  # pytest — config validation + metric math
├── configs/                # (reserved for per-experiment override files)
│
├── data/                   # DVC-tracked
│   ├── raw/                #   immutable downloads
│   ├── interim/            #   intermediate transforms
│   └── processed/          #   training-ready
│
├── models/checkpoints/     # Trained weights (gitignored; DVC-tracked)
├── serving/                # Exported ONNX models for cloud serving (gitignored; DVC-tracked)
└── reports/                # Metrics JSON, figures, eval artifacts
```

### Why the `src/` layout

The `src/` layout (vs flat top-level modules) is the modern Python default:

- Forces your code to be a real installable package, so `import stonescan_ml`
  resolves identically on your laptop, in CI, and on the cloud GPU node — no
  `sys.path.append` hacks.
- Lets `pip install -e .` make tests run against the same import path as
  scripts.
- Cleanly separates *library* (`src/`) from *entry points* (`scripts/`) from
  *configuration* (`params.yaml`, `configs/`).

### Why scripts are thin

Every `scripts/*.py` does three things and nothing else:
1. Load config.
2. Call a function from `src/`.
3. Write outputs to the path DVC expects.

Logic in `src/` is unit-testable and reusable. Logic stuck inside a script
is none of those things.

---

## 3. The pipeline flow

```
                   params.yaml ──┐
                                 │
data/raw/ ◄──── fetch_data ◄─────┤
    │                            │
    ▼                            │
  train  ◄────── code in src/ ◄──┤
    │                            │
    ▼                            │
models/checkpoints/  ─────►  evaluate  ───►  reports/eval_report.json
                                 │
                                 ▼
                              export  ──►  serving/  (ONNX → cloud inference service)
                                 │
                                 └──► mlflow (params, metrics, model artifact)
```

Each arrow in this diagram is a DVC stage in `dvc.yaml`. DVC's job is to
know which arrows need to re-run when an input changes. Change
`image_size` in `params.yaml` and `dvc repro` re-runs train + evaluate +
export, but skips fetch_data because data didn't change.

---

## 4. DVC vs MLflow — the part everyone gets wrong

They sound like competitors. They're not. They sit at right angles:

| Question | Tool |
|---|---|
| "What artifacts should exist, given this code + this data + these params?" | **DVC** |
| "I trained 47 models last month — which had the best pixel AUROC?" | **MLflow** |
| "Can I revert the dataset to exactly what `feat-fissure-v3` was trained on?" | **DVC** |
| "What was the learning rate for run `a3f2…`?" | **MLflow** |

**DVC reproduces. MLflow remembers.** A clean workflow uses both:

1. You change something in code or `params.yaml`.
2. `dvc repro` re-runs only the affected stages and updates the pinned
   hashes in `dvc.lock`.
3. Inside `train`, every run logs to MLflow regardless of whether DVC chose
   to re-run.
4. You browse MLflow to pick a winning run; you reach for `git` + `dvc
   checkout` to actually resurrect its code + data.

The model registry (a feature of MLflow) is the bridge to deployment: you
promote a `run_id` to `staging` → `production`, and the edge bundler reads
"latest production" rather than a hardcoded path.

---

## 5. Reproducibility — the things that bite

A "reproducible" pipeline still drifts unless you nail all of these:

1. **Seed every RNG** — `src/stonescan_ml/utils/seed.py` handles `random`,
   numpy, torch, CUDA, cuDNN.
2. **Pin dependency versions** — `pyproject.toml` has bounds; consider
   `pip-compile` to produce a lock file for production.
3. **Hash the data** — DVC does this. Never train from an unversioned
   directory; you'll regret it the day a collaborator deletes a file.
4. **Log the git SHA** — MLflow auto-tags runs with it. Don't disable that.
5. **Capture the environment** — log `pip freeze` output as an MLflow
   artifact for any run you care about.
6. **Determinism flags** — `cudnn.deterministic=True` costs ~10–20% perf
   but makes runs bit-identical. Worth it for the eval gate.

---

## 6. Config strategy

Hyperparameters live in **one** place: `params.yaml`. Three tools read it:

- **DVC** — knows which stages depend on which sub-trees (`params:` section
  in `dvc.yaml`).
- **Our code** — `Config.load()` parses + validates with Pydantic.
- **Humans** — diff-friendly YAML; PR reviewers can see param changes
  inline.

For multi-experiment sweeps, layer Hydra later (`configs/experiment/*.yaml`
overriding `params.yaml`). Not needed yet.

The **typed config** (Pydantic) catches `bacth_size: 32` (typo) at startup
in milliseconds, instead of letting it crash 4 hours into training with a
confusing `KeyError`.

---

## 7. Data layer principles

- `data/raw/` is **immutable**. Downloaded once, never edited. Any
  transformation produces a *new* file under `data/interim/` or
  `data/processed/`.
- The downloader (`src/stonescan_ml/data/mvtec.py`) verifies the archive
  (SHA256 logged), so a half-downloaded file doesn't poison your training
  set silently.
- DVC tracks `data/raw/` by hash. The cache lives in `.dvc/cache/` and is
  gitignored. To push the dataset to remote storage:
  `dvc remote add -d s3 s3://stonescan-data && dvc push`.
- For your own stone images later: same pattern. Drop them into a category
  folder under `data/raw/stonescan/granite/good/`, run `dvc add`, commit
  the `.dvc` pointer.

---

## 8. The training contract

`train_patchcore(cfg, output_dir)` in `src/stonescan_ml/training/anomaly.py`
is the single function every entry point (script, test, notebook, Airflow
task) calls. The contract:

- **Input**: validated `Config` + an output directory.
- **Side effects**: writes a checkpoint under `output_dir`, logs to MLflow.
- **Return**: dict with `run_id` and metrics.

This is the dependency-inversion habit applied to ML — your training
function depends on a config interface, not on argparse. Anything that can
build a `Config` can train.

---

## 9. Evaluation discipline

`src/stonescan_ml/evaluation/metrics.py` defines a single `compute_image_report`.
The eval script, future CI checks, and the production dashboard all call
it. This matters because:

- "image AUROC" has two slightly different definitions in the wild
  (per-image score vs per-pixel reduced to image). Pick one, encode it,
  reference it everywhere.
- Tests in `tests/test_metrics.py` pin the math: perfect separation → 1.0,
  inverted scores → 0.0, threshold sweep → reasonable bounds. If someone
  "refactors" later and breaks the convention, tests catch it.

The gate G1 ("scanner beats expert") becomes a literal CI check:
`assert report.image_auroc >= 0.95`.

---

## 10. Export & cloud serving

Train in PyTorch, export to **ONNX** once, and serve it in the cluster with
**ONNX Runtime-GPU** (or Triton) behind the inference service — no per-device
bundles, no signing, no OTA. Updating a model is a normal cluster deploy.

`scripts/export.py` reads the **latest checkpoint** for the configured
model+category and emits `serving/<model>/<category>/`. The cloud inference
service loads this artifact (packaged into its container image, or pulled from
object storage) and runs it on the GPU node pool.

Keep GPU-specific optimization (e.g. TensorRT engine build) as a separate,
post-export step that runs on a CUDA box matching the serving node — not in CI.

---

## 11. Active learning loop (later)

Once pilot devices are uploading scans:

```
device → mobile app → backend (scan + low-confidence flag)
                 ↓
            uncertain queue
                 ↓
          human labeling (CVAT)
                 ↓
         data/processed/ append + dvc push
                 ↓
              dvc repro
                 ↓
       MLflow comparison vs current prod
                 ↓
         registry promotion (if better)
                 ↓
        cluster deploy (new model image)
```

Anomaly-detection-first makes this loop short: the model surfaces "this
doesn't look like normal stone," human confirms or rejects, and the
labeled example feeds back. You don't need pre-existing crack masks to
start.

---

## 12. CI/CD outline (later)

A `.github/workflows/ml.yml` that on every PR:

1. `pip install -e ".[dev]"`
2. `ruff check` + `mypy`
3. `pytest -q` (config + metric math)
4. `dvc pull` (cached small subset)
5. `dvc repro` against the subset
6. Read `reports/eval_report.json`, fail PR if `image_auroc <
   threshold`.

This turns the gate criteria into mechanical checks. PRs that regress
detection cannot merge.

---

## 13. Commands cheat sheet

```bash
make setup          # create venv + install package + dev tools
make fetch          # download MVTec AD (one-time per category)
make train          # train PatchCore on configured category
make eval           # compute clean metrics report
make export         # emit ONNX bundle
make pipeline       # `dvc repro` — runs whatever's stale
make test           # pytest
make lint           # ruff
make mlflow-ui      # open http://127.0.0.1:5000 for run comparison
```

---

## 14. Reading order for someone joining the codebase

1. `params.yaml` — what's tunable.
2. `dvc.yaml` — the DAG.
3. `src/stonescan_ml/config.py` — the validated config shape.
4. `scripts/train.py` → `src/stonescan_ml/training/anomaly.py` — the train path.
5. `src/stonescan_ml/evaluation/metrics.py` + `tests/test_metrics.py` — what
   we measure and how we test the measurement.
6. This guide.
