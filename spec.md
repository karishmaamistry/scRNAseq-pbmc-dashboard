# Week 5 single-cell analysis specification

## Exact question

Alex Rios is a PhD student working with a first PBMC single-cell dataset. He thinks an unusual immune-cell cluster may be a novel population. The transcript asks whether its gene pattern supports calling it novel rather than relying on its separation on a 2-D map, before he tells his PI or plans follow-up experiments.

The interview first describes **cluster 4** as the visually separate cluster, with 163 cells, 1,263 genes per cell, and 2.4% mitochondrial content. Later, the owner specifically asks for a table for **each cluster, especially cluster 7**, and a yes/no recommendation on sending cluster 7 forward as a new finding or instead “investigate further,” with the reason. The implementation must preserve this distinction and must not silently treat cluster 4 and cluster 7 as the same target.

## Data actually available

The archive is `ddls-week5-s2-novel-or-known-dataset.zip`, with the extracted single-cell file at `data_archive/data/pbmc3k.h5ad`. Scanpy inspection found:

- 2,700 cells
- 13,714 genes
- `.obs` columns: `n_genes`, `total_counts`, `pct_mito`, `leiden`
- `leiden` cluster labels: `0` through `7`
- `.var` columns: `gene_ids`, `mt`, `n_cells_by_counts`, `mean_counts`, `log1p_mean_counts`, `pct_dropout_by_counts`, `total_counts`, `log1p_total_counts`, `n_cells`, `highly_variable`, `means`, `dispersions`, `dispersions_norm`
- `.obsm` contains `X_umap`; a UMAP already exists and should be displayed rather than recomputed
- `.layers` contains `counts` (the archive description identifies this as raw UMI counts); the default expression matrix `X` is described as log-normalised expression

The requested names `n_genes_by_counts` and `pct_counts_mt` do not occur in `.obs`; the available quality fields are `n_genes`, `total_counts`, and `pct_mito`. The interview does not establish donor, condition, run date, raw-file provenance, exact normalization, feature selection, dimensionality reduction, clustering settings, or QC thresholds.

## Required product and definition of done

Create a working FastAPI + Tailwind app on port 8000 so the owner can interrogate the data rather than receive only a static answer. It must include:

- a UMAP colored by cluster;
- a gene-expression overlay;
- a top-markers table for each cluster;
- quality-metric views using the available `n_genes`, `total_counts`, and `pct_mito` fields;
- comparisons with all other cells and, where appropriate, nearest plausible clusters;
- JSON endpoints for UMAP coordinates, per-gene expression, and per-cluster top markers.

The application loads the `.h5ad` exactly once at startup with Scanpy and never reloads it per request. Every number or top gene reported by the app must be independently reproduced in plain Python and printed; the app and verification script must agree before a finding is reported.

For marker reporting, “standout” means a gene consistently more expressed in a cluster than an appropriate comparison group, with meaningful effect size, multiple-testing-adjusted significance, and detection fraction—not simply the highest average count. Results should also consider whether signals are driven by RNA capture, mitochondrial content, or a few outliers.

## Required traps to check

1. **Low gene count does not automatically mean junk.** Check mitochondrial percentage and marker genes before discarding a cluster.
2. **High counts or genes may indicate a doublet.** Check co-expression of two lineage markers and whether housekeeping or ribosomal genes dominate.
3. **Spatial separation on UMAP does not establish a novel cell type.** Cell identity must be evaluated from marker-gene programs and comparisons, not the map alone.

## Claimed identity and evidence standard

The owner claims no confirmed cell-type identity. He suspects the unusual cluster may be a **new immune-cell population**: cluster 4 is described as separate on the map and difficult to place, while the final requested decision emphasizes cluster 7. No ranked genes or marker matches were available in the interview, so no identity can be assigned yet.

Evidence supporting a novel-population claim would require a coherent and distinctive gene program, acceptable quality metrics, clear distinction from nearest known PBMC groups, recurrence in an independent donor or dataset, and eventual experimental confirmation. Evidence contradicting or downgrading the claim includes mixed incompatible lineage signals, unusually high `n_genes`/capture consistent with doublets, quality-dependent disappearance, lack of recurrence, or only a weak unstable signature. In those cases the appropriate conclusion is technical artifact, low-quality/mixed population, known subgroup, or “candidate population/investigate further”—not “novel cell type.”

The final report must make the evidence and limitations explicit and must not infer identity from diagnosis, UMAP position, or quality metrics alone.
