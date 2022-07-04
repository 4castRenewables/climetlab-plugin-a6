import datetime
from typing import Iterator, List

import numpy as np
import xarray as xr
from sklearn.ensemble import GradientBoostingRegressor


def train_model(
    air_density: xr.DataArray,
    absolute_wind_speed: xr.DataArray,
    wind_direction: xr.DataArray,
    time_of_day: xr.DataArray,
    time_of_year: xr.DataArray,
    production: xr.DataArray,
    time_coordinate_name: str = "time",
) -> GradientBoostingRegressor:
    """Train the model with the given features and production data.

    All given data must be of the same shape.

    """
    x = _prepare_x(
        time_coordinate_name,
        air_density,
        absolute_wind_speed,
        wind_direction,
        time_of_day,
        time_of_year,
    )
    y = production
    return GradientBoostingRegressor().fit(x, y)


def predict_power_production(
    model: GradientBoostingRegressor,
    air_density: xr.DataArray,
    absolute_wind_speed: xr.DataArray,
    wind_direction: xr.DataArray,
    time_of_day: xr.DataArray,
    time_of_year: xr.DataArray,
    time_coordinate_name: str = "time",
) -> xr.DataArray:
    """Predict the power production from given features.

    Features need to be identical to those used to train the model.

    """
    x = _prepare_x(
        time_coordinate_name,
        air_density,
        absolute_wind_speed,
        wind_direction,
        time_of_day,
        time_of_year,
    )
    production = model.predict(x)
    return np.array(production)


def _prepare_x(time_coordinate_name: str, *args: xr.DataArray) -> List:
    intersecting_dates = _get_intersecting_dates(time_coordinate_name, *args)
    intersecting_data = _select_subset(intersecting_dates, time_coordinate_name, *args)
    return list(zip(*intersecting_data))


def _get_intersecting_dates(
    time_coordinate_name: str, *args: xr.DataArray
) -> xr.DataArray:
    if len(args) == 0:
        return args[time_coordinate_name]
    first, rest = args[0], args[1:]
    intersection = set(first[time_coordinate_name].values)
    for arg in rest:
        intersection = intersection & set(arg[time_coordinate_name].values)
    return sorted(intersection)


def _select_subset(
    dates: List[datetime.datetime], time_coordinate_name: str, *args
) -> Iterator[np.ndarray]:
    for arg in args:
        yield arg.sel({time_coordinate_name: dates}).values
