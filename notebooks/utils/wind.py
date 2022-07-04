import typing as t

import numpy as np
import xarray as xr


def calculate_absolute_wind_speed_and_wind_direction(
    grid_point: t.Dict[str, float],
    model_level: int,
    model_level_data: xr.Dataset,
) -> t.Tuple[xr.DataArray, xr.DataArray]:
    """Calculate the absolute wind speed and wind direction.

    Parameters
    ----------
    grid_point : t.Tuple[float, float]
        Grid point for which to calculate the wind properties.
    model_level : int
        Model level for which to calculate the wind properties.
    model_level_data : pandas.DataFrame
        Model level data from the `maelstrom-weather-model-level` dataset.


    Returns
    -------
    t.Tuple[pandas.Series, pandas.Series]
        Absolute wind speed and wind direction (angle relative to longitude).

    """
    model_level_index = {**grid_point, "level": model_level}
    wind_speed_east = model_level_data.loc[model_level_index]["u"]
    wind_speed_north = model_level_data.loc[model_level_index]["v"]
    absolute_wind_speed = calculate_absolute_wind_speed(
        wind_speed_east,
        wind_speed_north,
    )
    wind_direction = calculate_wind_direction_angle(
        wind_speed_east=wind_speed_east,
        wind_speed_north=wind_speed_north,
    )
    return absolute_wind_speed, wind_direction


def calculate_absolute_wind_speed(
    wind_speed_east: xr.DataArray, wind_speed_north: xr.DataArray
) -> xr.DataArray:
    """Calculate the absolte wind speed.

    Parameters
    ----------
    wind_speed_east : xr.DataArray
        Wind speed in East direction.
    wind_speed_north : xr.DataArray
        Wind speed in North direction.

    Returns
    -------
    xr.DataArray
        Absolute wind speed.

    """
    return np.sqrt(wind_speed_east**2 + wind_speed_north**2)


def calculate_wind_direction_angle(
    wind_speed_east: xr.DataArray, wind_speed_north: xr.DataArray
) -> xr.DataArray:
    """Calculate wind direction angle relative to longitude.

    Parameters
    ----------
    wind_speed_east : xr.DataArray
        Wind speed in East direction.
    wind_speed_north : xr.DataArray
        Wind speed in North direction.

    Returns
    -------
    xr.DataArray
        Wind direction angle relative to longitude in degrees.

    """
    angle = _calculate_angle_to_equator(
        opposite=wind_speed_north, adjacent=wind_speed_east
    )
    return 90.0 - angle


def _calculate_angle_to_equator(
    opposite: xr.DataArray, adjacent: xr.DataArray
) -> xr.DataArray:
    angle_in_rad = np.arctan(opposite / adjacent)
    return _rad_to_deg(angle_in_rad)


def _rad_to_deg(angle: xr.DataArray) -> xr.DataArray:
    return angle * 360.0 / (2 * np.pi)
