import numpy as np
import xarray as xr

from . import density


def test_calculate_density():
    temperature = xr.DataArray([1.0, 2.0, 3.0])
    pressure = xr.DataArray([1.0, 2.0, 3.0])
    relative_humidity = xr.DataArray([1.0, 2.0, 3.0])
    specific_humidity = xr.DataArray([1.0, 2.0, 3.0])

    result = density._calculate_density(
        temperature=temperature,
        pressure=pressure,
        relative_humidity=relative_humidity,
        specific_humidity=specific_humidity,
    )

    assert isinstance(result, xr.DataArray)


def test_rh():
    theta = xr.DataArray(
        data=np.array([280.30704, 280.34143, 280.06357, 279.99207, 280.0512 , 279.76233,
       279.57184, 279.164  , 279.09384, 279.43497, 279.68738, 279.74927,
       280.27695, 280.0551 , 279.27905, 278.77222, 278.26398, 277.60123,
       277.40894, 276.96182, 276.69672, 276.615  , 276.47763, 276.4316 ],
      dtype=np.float32)
    )
    p = xr.DataArray(np.array([100780.89320684, 100691.25938343, 100629.40833884, 100518.27722353,
       100378.32089605, 100244.12497797, 100189.60957538, 100064.85733115,
        99980.4588396 ,  99901.31112338,  99835.25945854,  99718.36793383,
        99688.75510537,  99640.10049464,  99625.96973165,  99593.53847231,
        99564.75959052,  99556.91431445,  99510.86964793,  99523.42517833,
        99505.11696026,  99485.75858713,  99481.0483328 ,  99492.55370814], dtype=np.float32))
    q = xr.DataArray(np.array([0.00607639, 0.0059933 , 0.0058618 , 0.00571206, 0.00535586,
       0.005237  , 0.00522418, 0.0050291 , 0.00480295, 0.00485605,
       0.00510731, 0.0053676 , 0.00553335, 0.0051581 , 0.00483336,
       0.00440401, 0.00427565, 0.00428529, 0.00396877, 0.00356923,
       0.00327716, 0.00306543, 0.00286495, 0.00275516], dtype=np.float32))

    result = density._rh(theta=theta, p=p, q=q)

    # In a Google colab environment, this function raised a
    # TypeError (see
    # https://github.com/4castRenewables/climetlab-plugin-a6/issues/19)
    # due to the result of `density._p_d` (and, as a consequence also
    # the result of `density._rh`) having the dtype object.
    # It requires to be of numpy.dtype float.
    # This could not be reproduced and hence is checked here.
    assert result.dtype is not np.dtype("O")
    assert result.dtype == np.float64 or result.dtype == np.float32
