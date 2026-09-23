# PBMC analysis summary

## Reproducible observations

The source contains 2,700 cells, 13,714 genes, eight numbered clusters, an existing 2-D `X_umap`, and a `counts` layer. The interview's quoted cluster-4 summary is reproduced: cluster 4 contains 163 cells. Cluster 7 contains 10 cells in the current file.

Using Scanpy's Wilcoxon rank-groups test against the rest, the verification script printed these top genes:

- Cluster 4: `LST1`, `FCER1G`, `FCGR3A`, `COTL1`, `AIF1`, `IFITM2`, `IFITM3`, `FTH1`, `SAT1`, `SERPINA1`.
- Cluster 7: `ACTG1`, `CFL1`, `GAPDH`, `KIAA0101`, `SLC25A5`, `STMN1`, `ACTB`, `FABP5`, `H2AFV`, `PFN1`.

For the first three genes of each cluster, the verification output also printed expression fraction and cluster mean. The app exposes the complete marker table with score, adjusted p-value, detection fraction, cluster mean, and rest mean.

## Interpretation boundary

This is an exploratory, reproducible app-backed result, not a definitive novel-cell-type claim. Cluster 4 has a coherent myeloid/monocyte-associated marker pattern in the observed top genes, which argues against calling it novel solely because it is spatially separate. Cluster 7's top list is dominated by broadly expressed/housekeeping or proliferation-associated genes in this small 10-cell cluster; that is insufficient evidence for a novel identity. The appropriate owner-facing status is **investigate further**, pending marker comparisons, doublet/QC review, independent replication, and experimental confirmation.

No donor/condition metadata, pipeline settings, exact QC thresholds, independent replication, or experimental validation is present in the supplied materials.
