import xarray as xr

from . import wind


def test_calculate_wind_speed():
    u = xr.DataArray([3.0, 3.0, 3.0])
    v = xr.DataArray([4.0, 4.0, 4.0])
    expected = xr.DataArray([5.0, 5.0, 5.0])

    result = wind.calculate_absolute_wind_speed(
        wind_speed_east=u,
        wind_speed_north=v,
    )

    xr.testing.assert_equal(result, expected)


def test_calculate_wind_direction_angle():
    u = xr.DataArray([10.0])
    v = xr.DataArray([10.0])
    expected = xr.DataArray([45.0])

    result = wind.calculate_wind_direction_angle(
        wind_speed_east=u,
        wind_speed_north=v,
    )

    xr.testing.assert_equal(result, expected)
