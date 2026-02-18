import numpy as np

def binary_metrics(y_true, y_score):

    y_true = np.asarray(y_true).astype(int)
    y_score = np.asarray(y_score).astype(float)
    out = {}

    try:
        from sklearn.metrics import roc_auc_score, average_precision_score
        out["roc_auc"] = float(roc_auc_score(y_true, y_score))
        out["pr_auc"] = float(average_precision_score(y_true, y_score))
    except Exception:
        # fallback: not exact AUC
        out["roc_auc"] = None
        out["pr_auc"] = None

    # threshold=0 for logits is common; if scores are probabilities, change yourself
    y_pred = (y_score >= 0).astype(int)
    acc = (y_pred == y_true).mean()
    out["accuracy@0"] = float(acc)
    return out

def sampled_ranking_metrics(pos_scores, neg_scores, ks=(1,3,10)):

    pos_scores = np.asarray(pos_scores).reshape(-1)
    neg_scores = np.asarray(neg_scores)
    N = len(pos_scores)
    K = neg_scores.shape[1]

    ranks = []
    for i in range(N):
        rank = 1 + int((neg_scores[i] > pos_scores[i]).sum())
        ranks.append(rank)

    ranks = np.array(ranks)
    mrr = float((1.0 / ranks).mean())

    out = {"mrr": mrr}
    for k in ks:
        out[f"hits@{k}"] = float((ranks <= k).mean())
    out["mean_rank"] = float(ranks.mean())
    out["num_test"] = int(N)
    out["num_negs_per_pos"] = int(K)
    return out
