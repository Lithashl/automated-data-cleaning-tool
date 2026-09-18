import numpy as np
import pandas as pd

from cleaner.base import BaseCleaner
from report import CleaningReport
from strategy import OutlierStrategy

"""
Fill outlier with median data
"""
class OutlierHandler(BaseCleaner):
    def implement(self, df: pd.DataFrame, report: CleaningReport) -> pd.DataFrame:
        # looping setiap konfigurasi kolom
        for config in self.config.column_configs:
            # memastikan bahwa kolom yang diproses ada di dataframe dan
            # memastikan penanganan outlier tidak berjenis NONE
            if (
                config.col_name not in df.columns
                or config.outlier_strategy == OutlierStrategy.NONE
            ):
                continue
            # memastikan bahwa tipe data adalah numeric (int, float)
            series = df[config.col_name]
            if not pd.api.types.is_numeric_dtype(series):
                continue

            # membuat implementasi logika untuk IQR dan zscore
            # dengan menghitung batas bawah (lower bound)
            # dan batas atas (upper bound) setiap data
            if config.outlier_strategy == OutlierStrategy.IQR:
                q1, q3 = series.quantile(0.25), series.quantile(0.75)
                iqr = q3 - q1
                lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            else:
                mean, std = series.mean(), series.std()
                if std == 0 or pd.isna(std):
                    continue
                lower, upper = mean - 3 * std, mean + 3 * std

            # mengambil outlier (diatas upperbound dan dibawah lower bound)
            # lalu mengisinya dengen median data
            mask = (series < lower) | (series > upper)
            n = int(mask.sum())
            if n:
                df.loc[mask, config.col_name] = np.nan
                df[config.col_name] = df[config.col_name].fillna(series.median())
                report.outliers_handled[config.col_name] = n

        return df
