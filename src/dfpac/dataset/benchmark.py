import pandas as pd
from dfpac import settings
from dfpac.dataset.base import BaseDataset, PSEMixin


def load_benchmark_dataset(kind: str) -> pd.DataFrame:
    data_dir = settings.DATA_DIR / kind / "benchmark"
    pos = pd.read_parquet(data_dir / "training" / "positive.parquet")
    neg = pd.read_parquet(data_dir / "training" / "negative.parquet")

    training_data = pd.concat([pos, neg], axis=0, ignore_index=True)
    training_data = training_data.sample(frac=1.0)  # shuffle
    training_data["Partition"] = "train"

    test_data = pd.read_parquet(data_dir / "test" / "test.parquet")
    test_data["Partition"] = "test"

    data = pd.concat([training_data, test_data], axis=0, ignore_index=True)
    return data


class BenchmarkPSEDataset(BaseDataset, PSEMixin):
    def __init__(self) -> None:
        super().__init__(load_benchmark_dataset, kind="pses")
