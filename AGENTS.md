# Operating instructions

## Environment

- Use the project virtual environment created with `uv venv`.
- Run Python through `uv run`; do not invoke a system Python directly.
- Installed task dependencies are `scanpy`, `anndata`, `fastapi`, `uvicorn[standard]`, `plotly`, and `python-multipart`. Install additional packages only when the task requires them.

## Data

- The supplied archive is `ddls-week5-s2-novel-or-known-dataset.zip`.
- It was extracted to `data_archive/data/pbmc3k.h5ad` (39,023,720 bytes; below the 100 MB Git-ignore threshold). `data_archive/data/ABOUT_THIS_FILE.txt` describes it as an already processed PBMC single-cell RNA-seq file.
- The file was inspected with Scanpy. It contains **2,700 cells and 13,714 genes**.
- `obs` columns: `n_genes`, `total_counts`, `pct_mito`, `leiden`.
  - `leiden` is categorical and contains the numbered clusters `0`, `1`, `2`, `3`, `4`, `5`, `6`, and `7`.
  - The quality/measurement columns present are `n_genes`, `total_counts`, and `pct_mito`; the requested names `n_genes_by_counts` and `pct_counts_mt` are not present under those names.
- `var` columns: `gene_ids`, `mt`, `n_cells_by_counts`, `mean_counts`, `log1p_mean_counts`, `pct_dropout_by_counts`, `total_counts`, `log1p_total_counts`, `n_cells`, `highly_variable`, `means`, `dispersions`, `dispersions_norm`.
- `obsm` keys: `X_umap`; a UMAP embedding is already computed and must not be recomputed merely to display it.
- `layers` keys: `counts`; `None` is also reported by the library as the default/unnamed layer entry. `ABOUT_THIS_FILE.txt` says `X` is log-normalised expression and `layers["counts"]` contains raw UMI counts.
- The source is a PBMC dataset; donor, condition, exact preprocessing, QC thresholds, run date, and raw-file provenance were not supplied by the interview.

## Outputs

Write all analysis results, reports, and exports to `results/`. Do not put generated outputs in the project root.

## App requirements

- Build a FastAPI + Tailwind interface on port 8000 when implementation begins.
- Load the `.h5ad` file **once at application startup with Scanpy**. Never reload it per request.
- Provide JSON endpoints for:
  - UMAP coordinates;
  - per-gene expression;
  - per-cluster top markers.
- The UI must make the data interrogable rather than presenting only a static conclusion.

## Verification rule

Whenever the app reports a number or a top gene for a cluster, reproduce that number in plain Python and print it. The app and the verification script must agree before reporting any finding.

## Version control

This folder is a Git repository. Commit before any large change and whenever something starts working, using short, clear commit messages.
