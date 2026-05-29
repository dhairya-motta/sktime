
from sktime.utils.estimator_checks import check_estimator
from sktime.forecasting.dynamic_factor import DynamicFactor
try:
    check_estimator(DynamicFactor, raise_exceptions=True)
    print('[PASS] check_estimator for DynamicFactor')
except Exception as e:
    print(f'[FAIL] check_estimator for DynamicFactor: {e}')
