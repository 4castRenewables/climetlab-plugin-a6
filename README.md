## climetlab-power-production
[![PyPI version](https://badge.fury.io/py/climetlab-maelstrom-power-production.svg)](https://badge.fury.io/py/climetlab-maelstrom-power-production)
![workflow](https://github.com/faemmi/climetlab-plugin-a6/actions/workflows/check-and-publish.yml/badge.svg)
[![](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A dataset plugin for climetlab for the dataset climetlab-plugin-a6/maelstrom-production-forecasts.


Features
--------

In this README is a description of how to get the CliMetLab Plugin for A6.

## Installation

Via `pip`

```commandline
pip install climetlab-maelstrom-power-production
```

or via [`poetry`](https://python-poetry.org/)

```bash
git clone git@github.com:4castRenewables/climetlab-plugin-a6.git
cd climetlab-plugin-a6
poetry install --no-dev
```

## Datasets description

There are five datasets:

- `maelstrom-constants-a-b`
- `maelstrom-power-production`
- `maelstrom-weather-model-level`
- `maelstrom-weather-pressure-level`
- `maelstrom-weather-surface-level`

A detailed description of each dataset (variables, meta data etc.) is available [here](https://www.maelstrom-eurohpc.eu/content/docs/uploads/doc6.pdf) (see Section 3.6).

### `maelstrom-constants-a-b`
Constants used for calculation of pressure at intermediate model levels.

#### Usage

```Python
import climetlab as cml

production_data = cml.load_dataset("maelstrom-constants-a-b")
```

#### References
IFS Documentation – Cy47r1, Operational implementation 30 June 2020, Part III: Dynamics and Numerical Procedures, ECMWF, 2020, p. 6, Eq. 2.11

### `maelstrom-power-production`
Power production data of wind turbines located in various regions of Germany.

The data were provided by [NOTUS energy GmbH & Co. KG](https://www.notus.de).
For a detailed description see the link above.

#### Usage

```Python
import climetlab as cml

production_data = cml.load_dataset("maelstrom-power-production", wind_turbine_id=1)
```

The `wind_turbine_id` is a number `1` to `N`, where `N` is the maximum number of currently available wind turbines.

Currently available: 4 wind turbines.

### `maelstrom-weather-model-level`
[ECMWF](https://www.ecmwf.int) IFS HRES model level data for whole Europe.

For a detailed description see the link above.

#### Usage

```Python
import climetlab as cml

weather_ml = cml.load_dataset("maelstrom-weather-model-level", date="2019-01-01")
```

Currently available dates:
- `2017-01-01` until `2020-12-31`

### `maelstrom-weather-pressure-level`
[ECMWF](https://www.ecmwf.int) IF HRES pressure level data for whole Europe.

For a detailed description see the link above.

#### Usage

```Python
import climetlab as cml

weather_pl = cml.load_dataset("maelstrom-weather-pressure-level", date="2019-01-01")
```

Currently available dates:
- `2017-01-01` until `2020-12-31`

### `maelstrom-weather-surface-level`
[ECMWF](https://www.ecmwf.int) IFS HRES surface level data for whole Europe.

For a detailed description see the link above.

#### Usage

```Python
import climetlab as cml

weather_pl = cml.load_dataset("maelstrom-weather-surface-level", date="2019-01-01")
```

Currently available dates:
- `2017-01-01` until `2020-12-31`

## Using climetlab to access the data (supports grib, netcdf and zarr)

See the demo notebooks [here](https://github.com/faemmi/climetlab-plugin-a6/tree/main/notebooks).

The climetlab python package allows easy access to the data with a few lines of code such as:
```Python
!pip install climetlab climetlab-maelstrom-power-production
import climetlab as cml

data = cml.load_dataset("maelstrom-weather-surface-level", date="2019-01-01")
data.to_xarray()
```


### Executing the notebooks

Before executing the notebooks, make sure to install the project and the
notebook dependencies correctly
```commandline
poetry install --extras notebooks
```
