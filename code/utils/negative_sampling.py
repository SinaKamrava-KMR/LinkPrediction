
import random

def build_pair_set(heads, tails):
    return set(zip(heads, tails))

def sample_negatives_for_pairs(pos_heads, pos_tails, tail_candidates, existing_pairs_set,
                               num_negs_per_pos=1, seed=42):

    rng = random.Random(seed)
    neg_h, neg_t = [], []

    tail_candidates = list(tail_candidates)
    if len(tail_candidates) == 0:
        raise ValueError("tail_candidates is empty!")

    for h, t in zip(pos_heads, pos_tails):
        for _ in range(num_negs_per_pos):
            for _try in range(50):  # avoid infinite loops
                t2 = rng.choice(tail_candidates)
                if (h, t2) not in existing_pairs_set:
                    neg_h.append(h)
                    neg_t.append(t2)
                    break
            else:

                t2 = rng.choice(tail_candidates)
                neg_h.append(h)
                neg_t.append(t2)

    return neg_h, neg_t

def sample_negatives_on_the_fly(batch_heads, tail_candidates, existing_pairs_set,
                               num_negs_per_pos=1, seed=0):
    rng = random.Random(seed)
    tail_candidates = list(tail_candidates)
    neg_h, neg_t = [], []
    for h in batch_heads:
        for _ in range(num_negs_per_pos):
            for _try in range(30):
                t2 = rng.choice(tail_candidates)
                if (h, t2) not in existing_pairs_set:
                    neg_h.append(h)
                    neg_t.append(t2)
                    break
            else:
                t2 = rng.choice(tail_candidates)
                neg_h.append(h)
                neg_t.append(t2)
    return neg_h, neg_t
