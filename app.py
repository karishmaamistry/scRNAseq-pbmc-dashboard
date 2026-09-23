from pathlib import Path
from typing import Optional

import numpy as np
import scanpy as sc
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).parent
DATA = ROOT / "data_archive" / "data" / "pbmc3k.h5ad"
# Loaded exactly once at startup/import; request handlers reuse this object.
AD = sc.read_h5ad(DATA)
GENES = list(AD.var_names.astype(str))
GENE_LOOKUP = {gene.casefold(): gene for gene in GENES}
CLUSTER_KEY = "leiden"
CLUSTERS = [str(x) for x in AD.obs[CLUSTER_KEY].cat.categories]
MARKERS = {}

app = FastAPI(title="PBMC Cluster Explorer")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")


def jsonable(value):
    if isinstance(value, (np.integer, np.floating)):
        return value.item()
    return value


def resolve_gene(gene: str) -> str:
    requested = gene.strip()
    exact = {str(name): str(name) for name in AD.var_names}
    if requested in exact:
        return exact[requested]
    if requested.casefold() in GENE_LOOKUP:
        return GENE_LOOKUP[requested.casefold()]
    raise HTTPException(404, f"Unknown gene: {gene}")


def matrix_column(gene: str):
    gene = resolve_gene(gene)
    x = AD[:, gene].X
    if hasattr(x, "toarray"):
        x = x.toarray()
    return np.asarray(x).ravel()


@app.get("/", response_class=HTMLResponse)
def index():
    return (ROOT / "static" / "index.html").read_text(encoding="utf-8")


@app.get("/api/meta")
def meta():
    return {
        "cells": int(AD.n_obs), "genes": int(AD.n_vars),
        "clusters": CLUSTERS,
        "obs": list(AD.obs.columns), "var": list(AD.var.columns),
        "obsm": list(AD.obsm.keys()), "layers": list(AD.layers.keys()),
    }


@app.get("/api/umap")
def umap(cluster: Optional[str] = None):
    if "X_umap" not in AD.obsm:
        raise HTTPException(500, "X_umap is not present")
    mask = np.ones(AD.n_obs, dtype=bool) if cluster is None else (AD.obs[CLUSTER_KEY].astype(str).to_numpy() == cluster)
    coords = np.asarray(AD.obsm["X_umap"])[mask]
    obs = AD.obs.loc[mask]
    return {"points": [{"x": float(x), "y": float(y), "cluster": str(c), "n_genes": int(n), "total_counts": float(t), "pct_mito": float(p)} for (x, y), c, n, t, p in zip(coords, obs[CLUSTER_KEY], obs.n_genes, obs.total_counts, obs.pct_mito)]}


@app.get("/api/expression/{gene}")
def expression(gene: str):
    resolved = resolve_gene(gene)
    values = matrix_column(resolved)
    coords = np.asarray(AD.obsm["X_umap"])
    return {"gene": resolved, "points": [{"x": float(x), "y": float(y), "value": float(v), "cluster": str(c)} for (x, y), v, c in zip(coords, values, AD.obs[CLUSTER_KEY])]}


def build_markers():
    tmp = AD.copy()
    tmp.obs[CLUSTER_KEY] = tmp.obs[CLUSTER_KEY].astype(str).astype("category")
    sc.tl.rank_genes_groups(tmp, groupby=CLUSTER_KEY, reference="rest", method="wilcoxon", n_genes=20, key_added="startup_markers")
    ranked = tmp.uns["startup_markers"]
    for cluster in CLUSTERS:
        names = ranked["names"][cluster]
        scores = ranked["scores"][cluster]
        pvals = ranked["pvals_adj"][cluster]
        mask = AD.obs[CLUSTER_KEY].astype(str).to_numpy() == cluster
        rows = []
        for gene, score, pval in zip(names, scores, pvals):
            expr = matrix_column(str(gene))
            rows.append({"gene": str(gene), "score": float(score), "p_adj": float(pval), "fraction": float(np.mean(expr[mask] > 0)), "mean_cluster": float(np.mean(expr[mask])), "mean_rest": float(np.mean(expr[~mask]))})
        MARKERS[cluster] = rows


build_markers()


@app.get("/api/markers/{cluster}")
def markers(cluster: str):
    if cluster not in MARKERS:
        raise HTTPException(404, "Unknown cluster")
    return {"cluster": cluster, "markers": MARKERS[cluster]}
