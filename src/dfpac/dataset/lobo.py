import pandas as pd
from dfpac import settings
from dfpac.dataset.base import BaseDataset, DescriptorMixin, PSEMixin


def load_LOBO_dataset(kind: str, species: str) -> pd.DataFrame:
    data_dir = settings.DATA_DIR / kind / "lobo"
    pos = pd.read_parquet(data_dir / "training" / "positive.parquet")
    neg = pd.read_parquet(data_dir / "training" / "negative.parquet")
    data = pd.concat([pos, neg], axis=0, ignore_index=True)

    training_data = data[data.Species != species].copy()
    training_data = training_data.sample(frac=1.0)  # shuffle
    training_data["Partition"] = "train"

    test_data = data[data.Species == species].copy()
    test_data["Partition"] = "test"

    data = pd.concat([training_data, test_data], axis=0, ignore_index=True)
    return data


class LOBODescriptorDataset(BaseDataset, DescriptorMixin):
    def __init__(self, species: str) -> None:
        super().__init__(load_LOBO_dataset, kind="descriptors", species=species)
        self.species = species


class LOBOPSEDataset(BaseDataset, PSEMixin):
    def __init__(self, species: str) -> None:
        super().__init__(load_LOBO_dataset, kind="pses", species=species)
        self.species = species
