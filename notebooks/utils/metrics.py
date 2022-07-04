import functools
import numbers

import numpy as np
import sklearn.metrics


def normalized_mean_absolute_error(
    y_true,
    y_pred,
    sample_weight=None,
    multioutput="uniform_average",
    normalization=1.0,
    assym=0,
):
    r"""
    Normalized mean absolute error.

    Parameters
    ----------
    normalization : number or str
        If number, divide mae by this number
        Can be one of the strings ``spread``, ``mean``, ``std``, or ``var``,
        resulting  in normalization with the respective quantity calculated from `y_true`.
    assym : int
        If positive, only take those datapoints into account where y_pred >= y_true.
        If negative, only take those datapoints into account where y_pred <= y_true.
        If zero, take all datapoints into account.
        assym does NOT influence the calculation of the normalization when ``normalization`` is a string.
    Other parameters
        are forwarded to `sklearn.metrics.mean_absolute_error`.

    """
    normalization = _get_normalization(y_true, normalization)
    y_true, y_pred = _restrict_datapoints(y_true, y_pred, assym)
    mae = sklearn.metrics.mean_absolute_error(
        y_true, y_pred, sample_weight=sample_weight, multioutput=multioutput
    )
    return mae / normalization


def normalized_root_mean_squared_error(
    y_true,
    y_pred,
    sample_weight=None,
    multioutput="uniform_average",
    normalization=1.0,
    assym=0,
):
    r"""
    Normalized root mean squared error.

    Parameters
    ----------
    normalization : number or str
        If number, divide mae by this number
        Can be one of the strings ``spread``, ``mean``, ``std``, or ``var``,
        resulting  in normalization with the respective quantity calculated from `y_true`.
    assym : int
        If positive, only take those datapoints into account where y_pred >= y_true.
        If negative, only take those datapoints into account where y_pred <= y_true.
        If zero, take all datapoints into account.
        assym does NOT influence the calculation of the normalization when ``normalization`` is a string.
    Other parameters
        are forwarded to `sklearn.metrics.mean_absolute_error`.

    """
    normalization = _get_normalization(y_true, normalization)
    y_true, y_pred = _restrict_datapoints(y_true, y_pred, assym)
    rmse = root_mean_squared_error(
        y_true, y_pred, sample_weight=sample_weight, multioutput=multioutput
    )
    return rmse / normalization


def root_mean_squared_error(
    y_true, y_pred, sample_weight=None, multioutput="uniform_average"
):
    """Root of the mean squared error.

    Parameters are forwarded to `sklearn.metrics.mean_squared_error`.
    """
    mse = sklearn.metrics.mean_squared_error(
        y_true, y_pred, sample_weight=sample_weight, multioutput=multioutput
    )
    return np.sqrt(mse)


def _get_normalization(y_true, normalization):
    if isinstance(normalization, numbers.Number):
        return normalization
    if isinstance(normalization, str):
        if normalization.lower() == "spread":
            return np.max(y_true) - np.min(y_true)
        if normalization.lower() == "mean":
            return np.mean(y_true)
        if normalization.lower() == "std":
            return np.std(y_true)
        if normalization.lower() == "var":
            return np.var(y_true)
        else:
            raise ValueError(
                "Normalization must either be a number or one of 'spread', 'mean', 'std', 'var'. "
                f"Found {normalization} which is neither."
            )


def _restrict_datapoints(y_true, y_pred, assym):
    if assym == 0:
        return y_true, y_pred
    elif assym > 0:
        mask = y_pred < y_true  # Values will be masked where mask is true
    else:
        mask = y_pred > y_true  # So we have to take the logical opposite.
    mask = functools.partial(np.ma.masked_array, mask=mask)
    return map(np.ma.compressed, map(mask, [y_true, y_pred]))
