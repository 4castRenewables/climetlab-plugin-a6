#!/usr/bin/env python3# (C) Copyright 2021 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#
import typing as t

import pandas as pd  # type: ignore
import xarray as xr

from climetlab_maelstrom_power_production import merger


class WeatherMerger(merger.AbstractMerger):
    """A merger for the weather data."""

    # Coordinate to use for merging multiple datasets.
    concat_dim = "time"

    def __init__(self, options: t.Optional[dict] = None):
        """Initialize the merger."""
        self.options = options or {}

    def to_pandas(self, paths, **kwargs) -> pd.DataFrame:
        """Merge a set of files into a single DataFrame."""
        return self.to_xarray(paths, **kwargs).to_dataframe()

    def to_xarray(self, paths, **kwargs) -> xr.Dataset:
        """Merge a set of files into a single dataset."""
        return xr.open_mfdataset(
            paths,
            engine=self.engine,
            concat_dim=self.concat_dim,
            combine="nested",
            coords="minimal",
            data_vars="minimal",
            preprocess=self._slice_first_twelve_hours,
            compat="override",
            parallel=True,
            **self.options,
        )

    def _slice_first_twelve_hours(self, dataset: xr.Dataset) -> xr.Dataset:
        """Cut an hourly dataset after the first 12 hours.

        This is necessary to overwrite older model runs with newer ones.

        Models are calculated at 00:00 and 12:00 for 48 hours each. Hence,
        when using two model runs, one always wants the newer values of the
        recent run to overwrite the older ones.

        """
        return dataset.isel({self.concat_dim: slice(None, 12)})
