import matplotlib.pyplot as plt
import numpy as np


def plot_forecast_and_real_production_data(
    indexes: np.ndarray,
    forecast: np.ndarray,
    real: np.ndarray,
) -> None:
    """Plot the forecast and real production data with residuals.

    Parameters
    ----------
    indexes : np.ndarray
        Indexes of the timeseries.
    forecast : np.ndarray
        Forecasted production.
    real : np.ndarray
        Real production.

    """

    fig, axs = plt.subplots(
        nrows=2,
        ncols=1,
        figsize=(12, 8),
        sharex=True,
        gridspec_kw={"height_ratios": [0.8, 0.2]},
    )
    fig.subplots_adjust(hspace=0)

    axs[0].set_title(f"Power production forecast")

    axs[0].plot(indexes, forecast, label="forecast")
    axs[0].plot(indexes, real, label="real")

    residuals = (forecast - real) / real
    axs[1].scatter(indexes, residuals, color="black")

    for ax in axs:
        ax.grid(True)

    axs[1].set_xlabel("Time")
    axs[0].set_ylabel("Power production [kW]")
    axs[1].set_ylabel("Residuals")

    axs[0].set_xlim(min(indexes), max(indexes))
    axs[0].set_ylim(0, 1.1 * max(max(forecast), max(real)))
    axs[1].set_ylim(1.5 * min(residuals), 1.2 * max(residuals))

    axs[0].legend()
    plt.show()
