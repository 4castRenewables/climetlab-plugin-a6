import xarray as xr


def calculate_pressure(
    p_s: xr.DataArray,
    constants: xr.Dataset,
    model_level: int,
) -> xr.DataArray:
    """Calculate the pressure at a certain model level.

    Parameters
    ----------
    p_s : xarray.DataArray
        Pressure at surface level.
    constants : xarray.Dataset
        Constants hayi, hybi, hyam, hybm as from the `maelstrom-constants-a-b` dataset.
    model_level : int
        Model level.

    Returns
    -------
    pandas.Series
        Pressure for a given model level.

    """
    upper_level_constants = constants.loc[{"dim0": 0, "dim0_0": model_level - 1}]
    model_level_constants = constants.loc[{"dim0": 0, "dim0_0": model_level}]
    A_1 = upper_level_constants["hyam"]
    A_2 = model_level_constants["hyam"]
    B_1 = upper_level_constants["hybm"]
    B_2 = model_level_constants["hybm"]
    p_1 = _calculate_pressure_levels(p_s, A_k=A_1, B_k=B_1)
    p_2 = _calculate_pressure_levels(p_s, A_k=A_2, B_k=B_2)
    p = 0.5 * (p_1 + p_2)
    return p


def _calculate_pressure_levels(
    p_s: xr.DataArray, A_k: xr.DataArray, B_k: xr.DataArray
) -> xr.DataArray:
    """Calculate the pressure for each model level.

    Parameters
    ----------
    p_s : float
        Pressure at surface level.
    A_k : xarray.DataArray
        Constant for each model level.
    B_k : xarray.DataArray
        Constant for each model level.

    Returns
    -------
    pandas.Series
        Pressure for each model level.

    """
    return A_k + B_k * p_s
