# scRNA-seq PBMC Dashboard

Interactive dashboard for exploring a processed 2,700-cell PBMC single-cell RNA-sequencing dataset.

## Features

- UMAP colored by cluster labels
- Case-insensitive gene-expression search and UMAP overlays
- Continuous expression color gradients
- Per-cluster top-marker tables
- Marker filtering by gene symbol
- Detection fraction, adjusted p-value, cluster mean, and rest mean
- Quality metrics including `n_genes`, `total_counts`, and `pct_mito`
- FastAPI JSON endpoints for UMAP coordinates, gene expression, and markers

## Dataset

The application reads:

```text
data_archive/data/pbmc3k.h5ad
```

The file contains 2,700 cells and 13,714 genes, with cluster labels in `obs["leiden"]`, a precomputed `obsm["X_umap"]`, and raw counts in the `counts` layer.

The source archive and data description are retained in the repository. The `.h5ad` file itself is excluded by `.gitignore` if extracted separately.

## Requirements

- Python
- `uv`

The project uses a virtual environment managed by `uv` and the following packages:

- scanpy
- anndata
- fastapi
- uvicorn[standard]
- plotly
- python-multipart

## Setup

Create the environment:

```bash
uv venv
```

Install dependencies:

```bash
uv pip install --python .venv/Scripts/python.exe scanpy anndata fastapi "uvicorn[standard]" plotly python-multipart
```

On macOS/Linux, use `.venv/bin/python` instead of `.venv/Scripts/python.exe`.

## Run the dashboard

```bash
uv run uvicorn app:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000 in a browser.

## Verify results

Run the reproducibility checks with:

```bash
uv run python verify.py
```

The verification output is stored in `results/verification.txt`. Analysis notes are in `results/analysis_summary.md`.

## API endpoints

- `GET /api/meta`
- `GET /api/umap`
- `GET /api/umap?cluster=4`
- `GET /api/expression/{gene}`
- `GET /api/markers/{cluster}`

Gene lookup is case-insensitive, so `cd3d`, `Cd3d`, and `CD3D` resolve to the same stored gene symbol.

## Interpretation note

UMAP separation alone does not establish a novel cell type. Marker programs, quality metrics, possible doublets, comparisons with neighboring clusters, independent replication, and experimental validation are required before making a novelty claim. The current exploratory conclusion is to investigate further rather than declare a novel cell type.
