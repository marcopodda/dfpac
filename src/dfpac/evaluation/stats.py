import pandas as pd
from dfpac import settings
from scipy import stats


def hypergeom(df, quant):
    subset = df[quant]
    ls = subset.shape[0]
    return stats.hypergeom.sf(df[:ls].Antigen.sum(), df.shape[0], df.Antigen.sum(), df[:ls].shape[0])


def fold_enrichment(species):
    root_dir = settings.EXP_DIR / "lobo" / "pses" / species
    dfs = pd.concat([pd.read_csv(p) for p in root_dir.glob("**/predictions_proteome.csv")], axis=0, ignore_index=True)
    dfs = dfs.groupby("ID").mean("PAProb").reset_index().sort_values("PAProb", ascending=False)
    perc90 = dfs.PAProb >= dfs.PAProb.quantile(0.9)
    obs = dfs[perc90].Antigen.sum()
    exp = dfs[perc90].shape[0] * (dfs.Antigen.sum() / dfs.shape[0])
    recall = dfs[perc90].Antigen.sum() / dfs.Antigen.sum()
    return {
        "Species": species,
        "Size": dfs.shape[0],
        "90th Perc.": perc90.sum(),
        "Exp.": exp,
        "Obs.": round(obs),
        "Fold Inc.": obs / exp,
        "Recall": recall,
        "PVal.": hypergeom(dfs, perc90),
    }


def get_fold_enrichment():
    rows = [fold_enrichment(sp) for sp in settings.SPECIES]
    return pd.DataFrame(rows)
