import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LassoCV
from sklearn.feature_selection import mutual_info_regression
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt

class FeatureImportance:
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def random_forest_importance(self):
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(self.X, self.y)
        importances = rf.feature_importances_
        return pd.Series(importances, index=self.X.columns).sort_values(ascending=False)

    def lasso_importance(self):
        lasso = LassoCV(cv=5, random_state=42)
        lasso.fit(self.X, self.y)
        return pd.Series(np.abs(lasso.coef_), index=self.X.columns).sort_values(ascending=False)

    def mutual_info(self):
        mi = mutual_info_regression(self.X, self.y)
        return pd.Series(mi, index=self.X.columns).sort_values(ascending=False)

    def permutation_importance(self):
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(self.X, self.y)
        result = permutation_importance(rf, self.X, self.y, n_repeats=10, random_state=42)
        return pd.Series(result.importances_mean, index=self.X.columns).sort_values(ascending=False)
