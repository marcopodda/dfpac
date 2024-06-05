import logging

import numpy as np
import pandas as pd
from dfpac import settings
from dfpac.dataset.proteome import load_proteome
from dfpac.evaluation.metrics import SCORERS, nadr
from dfpac.utils.misc import seed_everything

log = logging.getLogger(__name__)


def rank_bio(df: pd.DataFrame) -> pd.Index:
    indices = np.random.permutation(len(settings.BIO_DESCRIPTORS))
    BIO_DESCRIPTORS = [settings.BIO_DESCRIPTORS[i] for i in indices]
    return df.sort_values(BIO_DESCRIPTORS, ascending=False).index


def rank_prob(df: pd.DataFrame) -> pd.Index:
    return df.PAProb.sort_values(ascending=False).index


def _cumsum(series: pd.Series) -> np.ndarray:
    values = np.cumsum(series).values
    return values.astype(int)


def _score_pipeline(pipeline: str, experiment: str, species: str) -> pd.DataFrame:
    root = settings.EXP_DIR / experiment / pipeline

    if species is not None:
        root = root / species

    rows = []
    for seed in range(1, 11):
        path = root / f"{seed}" / "scores.csv"
        if path.exists():
            scores = {"Pipeline": pipeline}
            if species is not None:
                scores.update(Species=species)

            scores |= pd.read_csv(path).iloc[0].to_dict()
            if species is not None:
                scores.pop("PREC")
                scores.pop("REC")
            rows.append(scores)
    return pd.DataFrame(rows)


def get_scores(experiment: str, species: str | None = None, pipelines: list[str] = settings.PIPELINES) -> pd.DataFrame:
    scores = [_score_pipeline(p, experiment, species) for p in pipelines]
    return pd.concat(scores, axis=0, ignore_index=True)


def get_nadr(pipeline: str, species: str, rv: bool = False) -> pd.DataFrame:
    root = settings.EXP_DIR / "lobo" / pipeline / species

    rows = []
    for seed in range(1, 11):
        path = root / f"{seed}" / "predictions_proteome.csv"
        if path.exists():
            df = pd.read_csv(path)
            if rv is True:
                df = df.iloc[rank_bio(df), :]
            df = df.sort_values("PAProb", ascending=False).reset_index()
            scores = {"Species": species, "Pipeline": pipeline}
            scores.update(nADR=nadr(df.Antigen.values))
            antigens = df.Antigen[df.Antigen == True]  # noqa
            scores.update(FHI=antigens.index[0])
            rows.append(scores)
    return pd.DataFrame(rows)


def get_nadr_rv(species: str) -> pd.DataFrame:
    proteome = load_proteome("descriptors", species=species)

    root = settings.EXP_DIR / "lobo" / "descriptors" / species

    rows = []
    for seed in range(1, 11):
        seed_everything(seed)

        path = root / f"{seed}" / "predictions_proteome.csv"
        if path.exists():
            df = pd.read_csv(path)
            df = df.iloc[rank_bio(proteome), :].reset_index(drop=True)
            scores = {"Species": species, "Pipeline": "RV"}
            scores.update(nADR=nadr(df.Antigen.values))
            antigens = df.Antigen[df.Antigen == True]  # noqa
            scores.update(FHI=antigens.index[0])
            rows.append(scores)
    return pd.DataFrame(rows)


def get_lobo_nadr(species: str) -> pd.DataFrame:
    scores = [get_nadr(p, species) for p in settings.NADR_PIPELINES]
    scores.append(get_nadr_rv(species))
    return pd.concat(scores, axis=0, ignore_index=True)


def get_discovery_curves_bio(species: str, seed: int) -> np.ndarray:
    root = settings.EXP_DIR / "lobo" / "descriptors" / species / f"{seed}"
    path = root / "predictions_proteome.csv"

    if not path.exists():
        return np.empty

    results = pd.read_csv(path)
    descriptors = load_proteome(kind="descriptors", species=species)
    return _cumsum(results.Antigen.iloc[rank_bio(descriptors)])


def get_discovery_curves_feat(species: str, seed: int) -> np.ndarray:
    root = settings.EXP_DIR / "lobo" / "descriptors" / species / f"{seed}"
    path = root / "predictions_proteome.csv"

    if not path.exists():
        return np.empty

    results = pd.read_csv(path)
    return _cumsum(results.Antigen.iloc[rank_prob(results)])


def get_discovery_curves_emb(species: str, seed: int) -> np.ndarray:
    root = settings.EXP_DIR / "lobo" / "pses" / species / f"{seed}"
    path = root / "predictions_proteome.csv"

    if not path.exists():
        return np.empty

    results = pd.read_csv(path)
    return _cumsum(results.Antigen.iloc[rank_prob(results)])


def get_discovery_curves(species: str) -> pd.DataFrame:
    dfs = []
    for seed in range(1, 11):
        df = pd.DataFrame(
            {
                "RV": get_discovery_curves_bio(species, seed),
                "PSEs": get_discovery_curves_emb(species, seed),
            }
        )
        df["Pre-clinical trials"] = np.arange(df.shape[0])

        melted = df.melt(
            value_vars=df.columns[:3].tolist(),
            id_vars=("Pre-clinical trials",),
            value_name="Antigens Discovered",
            var_name="Method",
        )
        melted["Species"] = species
        dfs.append(melted)

    return pd.concat(dfs, axis=0, ignore_index=True)


def evaluate(model, dataset):
    scores = {}
    for name, scorer in SCORERS.items():
        scores[name] = scorer(model, dataset.X_test, dataset.y_test)

    log.info(f"Scores: {scores}")
    pd.DataFrame([scores]).round(4).to_csv("scores.csv", index=False)


def predict_test(model, dataset, filename):
    test_set = dataset.test_set
    test_set["PAProb"] = model.predict_proba(dataset.X_test)[:, 1]
    test_set = test_set.sort_values("PAProb", ascending=False)
    test_set.round(3).to_csv(filename, index=False)
