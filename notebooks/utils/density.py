"""Functionality for calculating the density of air."""
from typing import Dict, Optional

import numpy as np
import xarray as xr

from .pressure import calculate_pressure

r_l = 287.05  # Gas constant of dry air [J/kg/K]
r_d = 461.523  # Gas constant of water [J/kg/K]
magnus_const1 = (
    6.1078,
    17.08085,
    234.175,
)  # Constants for Magnus' formula in case of :math:`\Theta \ge 0`
magnus_const2 = (
    6.1078,
    17.84362,
    245.425,
)  # Constants for Magnus' formula in case of :math:`\Theta < 0`."""
mol_quot = 18.01534 / 28.9644  # Quotient of molar masses of water and air."""


def calculate_air_density(
    grid_point: dict[str, float],
    model_level: int,
    model_level_data: xr.Dataset,
    surface_data: xr.Dataset,
    constants: xr.Dataset,
) -> xr.DataArray:
    """Calculate the air density from the model data.

    Parameters
    ----------
    grid_point : Dict[str, float]
        Grid point for which to calculate the air density.
    model_level : int
        Model level for which to calculate the air density.
    model_level_data : xarray.Dataset
        Model level data from the `maelstrom-weather-model-level` dataset.
    surface_data : xarray.Dataset
        Surface from the `maelstrom-weather-surface-level` dataset.
    constants : xarray.Dataset
        Constants data from the `maelstrom-constants-a-b` dataset.

    Returns
    -------
    xr.DataArray
        Air density for each time stamp.

    """
    model_level_index = {**grid_point, "level": model_level}
    pressure_at_surface = surface_data["sp"].loc[grid_point]
    pressure = calculate_pressure(
        p_s=pressure_at_surface,
        constants=constants,
        model_level=model_level,
    )  # expected pressure is roughly 1000 hPa (10^5 Pa)
    temperature = model_level_data.loc[model_level_index]["t"]
    specific_humidity = model_level_data.loc[model_level_index]["q"]
    air_density = _calculate_density(
        temperature=temperature,
        pressure=pressure,
        specific_humidity=specific_humidity,
    )
    return air_density


def _calculate_density(
    temperature: xr.DataArray,
    pressure: xr.DataArray,
    specific_humidity: xr.DataArray,
    relative_humidity: Optional[xr.DataArray] = None,
) -> xr.DataArray:
    """Calculate air density.

    :param pandas.Series temperature: temperature (ºC)
    :param pandas.Series pressure: pressure (mBar)
    :param pandas.Series specific_humidity: specific humidity
    :param pandas.Series relative_humidity: (optional) relative humidity in % (from 0-100)
    :returns pandas.Series: rho (g/m^3)

    Note that relative humidity and specific humidity are not both necessary to calculate the air
    density. `rh` serves as a backup in case `q` is None or numpy.nan.

    This way, a fallback value for `rh` can be chosen. This is better than one for `q` because one for `q` might
    become unphysical when temperature and pressure change.o
    """
    theta = temperature
    p = pressure
    q = specific_humidity
    rh = relative_humidity
    rh_from_q = _rh(theta, p, q)

    if rh is not None:
        ind = rh_from_q.isnull()
        rh_from_q[ind] = rh[ind] / 100

    #  That's all, we can do..
    return 100 * p / (_r_f(theta, p, rh_from_q) * (theta + 273.15))


def _rh(theta: xr.DataArray, p: xr.DataArray, q: xr.DataArray) -> xr.DataArray:
    """Calculate relative humidity from specific humidity.

    :param pandas.Series q: specific humidity
    :param pandas.Series p: pressure (mBar)
    :param pandas.Series theta: temperature ºC
    :returns: relative humidity (float btw 0 and 1)
    """
    p_d = _p_d(theta)
    f1 = 1 - mol_quot
    return q * (p - f1 * p_d) / ((1 - f1) * p_d)


def _p_d(theta: xr.DataArray) -> xr.DataArray:
    """Saturated vapor pressure of water in air using Magnus' formula.

    Automated change of coefficients according to temperature.

    :param pandas.Series theta: temperature (ºC)

    :returns: `pandas.Series`, approximated saturation vapor pressure
    """
    ind1 = theta >= 0
    ind2 = theta < 0
    p_d = xr.DataArray(
        data=[0.0 for _ in range(theta.size)],
        coords=theta.coords,
        dims=theta.dims,
        name="saturated vapor pressure",
    )
    p_d[ind1] = _magnus(theta[ind1], *magnus_const1)
    p_d[ind2] = _magnus(theta[ind2], *magnus_const2)
    return p_d


def _magnus(
    theta: xr.DataArray, c0: xr.DataArray, c1: xr.DataArray, c2: xr.DataArray
) -> xr.DataArray:
    """Calculate Magnus' formula using one set of coefficients.

    :param float theta: absolute temperature
    :param float ci: coefficients (take from :attr:`magnus_const1` or :attr:`magnus_const2`).

    :returns float: approximated saturation vapor pressure
    """
    return c0 * np.exp(c1 * theta / (c2 + theta))


def _r_f(theta: xr.DataArray, p: xr.DataArray, rh: xr.DataArray) -> xr.DataArray:
    """Calculate modified gas constant to accomodate for the water content of the air.

    :param float theta: temperature in ºC
    :param float p: pressure in mBar
    :param float rh: relative humidity (0<= rh <= 1)

    :returns float: tweaked gas constant
    """
    return r_l / (1 - rh * (_p_d(theta) / p) * (1 - r_l / r_d))
