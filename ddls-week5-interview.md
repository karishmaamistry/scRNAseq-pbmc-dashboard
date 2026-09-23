# DDLS 2026 — Week 5 interview transcript

**Lab:** Interview a Single-Cell Data Owner
**Data owner:** Alex Rios — PhD student who thinks they've found a novel immune cell population
**Student:** Karishma Mistry <karishmamistry86160@gmail.com>
**Exported:** 2026-09-23T12:26:12+00:00

> This is the record of your interview with the data owner. Hand it to your analyst agent as the raw source for `AGENTS.md` and `spec.md`.

---

**You**:

Hi Alex! What type of data are we working on today? What does your data contain? and what do you want your results to look like?

**Alex Rios**:

Hi—I’m Alex, and this is my first PBMC single-cell dataset: 2,700 blood immune cells grouped into numbered clusters 0–7 on a 2-D map. Cluster 4, about **163 cells**, sits off on its own and I can’t place it, so I’m hoping it might be **a new population**. I want to know whether the gene pattern really supports calling it novel, rather than just relying on the map, before I tell my PI or plan follow-up experiments. Can you help me confirm that?

**You**:

yes can you tell me how does these cells look? and what do you mean by sits off on its own?

**Alex Rios**:

By “sits off on its own,” I mean cluster 4 forms a separate-looking group on the 2-D map. Its summary is **163 cells, 1,263 genes/cell, and 2.4% mito**—but okay, fair, being separate isn’t the same as being new. Do you want to start with its standout genes, or compare those genes directly with the neighbouring clusters?

**You**:

Let's look at the standout genes. What are the top differentially expressed genes for Cluster 4, and do they match any known marker genes for specific peripheral blood mononuclear cells (PBMCs)?

**Alex Rios**:

I don’t have the ranked gene list for cluster 4 in the summary, only **163 cells, 1,263 genes/cell, and 2.4% mito**. So I can’t honestly name its standout genes or match them to PBMC populations from what I can see—please paste the top DE genes, and you tell me whether they point to a known group or something genuinely distinct.

**You**:

Where did the raw data, the cluster numbers (0–7), and the 2D map labels come from? and how did you map it exactly?

**Alex Rios**:

The raw dataset is my **2,700-cell PBMC single-cell dataset**; I only have the cluster summary and the 2-D map labels here. I generated clusters **0–7** from the analysis, but I don’t have the preprocessing, dimensionality-reduction, or clustering settings in front of me, so I can’t tell you exactly how the map was constructed or reproduce the mapping. Are you asking about the data’s biological source, or the computational steps that produced the map?

**You**:

both

**Alex Rios**:

Biological source: **PBMCs—2,700 blood immune cells**. I don’t have donor, condition, or raw-file metadata here.

Computationally, I assigned the labels **0–7** after clustering the cells and plotted them on a 2-D embedding, but I don’t have the exact normalization, feature selection, reduction, or clustering settings. So I can describe the map, not reproduce exactly how each label was generated.

**You**:

When you look for 'standout' or 'matching' genes in the app, what exactly are we measuring?

**Alex Rios**:

Usually, “standout” means genes with higher expression in one cluster than in the others—often summarized with a statistical differential-expression score and an effect size. “Matching” means comparing those genes with established PBMC marker sets.

That’s separate from **n_genes** and **% mito**: those describe each cell’s captured transcriptome and mitochondrial-read fraction, not its identity. I don’t know the app’s exact test or thresholds here—what app and display are you using?

**You**:

What would count as convincing evidence for your PI that a cluster is truly a 'new' cell type, rather than just a technical glitch, a low-quality cell mix, or a subgroup of a known cell type?

**Alex Rios**:

I’d want more than separation on the map: a **coherent, distinctive gene program** that isn’t just unusually high RNA capture, acceptable quality metrics, and clear distinction from the nearest known PBMC groups. I’d also want the pattern to recur in another donor or dataset, then be confirmed experimentally; otherwise the honest claim is “candidate population,” not “new cell type.”

For cluster 4, we have **163 cells, 1,263 genes/cell, and 2.4% mito**, but we still need its actual standout genes and comparisons with neighbouring clusters. Do you want the PI-facing call to be “new,” “known subgroup,” or “investigate further”?

**You**:

When the app calculates or retrieves these missing comparisons, how should it define a 'standout' gene?

**Alex Rios**:

I’d define a standout gene as one that is **consistently more expressed in the cluster than in an appropriate comparison group**, with a meaningful effect size and a multiple-testing-adjusted significance value—not simply the gene with the highest average count.

The comparison should be both against all other cells and against the nearest plausible clusters, while checking how many cells express the gene and whether the result is driven by RNA capture, mitochondrial content, or a few outliers. A gene list without those effect sizes, detection fractions, and adjusted values wouldn’t be enough to support a “new” call. Are you looking at the app’s rank list, or can it show those statistics too?

**You**:

When was this analysis run, what exact preprocessing and quality-control filtering thresholds were applied to the raw sequencing data, and has anything shifted or changed between the raw data files and the summary metrics you have right now?

**Alex Rios**:

I don’t have the run date, raw-file provenance, or the exact preprocessing/QC thresholds here. I also can’t verify whether anything changed between the raw files and the current summary; all I can quote is the summary for cluster 4: **163 cells, 1,263 genes/cell, 2.4% mito**.

So I wouldn’t present the analysis as fully reproducible until we retrieve the pipeline log, filtering report, and versioned object. Do you have the analysis notebook or processing metadata?

**You**:

What specific result in that replication dataset would completely downgrade this cluster to a 'technical artifact,' a low-quality cell mix, or just a generic 'candidate population' rather than a novel cell type?

**Alex Rios**:

The strongest downgrade would be: in an independent donor or run, the cluster **doesn’t recur with the same coherent gene program**—and the few matching cells instead track unusually high `n_genes`, show mixed incompatible lineage signals, or disappear after stricter QC. That would support a technical artifact or cell mixture; if it recurs only weakly without a stable signature, I’d call it **“candidate population,” not novel cell type**. Do you have a replication gene list and its `n_genes`/`pct_mito` values?

**You**:

how do you want your data to look like that I will process?

**Alex Rios**:

I want a table for each cluster—especially **cluster 7**—with its strongest genes, effect sizes, adjusted significance, and fraction of cells expressing each gene, alongside `n_genes` and `pct_mito`. Include comparisons with the nearest clusters, not just the 2-D map. Then give me a yes/no on sending cluster 7 forward as a new finding, or “investigate further,” with the reason.
