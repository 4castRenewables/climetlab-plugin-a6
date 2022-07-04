import datetime
import typing as t

import numpy as np
import xarray as xr


def get_dates_from_time_coordinate(data: xr.Dataset) -> t.List[datetime.datetime]:
    """Get the time index/coordinate as a list of datetimes."""
    return data.coords["time"].to_index().to_list()


def get_time_of_day_and_year(
    dates: t.List[datetime.datetime], time_coord_name: str = "time"
) -> t.Tuple[xr.DataArray, xr.DataArray]:
    """Calculate the time of day and year for given datetimes."""
    time_of_day = get_time_of_day(dates, time_coord_name=time_coord_name)
    time_of_year = get_time_of_year(dates, time_coord_name=time_coord_name)
    return time_of_day, time_of_year


def get_time_of_day(
    dates: t.List[datetime.datetime], time_coord_name: str = "time"
) -> xr.DataArray:
    """Calculate relative time of day for datetimes."""
    converted = _apply_to_dates(_time_of_day, dates=dates)
    return xr.DataArray(
        data=converted,
        coords={time_coord_name: dates},
    )


def get_time_of_year(
    dates: t.List[datetime.datetime], time_coord_name: str = "time"
) -> xr.DataArray:
    """Calculate relative time of year for datetimes."""
    converted = _apply_to_dates(_time_of_year, dates=dates)
    return xr.DataArray(
        data=converted,
        coords={time_coord_name: dates},
    )


def _apply_to_dates(func: t.Callable, dates: t.List[datetime.datetime]) -> np.ndarray:
    return np.array(list(map(func, dates)))


def _time_of_day(dt: datetime) -> float:
    """Convert a given datetime `dt` to a point on the unit circle, where the 'period' corresponds to one day.

    :param datetime.datetime dt: input datetime UTC
    :returns: `float` between 0 and 1 corresponding to the phase
    """
    midnight = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds_since_midnight = (dt - midnight).total_seconds()
    return seconds_since_midnight / 86400


def _time_of_year(dt: datetime) -> float:
    """Convert a given datetime `dt` to a point on the unit circle, where the 'period' corresponds to one year.

    :param datetime.datetime dt: input datetime (preferably UTC)
    :returns: `float` between 0 and 1 corresponding to the phase

    This function makes a small mistake in leap years as it considers the length of the year to be 365d always.
    """
    # Convert to UTC before
    return (dt.timetuple().tm_yday - 1) / 365
