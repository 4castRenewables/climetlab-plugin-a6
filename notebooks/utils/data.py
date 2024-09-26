from datetime import datetime
from typing import Dict, List, Set, Tuple, Union

import numpy as np
import pandas as pd
import xarray as xr

Number = Union[int, float]


def get_closest_grid_point_to_wind_turbine(
    production_data: xr.Dataset,
    data: xr.Dataset,
) -> dict[str, Number]:
    """Get the grid point in the data closest to the wind turbine.

    Parameters
    ----------
    production_data : xarray.Datases
        Production data from the `maelstrom-power-production` dataset.
        Needs to be of type `xarray.Dataset` since its header contains
        the meta information with the wind turbine's coordinates.
    data : pandas.DataFrame
        The data either from the `maelstrom-weather-model-level` or
        `maelstrom-weather-pressure-level` dataset. These contain the
        grid points.

    Returns
    -------
    dict[str, float]
        Grid point coordinates that are closest to the wind turbine.

    """
    turbine_coordinates = _get_wind_turbine_coordinates(production_data)
    grid = [
        _get_grid_coordinates(data, "longitude"),
        _get_grid_coordinates(data, "latitude"),
    ]
    longitude, latitude = _get_closest_grid_point(grid, coordinates=turbine_coordinates)
    return {"longitude": longitude, "latitude": latitude}


def _get_wind_turbine_coordinates(ds: xr.Dataset) -> tuple[Number, Number]:
    """Get the coordinates (longitude, latitude) of a wind turbine from the production data.

    Parameters
    ----------
    ds : xarray.Dataset
        The production data from the dataset `maelstrom-power-production`.

    Returns
    -------
    tuple
        Longitude and latitude of the wind turbine.

    """
    coordinates = ds.coords
    longitude = coordinates["longitude"].values[0]
    latitude = coordinates["latitude"].values[0]
    return longitude, latitude


def _get_grid_coordinates(ds: xr.Dataset, coordinate: str) -> np.ndarray:
    """Get the unique coordinates (longitude and latitude) from a series.

    Parameters
    ----------
    ds : xarray.Dataset
        Dataset with coordinates as index.
    coordinate : t.List[str], default ["longitude", "latitude"]
        The coordinates to get as a dataframe.

    Returns
    -------
    np.ndarray
        Contains the unique coordinates as columns.

    """
    return np.round(ds.coords[coordinate].values.astype(float), 1)


def _get_closest_grid_point(
    grid: list[np.ndarray], coordinates: tuple[Number, ...]
) -> tuple[Union[int, float], ...]:
    """Get the grid point that is closest to the given coordinates.

    Parameters
    ----------
    grid : t.List[list, list]
        List with two lists, each representing coordinates.
        For each coordinate, the value closest to the respective value at
        the same column of the tuple will be returned.
    coordinates : tuple
        Coordinates whose closest grid point to get from `grid`.
        The first value will find the closest value in the first column
        of `coordinates`, the second value that in the second column.

    Returns
    -------
    tuple
        The closest values in each column of `grid`.

    """
    closest_values = (
        _get_closest_coordinate(
            axis,
            value=coordinates[index],
        )
        for index, axis in enumerate(grid)
    )
    return tuple(closest_values)


def _get_closest_coordinate(coordinates: np.ndarray, value: Number) -> Number:
    exact_match = [coordinate for coordinate in coordinates if coordinate == value]
    if exact_match:
        [match] = exact_match
        return match
    return min(coordinates, key=lambda x: abs(x - value))


def resample_and_clear_production_data_to_hourly_timeseries(
    production_data: xr.Dataset,
    dates: list[datetime],
) -> xr.DataArray:
    """Resample the production data to an hourly timeseries and clear negative values.

    Parameters
    ----------
    production_data : pandas.DataFrame
        Production data from the `maelstrom-power-production` dataset.
    dates : List[datetime]
        Dates from the weather data to get all matching timestamps of the resample.

    Returns
    -------
    xr.DataArray
        Production data resampled to an hourly time series.
        The data are averaged (mean) over the time windows.
        Negative values are set to 0.

    """
    resampled = _resample_production_data_to_hourly_timeseries(
        production_data.to_dataframe()
    )

    dates_intersection = _get_intersection_of_dates(resampled, dates)
    resampled_and_matching_dates = resampled.loc[dates_intersection]
    resampled_and_matching_dates[resampled_and_matching_dates < 0.0] = 0.0

    if resampled_and_matching_dates.size == 0:
        raise RuntimeError(
            "Resampled production data have no temporal intersection with given dates"
        )

    return resampled_and_matching_dates.to_xarray()


def _resample_production_data_to_hourly_timeseries(
    production: pd.DataFrame,
    time_index_name: str = "time",
    production_column_name: str = "production",
) -> pd.Series:
    """Resample the production data to an hourly timeseries."""
    production_copy = production.copy()
    production_copy.reset_index(inplace=True)
    production_copy = production_copy.set_index(time_index_name)
    return production_copy[production_column_name].resample("1h").mean()


def _get_intersection_of_dates(
    left: pd.DataFrame, right: list[datetime]
) -> set[pd.Timestamp]:
    return sorted(set(left.index) & set(right))


def get_power_rating(
    data: xr.Dataset, power_rating_attribute_name: str = "power rating [kW]"
) -> float:
    """Get the power rating of a wind turbine."""
    return float(data.attrs[power_rating_attribute_name])
