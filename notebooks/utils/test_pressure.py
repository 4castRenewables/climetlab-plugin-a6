import numpy as np
import pytest
import xarray as xr

from . import pressure


def test_calculate_pressure():
    model_level = 1
    p_s = xr.DataArray([1.0, 2.0])
    constants = xr.Dataset(
        data_vars={
            "hyai": (
                ["dim0", "dim0_0"],
                [
                    [0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0],
                ],
            ),
            "hybi": (
                ["dim0", "dim0_0"],
                [
                    [0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0],
                ],
            ),
            "hyam": (
                ["dim0", "dim0_0"],
                [
                    [1.0, 2.0, 0.0],
                    [1.0, 2.0, 0.0],
                ],
            ),
            "hybm": (
                ["dim0", "dim0_0"],
                [
                    [1.0, 2.0, 0.0],
                    [1.0, 2.0, 0.0],
                ],
            ),
        },
        coords={
            "dim0": ("dim0", [0, 1]),
            "dim0_0": ("dim0_0", [0, 1, 2]),
        },
    )
    expected = xr.DataArray([3.0, 4.5])
    result = pressure.calculate_pressure(
        p_s=p_s,
        constants=constants,
        model_level=model_level,
    )

    np.testing.assert_equal(result.values, expected.values)


@pytest.mark.parametrize(
    ("p_s", "A_k", "B_k", "expected"),
    [
        (
            xr.DataArray([1.0, 1.0]),
            xr.DataArray([1.0, 1.0]),
            xr.DataArray([1.0, 1.0]),
            xr.DataArray([2.0, 2.0]),
        ),
        (
            xr.DataArray([2.0, 2.0]),
            xr.DataArray([1.0, 1.0]),
            xr.DataArray([2.0, 2.0]),
            xr.DataArray([5.0, 5.0]),
        ),
    ],
)
def test_calculate_pressure_levels(p_s, A_k, B_k, expected):
    result = pressure._calculate_pressure_levels(
        p_s=p_s,
        A_k=A_k,
        B_k=B_k,
    )

    xr.testing.assert_equal(result, expected)
