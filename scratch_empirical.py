import pandas as pd
from skpro.distributions.empirical import Empirical

spl_idx = pd.MultiIndex.from_tuples(
    [(0, "t1"), (1, "t1"), (2, "t1"), (0, "t2"), (1, "t2")], names=["sample", "time"]
)

spl = pd.DataFrame({"y": [1.0, 2.0, 3.0, 4.0, 5.0]}, index=spl_idx)
dist = Empirical(spl)
print("Mean:\n", dist.mean())
print("Var:\n", dist.var())
print("Quantiles:\n", dist.quantile([0.1, 0.9]))
