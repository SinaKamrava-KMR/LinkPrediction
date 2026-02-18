
from pathlib import Path
import json
import gzip

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(obj, path: Path):
    ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def open_maybe_gz(path: Path, mode="rt"):
    if str(path).endswith(".gz"):
        return gzip.open(path, mode, encoding="utf-8", errors="ignore")
    return open(path, mode, encoding="utf-8", errors="ignore")

def read_tsv_edges(path: Path, max_edges: int = None):

    with open_maybe_gz(path, "rt") as f:
        for i, line in enumerate(f):
            if max_edges is not None and i >= max_edges:
                break
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) < 3:
                continue
            h, r, t = parts[0], parts[1], parts[2]
            yield h, r, t

def load_yaml(path: Path):
    import yaml
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
