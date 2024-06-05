import pandas as pd
from dfpac import settings
from dfpac.dataset.base import BaseProteome, DescriptorMixin, PSEMixin


def load_proteome(kind: str, species: str) -> pd.DataFrame:
    data_dir = settings.DATA_DIR / kind / "lobo" / "training"
    pos_df = pd.read_parquet(data_dir / "positive.parquet")
    pos_df = pos_df[(pos_df.Species == species) & pos_df.Loc.isin(settings.OUTER)]
    data_dir = settings.DATA_DIR / kind / "lobo" / "test"
    df = pd.read_parquet(data_dir / f"{settings.SPECIES2PROT[species]}.parquet")
    df["Antigen"] = df["Antigen"].astype(bool)
    df.loc[df.Seq.isin(pos_df.Seq), "Antigen"] = True
    df = pd.concat([pos_df, df], axis=0, ignore_index=True)
    df = df.drop_duplicates("Seq")
    return df.reset_index(drop=True)


class ProteomeDescriptorDataset(BaseProteome, DescriptorMixin):
    def __init__(self, species: str) -> None:
        super().__init__(load_proteome, kind="descriptors", species=species)
        self.species = species


class ProteomeEmbeddingDataset(BaseProteome, PSEMixin):
    def __init__(self, species: str) -> None:
        super().__init__(load_proteome, kind="pses", species=species)
        self.species = species
