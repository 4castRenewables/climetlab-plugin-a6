import climetlab as cml
import pytest


@pytest.mark.parametrize("wind_turbine_id", [1, 2, 3, 4])
def test_download_turbine_data(wind_turbine_id):
    response = cml.load_dataset(
        "maelstrom-power-production", wind_turbine_id=wind_turbine_id
    )
    result = response.to_dataframe()

    assert "production" in result.columns
    assert "wind_speed" in result.columns
