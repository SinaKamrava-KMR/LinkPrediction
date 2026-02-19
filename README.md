# DRKG Link Prediction with (Relational) Graph Neural Networks

This repository implements an end-to-end pipeline for **link prediction** on a compact **DRKG-derived** biomedical knowledge graph.
It includes preprocessing, split construction, training and comparing multiple GNN models (**GAT**, **R-GCN**, **R-GAT**),
attention-based analysis, figure generation, query-time inference/recommendation, and evaluation on an external holdout set.

---

## Project Structure

```
project_root/
├─ code/                         # reusable python modules (helpers, models, eval utilities)
│  └─ drkg/                       # lightweight package (optional but recommended)
├─ data/
│  ├─ raw/                        # raw inputs (tsv, etc.)
│  └─ processed/                  # processed tensors, mappings, splits (generated)
├─ notebooks/                     # notebooks 01–10 (pipeline steps)
├─ output/
│  ├─ checkpoints/                # trained model weights (generated)
│  ├─ logs/                       # training logs (CSV) (generated)
│  ├─ metrics/                    # metrics + attention summaries (CSV/JSON) (generated)
│  ├─ figures/                    # plots for the report (generated)
│  ├─ queries/                    # query pair scoring + recommendations (generated)
│  └─ subgraph/                   # attention-weighted 2-hop subgraph images (generated)
└─ report/
   ├─ report.pdf                  # final report (generated / exported)
   └─ report.html                 # notebook export (generated / exported)
```

> All paths should be **relative** to `project_root/` to ensure reproducibility.

---

## Data

This project expects two TSV files (tab-separated, **no header**, 3 columns: `head`, `relation`, `tail`):

- **Training subgraph**: `drkg_subgraph_120k.tsv`  
  Used to build the main graph and create internal splits.

- **External holdout**: `drkg_test_holdout_20k.tsv`  
  Used to evaluate generalization on unseen triples. The evaluation is configured to keep only triples whose **entities and relations**
  appear in the training graph (to avoid cold-start cases).

Place them under:

```
data/raw/
├─ drkg_subgraph_120k.tsv
└─ drkg_test_holdout_20k.tsv
```

---

## Notebooks (01–10)

Run notebooks in this order:

1. `01_preprocess_drkg.ipynb`  
   Build entity/relation mappings and save typed edges.

2. `02_build_splits.ipynb`  
   Create train/val/test target edges and sample negatives for ranking evaluation.

3. Train models:
   - `03_train_gat_baseline.ipynb`
   - `04_train_rgcn.ipynb`
   - `05_train_rgat.ipynb`

4. Evaluate & analyze:
   - `06_evaluate_all.ipynb`
   - `07_attention_analysis.ipynb` (R-GAT interpretability)
   - `08_make_figures.ipynb`

5. Inference & external testing:
   - `09_query_inference.ipynb`
   - `10_evaluate_external_test.ipynb`

---

## Outputs (What Gets Generated)

### `data/processed/`
Typical generated files:
- `entity2id.json`, `id2entity.json`
- `relation2id.json`, `id2relation.json`
- `graph_edges.pt` (contains `edge_index`, `edge_type`, `num_nodes`, `num_relations`)
- `graph_meta.json`
- `split_target_edges.npz` (train/val/test positives)
- `negatives.npz` (val/test negatives, e.g., K=50)
- `train_graph_edge_idx.npy` (edges used for message passing)

### `output/logs/`
- `gat_train.csv`, `rgcn_train.csv`, `rgat_train.csv`  
  Per-epoch training logs (loss + validation metrics).

### `output/metrics/`
- `metrics_gat.json`, `metrics_rgcn.json`, `metrics_rgat.json`
- `comparison.csv` / summary tables
- `attention_by_relation.csv`, `attention_summary.json`
- `test_holdout_summary.json`

### `output/figures/`
- Degree histogram, relation count plots
- Training loss curves
- Model comparison plot
- Attention by relation plot

### `output/queries/`
- `pair_*.json`: pair scoring with resolved entities + logits/probabilities
- `recommend_rgat_*.csv`: top-k compound recommendations for a disease (ranking output)

### `output/subgraph/`
- `case_*.png`: 2-hop subgraph visualizations where **edge width ∝ attention**

---

## Models

The project compares three approaches:

- **GAT (baseline)**  
  Graph Attention Network without explicit modeling of relation types.

- **R-GCN**  
  Relational GNN that incorporates typed edges (relation-aware message passing).

- **R-GAT**  
  Relational attention model that learns attention weights conditioned on relations and neighbors.
  This model also enables interpretability via attention aggregation and subgraph visualization.

Evaluation includes:
- **Binary** metrics over positive vs sampled negatives: ROC-AUC, PR-AUC
- **Ranking** metrics with K sampled negatives per positive: MRR, Hits@K

> Note: With large negative ratios (e.g., K=50), simple accuracy can be misleading. Prefer ROC-AUC/PR-AUC and ranking metrics.

---

## Quick Start

### 1) Environment
Create an environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
# .venv\Scripts\activate       # Windows PowerShell

pip install -r requirements.txt
```

Typical requirements include:
- numpy, pandas
- pyyaml
- scikit-learn
- torch (+ your GNN library such as torch-geometric / dgl depending on implementation)
- matplotlib

### 2) Run notebooks
Open Jupyter and run notebooks from `code/` in order.

---



## Reproducibility Notes

- Fix seeds (Python/NumPy/PyTorch) in training/evaluation notebooks.
- Store split metadata (seed, ratios) alongside generated split files.
- Keep paths **relative** to `project_root/`.
- When running query inference, log the **resolved** entity IDs/names; approximate matching can change the target entity.

---

## Common Pitfalls

- **Missing `data/raw/`**: ensure raw TSV files exist under `data/raw/`.
- **Imbalance**: relation counts and degree distribution are heavy-tailed; consider per-relation/per-degree analysis.
- **Checkpoint selection**: some models (e.g., R-GCN) may overfit; select the best epoch based on validation metrics.

---

## License / Academic Use

This repository is intended for course/academic use.
