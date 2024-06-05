import numpy as np
from sklearn import metrics

SCORERS = {
    "AUROC": metrics.make_scorer(metrics.roc_auc_score, response_method="predict_proba", average="weighted"),
    "AUPR": metrics.make_scorer(metrics.average_precision_score, response_method="predict_proba"),
    "WF1": metrics.make_scorer(metrics.f1_score, average="weighted"),
    "MCC": metrics.make_scorer(metrics.matthews_corrcoef),
    "PREC": metrics.make_scorer(metrics.precision_score, average="weighted", zero_division=0),
    "REC": metrics.make_scorer(metrics.recall_score, average="weighted", zero_division=0),
}


def nadr(y_ranked: np.ndarray) -> float:
    # ideal vector has all 1s in first n positions
    ideal = np.zeros_like(y_ranked)
    ideal[: y_ranked.sum()] = 1

    penalty = np.linspace(ideal.shape[0], 0)
    penalty = penalty.max()

    area = np.cumsum(y_ranked)
    area = (area / penalty).sum()

    ideal_area = np.cumsum(ideal)
    ideal_area = (ideal_area / penalty).sum()

    if ideal_area == 0.0:
        return 0.0

    return area / ideal_area
