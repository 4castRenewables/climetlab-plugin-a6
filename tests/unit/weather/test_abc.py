from contextlib import nullcontext as doesnotraise
from datetime import datetime

import pytest

from climetlab_maelstrom_power_production.weather import abc


@pytest.mark.parametrize(
    ("date", "expected"),
    [
        ("2019-01-01", [datetime(2019, 1, 1)]),
        ("2000-01-01", abc.DateUnavailableException()),
        (["2019-01-01", "2019-01-02"], [datetime(2019, 1, 1), datetime(2019, 1, 2)]),
    ],
)
def test_convert_dates(date, expected):
    with pytest.raises(type(expected)) if isinstance(
        expected, Exception
    ) else doesnotraise():
        result = abc._convert_dates(date)

        assert result == expected


@pytest.mark.parametrize(
    ("date", "expected"),
    [
        ("2020-01-01", datetime(2020, 1, 1)),
        ("01-01-2020", abc.IncorrectDateFormatException()),
    ],
)
def test_convert_to_datetime(date, expected):
    with pytest.raises(type(expected)) if isinstance(
        expected, Exception
    ) else doesnotraise():
        result = abc._convert_to_datetime(date)

        assert result == expected


@pytest.mark.parametrize(
    ("date", "expected"),
    [
        ([datetime(2019, 1, 1)], None),
        ([datetime(2000, 1, 1)], abc.DateUnavailableException()),
    ],
)
def test_check_dates_availability(date, expected):
    with pytest.raises(type(expected)) if isinstance(
        expected, Exception
    ) else doesnotraise():
        result = abc._check_dates_availability(date)

        assert result == expected


@pytest.mark.parametrize(
    ("date", "expected"),
    [
        (datetime(2019, 1, 1), True),
        (datetime(2000, 1, 1), False),
    ],
)
def test_date_is_available(date, expected):
    result = abc._date_is_available(date)

    assert result == expected
