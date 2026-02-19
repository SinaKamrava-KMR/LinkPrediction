# DRKG Project Notebooks (01–10)

This repository contains a notebook-based pipeline for **DRKG link prediction** experiments, including:
data preprocessing, split construction, training multiple baselines/models, evaluation, attention analysis,
figure generation, query-time inference, and external test evaluation.

---

## Notebooks Overview

### 01_preprocess_drkg.ipynb
**Goal:** Prepare the raw DRKG data into a clean, model-ready format.

**Typical steps:**
- Load raw DRKG triples (head, relation, tail)
- Clean/normalize entity and relation identifiers
- Build entity/relation vocabularies and ID mappings
- Save processed artifacts for later notebooks

**Outputs (examples):**
- Processed triples (train-ready format)
- `entity2id`, `relation2id` mappings
- Any cached intermediate files in `data/processed/` or `output/`

---

### 02_build_splits.ipynb
**Goal:** Build train/validation/test splits for link prediction.

**Typical steps:**
- Construct positive edges from processed triples
- Generate split files (pos edges)
- Create / store negative samples (if used offline)
- Save indices / masks for reproducible evaluation

**Outputs (examples):**
- `train_pos`, `val_pos`, `test_pos`
- optional `train_neg`, `val_neg`, `test_neg`
- split metadata (seed, ratios, constraints)

---

### 03_train_gat_baseline.ipynb
**Goal:** Train a **GAT baseline** for link prediction (or embedding + scorer).

**Typical steps:**
- Load splits + graph
- Build baseline model (GAT encoder + link predictor/scorer)
- Train loop + checkpointing
- Save metrics and trained weights

**Outputs (examples):**
- model checkpoints in `output/checkpoints/gat/`
- training curves / logs
- embeddings or predictions (optional)

---

### 04_train_rgcn.ipynb
**Goal:** Train **R-GCN** for multi-relational DRKG link prediction.

**Typical steps:**
- Build a relational graph with typed edges
- Configure R-GCN (hidden size, num bases, layers, etc.)
- Train + validate, save best checkpoint

**Outputs (examples):**
- model checkpoints in `output/checkpoints/rgcn/`
- validation metrics per epoch

---

### 05_train_rgat.ipynb
**Goal:** Train **R-GAT (Relational Graph Attention)** for DRKG link prediction.

**Typical steps:**
- Load relational graph + splits
- Configure RGAT (heads, bases, layers, dropout, etc.)
- Train + checkpoint best model

**Outputs (examples):**
- model checkpoints in `output/checkpoints/rgat/`
- attention weights (if stored) or intermediate stats

---

### 06_evaluate_all.ipynb
**Goal:** Evaluate all trained models (GAT, R-GCN, R-GAT) on the same split.

**Typical steps:**
- Load checkpoints for each model
- Run scoring on (pos + neg) pairs
- Compute link prediction metrics (ROC-AUC, AP, Hits@K if implemented)
- Compare results across models

**Outputs (examples):**
- a comparison table (CSV/JSON) in `output/results/`
- plots or summary metrics

---

### 07_attention_analysis.ipynb
**Goal:** Analyze attention patterns (mainly for attention-based models like GAT/RGAT).

**Typical steps:**
- Load trained attention model
- Extract attention weights (by layer/head/relation)
- Identify most influential neighbors/relations
- Produce interpretability plots/tables

**Outputs (examples):**
- attention statistics tables
- neighbor/relation importance summaries
- interpretability figures

---

### 08_make_figures.ipynb
**Goal:** Produce publication/report-ready figures.

**Typical steps:**
- Load saved metrics and result tables
- Plot training curves, ROC/AP comparisons, ablations, etc.
- Export figures to `output/figures/`

**Outputs:**
- `.png` / `.pdf` plots in `output/figures/`

---

### 09_query_inference.ipynb
**Goal:** Run query-time inference for a specific link prediction question.

**Typical steps:**
- Load model checkpoint + entity/relation mapping
- Encode/query (head, relation, ?) or (?, relation, tail)
- Rank candidate entities and display top-k predictions

**Outputs (examples):**
- top-k ranked predictions shown in notebook
- optional exported tables to `output/inference/`

---

### 10_evaluate_external_test.ipynb
**Goal:** Evaluate models on an **external test dataset** (separate from internal split).

**Typical steps:**
- Load external test triples/pairs
- Map entities/relations to internal IDs (handle unknowns)
- Score and compute metrics on external set
- Compare generalization vs internal test

**Outputs (examples):**
- metrics table for external test
- plots comparing internal vs external performance

---

## Recommended Execution Order

Run notebooks in this order:

1. `01_preprocess_drkg.ipynb`
2. `02_build_splits.ipynb`
3. Train models:
   - `03_train_gat_baseline.ipynb`
   - `04_train_rgcn.ipynb`
   - `05_train_rgat.ipynb`
4. Evaluation and analysis:
   - `06_evaluate_all.ipynb`
   - `07_attention_analysis.ipynb` (optional)
   - `08_make_figures.ipynb`
5. Inference and external testing:
   - `09_query_inference.ipynb`
   - `10_evaluate_external_test.ipynb`

---

## Output Convention

To keep the project reproducible:
- Store raw files under `data/raw/`
- Store processed artifacts under `data/processed/`
- Store model checkpoints under `output/checkpoints/<model_name>/`
- Store results tables under `output/results/`
- Store figures under `output/figures/`

---

## Reproducibility Notes

- Fix random seeds (Python/NumPy/PyTorch) inside training/evaluation notebooks.
- Save split metadata (seed, ratios) alongside split files.
- Always build file paths relative to the project root.

---
