import abc
import typing as t

import climetlab as cml  # type: ignore
import pandas as pd  # type: ignore
from climetlab.sources import url  # type: ignore

from climetlab_maelstrom_power_production import config

from . import merger

BASE_PATTERN = "{url}/MAELSTROM_AP6/"


class AbstractDataset(cml.Dataset):
    """Abstract base class for a dataset."""

    home_page = config.GITHUB_REPO_URL
    citation = "-"
    licence = "-"
    terms_of_use = (
        "By downloading data from this dataset, you agree to the terms and conditions defined at "
        f"{config.GITHUB_REPO_URL}/LICENSE. If you do not agree with such terms, do not download the data."
    )
    dataset = None
    _as_dataframe = None
    _merger: t.Optional[merger.AbstractMerger] = None

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Name of the dataset."""

    @property
    @abc.abstractmethod
    def documentation(self) -> str:
        """Name of the dataset."""

    @property
    @abc.abstractmethod
    def url_pattern(self) -> str:
        """URL pattern of the dataset."""

    @abc.abstractmethod
    def _get_data(self) -> url.Url:
        """Get the data of the dataset."""

    @property
    def merger(self) -> t.Optional[merger.AbstractMerger]:
        """Get the merger for the source files."""
        return self._merger

    def _load_source(self, **kwargs) -> cml.Source:
        request = {"url": config.ECMWF_CLOUD_URL, **kwargs}
        pattern = BASE_PATTERN + self.url_pattern
        if self.merger is not None:
            return cml.load_source(
                "url-pattern", pattern, merger=self.merger, **request
            )
        return cml.load_source("url-pattern", pattern, **request)

    def to_dataframe(self) -> pd.DataFrame:
        """Convert data to dataframe."""
        if self._as_dataframe is None:
            dataset = self.to_xarray()
            self._as_dataframe = dataset.to_dataframe()
        return self._as_dataframe
