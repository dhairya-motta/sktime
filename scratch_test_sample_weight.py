import numpy as np
import pandas as pd

from sktime.performance_metrics.forecasting.probabilistic import PinballLoss

# Create dummy data
y_true = pd.Series([3, -0.5, 2, 7, 2])
y_pred = pd.DataFrame(
    {
        ("Quantiles", 0.05): [1.25, 0, 1, 4, 0.625],
        ("Quantiles", 0.5): [2.5, 0, 2, 8, 1.25],
        ("Quantiles", 0.95): [3.75, 0, 3, 12, 1.875],
    }
)

# Instantiate the metric
pl = PinballLoss()

# 1. Unweighted evaluation
loss_unweighted = pl(y_true, y_pred)
print(f"Unweighted Pinball Loss: {loss_unweighted}")

# 2. Weighted evaluation (higher weight on the first observation where error is small)
# Pinball loss per index for score_average=True (average over alpha=0.05, 0.5, 0.95)
# If we weight the first index heavier, the overall loss should change
weights = np.array([5.0, 1.0, 1.0, 1.0, 1.0])
loss_weighted = pl(y_true, y_pred, sample_weight=weights)
print(f"Weighted Pinball Loss (heavy on first): {loss_weighted}")

# 3. Weighted evaluation (higher weight on the fourth observation where error is high)
weights2 = np.array([1.0, 1.0, 1.0, 5.0, 1.0])
loss_weighted2 = pl(y_true, y_pred, sample_weight=weights2)
print(f"Weighted Pinball Loss (heavy on fourth): {loss_weighted2}")

if loss_unweighted != loss_weighted and loss_weighted != loss_weighted2:
    print("SUCCESS: sample_weight correctly impacts the evaluation output!")
else:
    print("FAILURE: sample_weight had no effect.")
