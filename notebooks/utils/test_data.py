import datetime

import numpy as np
import pandas as pd
import pytest
import xarray as xr

from . import data


def test_get_wind_turbine_coordinates():
    ds = xr.Dataset(
        {
            "longitude": ([1]),
            "latitude": ([2]),
        }
    )
    expected = (1, 2)

    result = data._get_wind_turbine_coordinates(ds)

    assert result == expected


def test_get_grid_coordinates():
    ds = xr.Dataset(
        data_vars={
            "test_var": (["longitude", "latitude"], [[1, 2], [1, 2]]),
        },
        coords={
            "longitude": ("longitude", [1.0, 2.0]),
            "latitude": ("latitude", [1.0, 2.0]),
        },
    )
    expected = np.array([1.0, 2.0])

    result = data._get_grid_coordinates(ds, coordinate="longitude")

    np.testing.assert_equal(result, expected)


@pytest.mark.parametrize(
    ("grid", "coordinates", "expected"),
    [
        (
            np.array([[3, 2, 1], [3, 2, 1]]),
            (1.4, 1.4),
            (1, 1),
        ),
        (
            np.array([[3, 1, 2], [3, 2, 1]]),
            (1.6, 1.6),
            (2, 2),
        ),
        (
            np.array([[1, 2, 3], [1, 2, 3]]),
            (1.4, 1.6),
            (1, 2),
        ),
    ],
)
def test_get_closest_grid_point(grid, coordinates, expected):
    result = data._get_closest_grid_point(grid, coordinates=coordinates)

    assert result == expected


@pytest.mark.parametrize(
    ("coordinates", "value", "expected"),
    [
        (
            np.array([1, 2, 3]),
            1.4,
            1,
        ),
        (
            np.array([10.0, 20.0, 30.0]),
            16.0,
            20.0,
        ),
        (
            np.array([30.0, 10.0, 20.0]),
            16.0,
            20.0,
        ),
    ],
)
def test_get_closest_coordinate(coordinates, value, expected):
    result = data._get_closest_coordinate(coordinates, value=value)

    assert result == expected


def test_resample_and_clear_production_data_to_hourly_timeseries():
    weather_data_dates = pd.date_range(
        start=datetime.datetime(2020, 1, 1),
        end=datetime.datetime(2020, 1, 3),
        freq="1H",
    )
    # Different dates of weather and production data throws error:
    # KeyError: "[Timestamp('2020-01-01 00:00:00'), ...] not in index"
    production_data_dates = pd.date_range(
        start=datetime.datetime(2020, 1, 2),
        end=datetime.datetime(2020, 1, 3),
        freq="10min",
    )
    production_data = np.array(range(len(production_data_dates)))
    # Reshape data to match dimensions time, level, latitude, longitude
    production_data = production_data.reshape(len(production_data_dates), 1, 1, 1)

    production = xr.Dataset(
        data_vars={
            "production": (
                ["time", "level", "latitude", "longitude"],
                production_data,
            ),
        },
        coords={
            "time": production_data_dates,
            "level": ([0]),
            "latitude": ([2]),
            "longitude": ([1]),
        },
    )

    expected_dates = pd.date_range(
        start=datetime.datetime(2020, 1, 2),
        end=datetime.datetime(2020, 1, 3),
        freq="1H",
    )

    averages = []
    for n_hours, _ in enumerate(expected_dates):
        avg = np.mean(production_data[n_hours * 6 : (n_hours + 1) * 6])
        averages.append(avg)

    expected = xr.DataArray(
        data=averages,
        coords={
            "time": expected_dates,
        },
    )

    result = data.resample_and_clear_production_data_to_hourly_timeseries(
        production,
        dates=weather_data_dates,
    )

    xr.testing.assert_equal(result, expected)


def test_resample_production_data_to_hourly_timeseries():
    dates = pd.date_range(
        start=datetime.datetime(2020, 1, 1),
        end=datetime.datetime(2020, 1, 1, 1),
        freq="10min",
    )
    production_data = range(len(dates))
    average_first_hour = np.mean(production_data[:-1])
    average_second_hour = np.mean(production_data[-1:])
    production = pd.DataFrame(
        [[value] for value in production_data],
        columns=["production"],
        index=pd.MultiIndex.from_arrays(
            [list(range(len(dates))), dates], names=["longitude", "time"]
        ),
    )
    expected = pd.Series(
        data=[average_first_hour, average_second_hour],
        index=pd.DatetimeIndex(
            [datetime.datetime(2020, 1, 1), datetime.datetime(2020, 1, 1, 1)],
            name="time",
            freq="H",
        ),
        name="production",
    )

    result = data._resample_production_data_to_hourly_timeseries(production)

    pd.testing.assert_series_equal(result, expected)
