from collections import Counter
from pathlib import Path
import torch

def parse_entity_type(entity: str) -> str:

    if "::" in entity:
        return entity.split("::", 1)[0]
    if ":" in entity:
        return entity.split(":", 1)[0]
    return "UNK"

def build_mappings_and_edges(edge_iter, relations_keep=None, entity_types_keep=None):

    entity2id = {}
    relation2id = {}
    id2entity = []
    id2relation = []
    id2etype = []

    edges_src = []
    edges_rel = []
    edges_dst = []

    def get_ent_id(ent: str):
        if ent in entity2id:
            return entity2id[ent]
        idx = len(id2entity)
        entity2id[ent] = idx
        id2entity.append(ent)
        et = parse_entity_type(ent)
        id2etype.append(et)
        return idx

    def get_rel_id(rel: str):
        if rel in relation2id:
            return relation2id[rel]
        idx = len(id2relation)
        relation2id[rel] = idx
        id2relation.append(rel)
        return idx

    for h, r, t in edge_iter:
        # relation filter (substring)
        if relations_keep:
            ok = any(k in r for k in relations_keep)
            if not ok:
                continue

        # entity type filter
        if entity_types_keep:
            ht = parse_entity_type(h)
            tt = parse_entity_type(t)
            if (ht not in entity_types_keep) or (tt not in entity_types_keep):
                continue

        hid = get_ent_id(h)
        rid = get_rel_id(r)
        tid = get_ent_id(t)

        edges_src.append(hid)
        edges_rel.append(rid)
        edges_dst.append(tid)

    return entity2id, relation2id, id2entity, id2relation, id2etype, edges_src, edges_rel, edges_dst

def make_edge_tensors(edges_src, edges_dst, edges_rel):
    edge_index = torch.tensor([edges_src, edges_dst], dtype=torch.long)
    edge_type = torch.tensor(edges_rel, dtype=torch.long)
    return edge_index, edge_type

def relation_counts(edge_type):
    c = Counter(edge_type.tolist())
    return dict(c)

def degree_hist(edge_index, num_nodes: int):
    deg = torch.zeros(num_nodes, dtype=torch.long)
    src = edge_index[0]
    dst = edge_index[1]
    deg.scatter_add_(0, src, torch.ones_like(src))
    deg.scatter_add_(0, dst, torch.ones_like(dst))
    return deg

def filter_edges_by_idx(edge_index, edge_type, keep_idx):
    keep_idx = torch.as_tensor(keep_idx, dtype=torch.long)
    ei = edge_index[:, keep_idx]
    et = edge_type[keep_idx]
    return ei, et
