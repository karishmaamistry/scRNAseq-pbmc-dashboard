from pathlib import Path
import numpy as np
import scanpy as sc

ad = sc.read_h5ad(Path(__file__).parent / 'data_archive/data/pbmc3k.h5ad')
print('shape:', ad.shape)
print('clusters:', sorted(ad.obs['leiden'].astype(str).unique()))
print('umap shape:', ad.obsm['X_umap'].shape)
for cluster in ['4', '7']:
    mask = ad.obs['leiden'].astype(str).to_numpy() == cluster
    print(f'cluster {cluster} cells:', int(mask.sum()))
    tmp = ad.copy()
    tmp.obs['leiden'] = tmp.obs['leiden'].astype(str).astype('category')
    sc.tl.rank_genes_groups(tmp, groupby='leiden', groups=[cluster], reference='rest', method='wilcoxon', n_genes=10)
    names = [str(x) for x in tmp.uns['rank_genes_groups']['names'][cluster]]
    print(f'cluster {cluster} top genes:', names)
    for gene in names[:3]:
        x = ad[:, gene].X
        if hasattr(x, 'toarray'): x = x.toarray()
        x = np.asarray(x).ravel()
        print(f'  {gene}: fraction={float(np.mean(x[mask] > 0)):.6f}, mean_cluster={float(np.mean(x[mask])):.6f}')
