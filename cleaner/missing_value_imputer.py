import pandas as pd

from cleaner.base import BaseCleaner
from report import CleaningReport
from strategy import MissingStrategy


class MissingValueImputer(BaseCleaner):
    def implement(self, df: pd.DataFrame, report: CleaningReport):
        for config in self.config.column_configs:
            if config.col_name not in df.columns:
                continue
            if config.missing_strategy == MissingStrategy.NONE:
                continue

            n_missing = int(df[config.col_name].isna().sum())

            if n_missing == 0:
                continue

            col = config.col_name
            strategy = config.missing_strategy

            # MEAN dan MEDIAN hanya masuk akal untuk kolom numerik. MEAN adalah
            # default ColumnConfig, jadi kolom teks yang lupa diatur strateginya
            # akan melempar TypeError tanpa penjagaan ini.
            if strategy in (
                MissingStrategy.MEAN,
                MissingStrategy.MEDIAN,
            ) and not pd.api.types.is_numeric_dtype(df[col]):
                continue

            if strategy == MissingStrategy.DROP:
                df = df.dropna(subset=[col])
            elif strategy == MissingStrategy.MEAN:
                df[col] = df[col].fillna(df[col].mean())
            elif strategy == MissingStrategy.MEDIAN:
                df[col] = df[col].fillna(df[col].median())
            elif strategy == MissingStrategy.MODE:
                mode_val = df[col].mode()
                if not mode_val.empty:
                    df[col] = df[col].fillna(mode_val[0])
            elif strategy == MissingStrategy.FFILL:
                df[col] = df[col].ffill()
            elif strategy == MissingStrategy.BFILL:
                df[col] = df[col].bfill()
            elif strategy == MissingStrategy.FFILL_TO_BFILL:
                df[col] = df[col].ffill().bfill()
            elif strategy == MissingStrategy.BFILL_TO_FFILL:
                df[col] = df[col].bfill().ffill()
            elif strategy == MissingStrategy.CONSTANT:
                df[col] = df[col].fillna(config.fill_value)
                
            report.missing_handled[col] = n_missing

        return df