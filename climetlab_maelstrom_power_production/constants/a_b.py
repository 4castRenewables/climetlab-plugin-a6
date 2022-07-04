#!/usr/bin/env python3# (C) Copyright 2021 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#
import climetlab as cml  # type: ignore

from climetlab_maelstrom_power_production import dataset

PATTERN = "ECMWF_AB137.nc"


class ABConstants(dataset.AbstractDataset):
    """Access the constants A and B for the model levels."""

    name = "Constants A and B for the model levels"
    documentation = "Contains the values for the constants A and B."
    citation = (
        "IFS Documentation – Cy47r1, "
        "Operational implementation 30 June 2020, "
        "Part III: Dynamics and Numerical Procedures, "
        "ECMWF, 2020, p. 6, Eq. 2.11"
    )
    url_pattern = PATTERN

    def __init__(self):
        """Initialize and load the dataset."""
        self.source = self._get_data()

    def _get_data(self) -> cml.Source:
        return self._load_source()
