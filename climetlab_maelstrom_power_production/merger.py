import abc

import pandas as pd  # type: ignore
import xarray as xr


class AbstractMerger(abc.ABC):
    """Abstract base class for a source merger."""

    engine = "netcdf4"

    @abc.abstractmethod
    def to_pandas(self, paths, **kwargs) -> pd.DataFrame:
        """Merge multiple source files."""

    @abc.abstractmethod
    def to_xarray(self, paths, **kwargs) -> xr.Dataset:
        """Merge multiple source files."""

    def to_tfdataset(self, paths, **kwargs):
        """Merge multiple source files."""
        raise NotImplementedError("TensorFlow is not supported by this dataset yet")
