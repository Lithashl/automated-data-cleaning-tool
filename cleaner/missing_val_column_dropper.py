import pandas as pd

from cleaner.base import BaseCleaner

"""
Menghapus kolom dengan jumlah missing values lebih dari threshold
"""
class MissingValColumnDropper(BaseCleaner):
    # implementasi dari abstact method [WAJIB]
    def implement(self, df: pd.DataFrame, report):
        dropped: list[str] = [
            col
            for col in df.columns
            if df[col].isna().mean() > self.config.drop_col_threshold
        ]
        # memasukkan kolom yang harus didrop ke object CleaningReport
        report.columns_dropped = dropped

        return df.drop(columns=dropped)
