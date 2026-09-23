import numpy as np
import pandas as pd

from cleaner.base import BaseCleaner
from report import CleaningReport


class AllowedValuesFilter(BaseCleaner):
    def implement(self, df: pd.DataFrame, report: CleaningReport):
        for config in self.config.column_configs:
            if config.col_name not in df.columns:
                continue
            if config.allowed_values is None:
                continue

            mask = df[config.col_name].isin(config.allowed_values)
            was_not_na = df[config.col_name].notna()
            n_invalid = int((was_not_na & ~mask).sum())

            df[config.col_name] = df[config.col_name].where(mask, np.nan)

            if n_invalid > 0:
                report.invalid_values_deleted[config.col_name] = n_invalid

        return df