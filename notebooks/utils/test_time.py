import datetime

import pytest
import xarray as xr

from . import time


def test_get_time_of_day_and_year():
    dates = [datetime.datetime(2020, 1, 1), datetime.datetime(2020, 1, 1, 1)]

    expected_time_of_day = xr.DataArray(
        data=[0.0, 0.041667],
        coords={"time": dates},
    )
    expected_time_of_year = xr.DataArray(
        data=[0.0, 0.0],
        coords={"time": dates},
    )

    result_time_of_day, result_time_of_year = time.get_time_of_day_and_year(dates)

    xr.testing.assert_allclose(result_time_of_day, expected_time_of_day)
    xr.testing.assert_allclose(result_time_of_year, expected_time_of_year)


@pytest.mark.parametrize(
    ("dt", "expected"),
    [
        (datetime.datetime(2020, 1, 1), 0.0),
        (datetime.datetime(2020, 1, 1, 6), 0.25),
        (datetime.datetime(2020, 1, 1, 12), 0.5),
        (datetime.datetime(2020, 1, 1, 18), 0.75),
        (datetime.datetime(2020, 1, 2), 0.0),
    ],
)
def test_time_of_day(dt, expected):
    result = time._time_of_day(dt)

    assert result == expected


@pytest.mark.parametrize(
    ("dt", "expected"),
    [
        (datetime.datetime(2020, 1, 1), 0.0),
        (datetime.datetime(2020, 7, 2), 0.5),
        (datetime.datetime(2020, 12, 31), 1.0),
    ],
)
def test_time_of_year(dt, expected):
    result = time._time_of_year(dt)
    result_rounded = round(result, 2)

    assert result_rounded == expected
