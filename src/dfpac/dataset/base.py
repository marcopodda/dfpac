from abc import ABC

import pandas as pd


class BaseDataset(ABC):
    meta_columns: list[str] = ["ID", "Species", "Antigen"]

    def __init__(self, loader, **loader_kwargs):
        self._X_train: pd.DataFrame | None = None
        self._y_train: pd.Series | None = None
        self._X_test: pd.DataFrame | None = None
        self._y_test: pd.Series | None = None
        self._test_set: pd.DataFrame | None = None
        self.dataset = loader(**loader_kwargs)

    @property
    def X_train(self) -> pd.DataFrame:
        if self._X_train is None:
            data = self.dataset[self.dataset.Partition == "train"]
            self._X_train = data[self.attributes].reset_index(drop=True)
        return self._X_train

    @property
    def y_train(self) -> pd.Series:
        if self._y_train is None:
            data = self.dataset[self.dataset.Partition == "train"]
            self._y_train = data.Antigen.astype(int)
        return self._y_train

    @property
    def X_test(self) -> pd.DataFrame:
        if self._X_test is None:
            data = self.dataset[self.dataset.Partition == "test"]
            self._X_test = data[self.attributes]
        return self._X_test

    @property
    def y_test(self) -> pd.Series:
        if self._y_test is None:
            data = self.dataset[self.dataset.Partition == "test"]
            self._y_test = data.Antigen.astype(int)
        return self._y_test

    @property
    def test_set(self) -> pd.DataFrame:
        if self._test_set is None:
            data = self.dataset[self.dataset.Partition == "test"]
            self._test_set = data[self.meta_columns].reset_index(drop=True)
        return self._test_set.copy()


class BaseProteome(ABC):
    meta_columns: list[str] = ["ID", "Species", "Antigen"]

    def __init__(self, loader, **loader_kwargs):
        self._X_test: pd.DataFrame | None = None
        self._y_test: pd.Series | None = None
        self._test_set: pd.DataFrame | None = None
        self.dataset = loader(**loader_kwargs)

    @property
    def X_test(self) -> pd.DataFrame:
        if self._X_test is None:
            self._X_test = self.dataset[self.attributes]
        return self._X_test

    @property
    def y_test(self) -> pd.Series:
        if self._y_test is None:
            self._y_test = self.dataset.Antigen.astype(int)
        return self._y_test

    @property
    def test_set(self) -> pd.DataFrame:
        if self._test_set is None:
            self._test_set = self.dataset[self.meta_columns].reset_index(drop=True)
        return self._test_set.copy()


class PSEMixin:
    @property
    def attributes(self) -> list[str]:
        columns = self.dataset.columns[7:].tolist()
        if "Partition" in columns:
            columns.remove("Partition")
        return columns

    @property
    def num_attributes(self) -> int:
        return len(self.attributes)


class DescriptorMixin:
    @property
    def attributes(self) -> list[str]:
        columns = self.dataset.columns[7:].tolist()
        if "Partition" in columns:
            columns.remove("Partition")
        return columns

    @property
    def num_attributes(self) -> int:
        return len(self.attributes)
