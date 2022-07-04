import datetime

import numpy as np
import xarray as xr

from . import model


def test_prepare_x():

    dates = [datetime.datetime(2020, 1, 1), datetime.datetime(2020, 1, 2)]
    coords = {"time": dates}

    first = xr.DataArray(
        data=[1, 2],
        coords={"time": [datetime.datetime(2020, 1, 1), datetime.datetime(2020, 1, 2)]},
    )
    second = xr.DataArray(
        data=[2, 3],
        coords={"time": [datetime.datetime(2020, 1, 2), datetime.datetime(2020, 1, 3)]},
    )

    expected = [(2, 2)]

    result = model._prepare_x(
        "time",
        first,
        second,
    )

    np.testing.assert_equal(result, expected)
