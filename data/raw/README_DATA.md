# DRKG Derived Datasets (TSV)

This folder provides two DRKG-derived TSV files used for link prediction experiments:
1) a sampled subgraph for training/validation split creation,
2) an external holdout set for testing generalization.

Both files share the same format.

---

## File: `drkg_subgraph_120k.tsv`

**Purpose:** A compact DRKG subgraph intended for building the main graph and creating train/val/test splits.

**Actual size (from file content):**
- Rows (triples): **118,308**
- Unique relations: **107**
- Unique entities (head ∪ tail): **37,614**

**Notes:**
- The filename indicates an approximate size (“120k”), but the exact row count is 118,308.

---

## File: `drkg_test_holdout_20k.tsv`

**Purpose:** An external holdout set for evaluating trained models on unseen test triples (generalization).

**Actual size (from file content):**
- Rows (triples): **19,592**
- Unique relations: **95**
- Unique entities (head ∪ tail): **15,351**

**Notes:**
- The filename indicates an approximate size (“20k”), but the exact row count is 19,592.

---

## Common Format (Both Files)

- **File type:** TSV (tab-separated values)
- **Encoding:** UTF-8
- **Header:** **No header row**
- **Columns (3):**
  1. `head`   (string) — entity identifier
  2. `relation` (string) — typed relation identifier
  3. `tail`   (string) — entity identifier

### Example row
