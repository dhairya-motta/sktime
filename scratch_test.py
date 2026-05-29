import warnings

warnings.filterwarnings("ignore")
import sys

sys.path.append(r"c:\Users\kingcuber\Desktop\skpro")

from sktime.datasets import load_airline
from sktime.forecasting.conformal import ConformalIntervals
from sktime.forecasting.naive import NaiveForecaster


def test_proba():
    print("Testing ConformalIntervals _predict_proba on Series")
    y = load_airline()
    forecaster = NaiveForecaster(strategy="drift")
    conformal_forecaster = ConformalIntervals(forecaster)
    conformal_forecaster.fit(y, fh=[1, 2, 3])

    # This will call _predict_proba internally if skpro is available
    dist = conformal_forecaster.predict_proba()
    print("Distribution:", type(dist))

    if dist is not None:
        mean = dist.mean()
        print("Mean shape:", mean.shape)
        quantiles = dist.quantile([0.1, 0.9])
        print("Quantiles shape:", quantiles.shape)
        print("Quantiles head:\n", quantiles.head())


def test_proba_hierarchical():
    print("\nTesting ConformalIntervals _predict_proba on Hierarchical")
    from sktime.utils._testing.hierarchical import _make_hierarchical

    y = _make_hierarchical(
        hierarchy_levels=(2, 3),
        max_timepoints=15,
        min_timepoints=15,
        n_columns=1,
    )

    forecaster = ConformalIntervals(NaiveForecaster())
    forecaster.fit(y, fh=[1, 2])
    dist = forecaster.predict_proba()
    print("Distribution:", type(dist))

    if dist is not None:
        mean = dist.mean()
        print("Mean shape:", mean.shape)
        quantiles = dist.quantile([0.1, 0.9])
        print("Quantiles shape:", quantiles.shape)


if __name__ == "__main__":
    test_proba()
    test_proba_hierarchical()
