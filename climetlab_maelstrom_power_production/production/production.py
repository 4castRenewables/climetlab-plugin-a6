#!/usr/bin/env python3# (C) Copyright 2021 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#
"""Load wind turbine production data."""
import climetlab as cml  # type: ignore

from climetlab_maelstrom_power_production import dataset

PATTERN = "production_data/wind_turbine_{wind_turbine_id}.nc"

NUMBER_OF_AVAILABLE_WIND_TURBINES = 45


class Production(dataset.AbstractDataset):
    """Access the power production data of a wind turbine.

    Parameters
    ----------
    wind_turbine_id : int
        Unique ID of the wind turbine.

    """

    name = "Wind turbine power production dataset"
    documentation = (
        "Contains the power production of wind turbines and other measured/reported quantities from each site"
        "(wind speed, rotor speed, regulation by the network operator, and status). "
        "The data is grouped by wind turbine. For detailed information see "
        "https://www.maelstrom-eurohpc.eu/content/docs/uploads/doc6.pdf in Section 3.6."
    )
    url_pattern = PATTERN

    def __init__(self, wind_turbine_id: int):
        """Initialize and load the dataset."""
        wind_turbine_id = int(wind_turbine_id)
        if wind_turbine_id > NUMBER_OF_AVAILABLE_WIND_TURBINES:
            raise ValueError(
                f"No data available for wind turbine with ID {wind_turbine_id}. "
                f"Available are ID 1 to {NUMBER_OF_AVAILABLE_WIND_TURBINES}."
            )
        self.wind_turbine_id = wind_turbine_id
        self.source = self._get_data()

    def _get_data(self) -> cml.Source:
        return self._load_source(wind_turbine_id=self.wind_turbine_id)
