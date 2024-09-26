#!/usr/bin/env python3# (C) Copyright 2021 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#
import abc
import datetime
import itertools
from typing import Optional, Union

import climetlab as cml  # type: ignore
import pandas as pd  # type: ignore

import climetlab_maelstrom_power_production.merger
from climetlab_maelstrom_power_production import dataset

from . import merger

# TODO: Implement merging of the two datasets (currently only `PATTERN_1` is loaded).
#  Make sure to always take the more recent data if there are duplicates.

PATTERN = "{type}_{date_with_model_timestamp}.nc"
MODEL_TIMESTAMP_1 = "00"
MODEL_TIMESTAMP_2 = "12"

DATE_FORMAT = "%Y-%m-%d"
DATE_FORMAT_REMOTE = "%Y%m%d"

AVAILABLE_DATA_DATES = pd.date_range(
    start=datetime.datetime(2017, 1, 1), end=datetime.datetime(2020, 12, 31)
)


class IncorrectDateFormatException(Exception):
    """Given date has an invalid format."""


class DateUnavailableException(Exception):
    """No data available for given date."""


class Weather(dataset.AbstractDataset):
    """Access the weather data.

    Parameters
    ----------
    date : str or t.List[str], default None
        Date(s) for which to get the weather data.
        If `None`, all available dates will be fetched.

    """

    url_pattern = PATTERN
    model_timestamp_1 = MODEL_TIMESTAMP_1
    model_timestamp_2 = MODEL_TIMESTAMP_2
    dates = AVAILABLE_DATA_DATES

    def __init__(self, date: Optional[Union[str, list[str]]] = None):
        """Initialize and load the dataset."""
        self.date = _convert_dates(date) if date is not None else self.dates
        self._merger = merger.WeatherMerger()

        self.source = self._get_data()

    @property
    @abc.abstractmethod
    def type(self) -> str:  # noqa: A003
        """Return the type of the weather data.

        Either ml (model level) or pl (pressure level).

        """

    @property
    def merger(
        self,
    ) -> Optional[climetlab_maelstrom_power_production.merger.AbstractMerger]:
        """Get the merger for the weather data."""
        return self._merger

    def _get_data(self) -> cml.Source:
        dates_with_model_timestamps = self._add_timestamps_to_each_date()
        return self._load_source(
            type=self.type,
            date_with_model_timestamp=dates_with_model_timestamps,
        )

    def _add_timestamps_to_each_date(self) -> list[str]:
        dates = (date.strftime(DATE_FORMAT_REMOTE) for date in self.date)
        timestamps = (self.model_timestamp_1, self.model_timestamp_2)
        dates_with_model_timestamps = (
            f"{date}_{timestamp}"
            for date, timestamp in itertools.product(dates, timestamps)
        )
        return list(dates_with_model_timestamps)


def _convert_dates(dates: Union[str, list[str]]) -> list[datetime.datetime]:
    if isinstance(dates, str):
        dates_as_datetime = [_convert_to_datetime(dates)]  # type: ignore
    else:
        dates_as_datetime = list(map(_convert_to_datetime, dates))
    _check_dates_availability(dates_as_datetime)
    return sorted(dates_as_datetime)


def _convert_to_datetime(date: str) -> datetime.datetime:
    try:
        return datetime.datetime.strptime(date, DATE_FORMAT)
    except ValueError:
        raise IncorrectDateFormatException(
            f"Date {date} has incorrect format ({DATE_FORMAT} required)"
        )


def _check_dates_availability(dates: list[datetime.datetime]) -> None:
    for date in dates:
        if not _date_is_available(date):
            start = AVAILABLE_DATA_DATES[0].strftime(DATE_FORMAT)
            end = AVAILABLE_DATA_DATES[-1].strftime(DATE_FORMAT)
            raise DateUnavailableException(
                f"Date {date} is not an available date. "
                f"Available dates: {start} until {end}."
            )


def _date_is_available(date: datetime.datetime) -> bool:
    return date in AVAILABLE_DATA_DATES
