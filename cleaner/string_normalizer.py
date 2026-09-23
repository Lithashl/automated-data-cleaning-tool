import pandas as pd

from cleaner.base import BaseCleaner
from report import CleaningReport


class StringNormalizer(BaseCleaner):
    def implement(self, df: pd.DataFrame, report: CleaningReport):
        for config in self.config.column_configs:
            if config.col_name not in df.columns:
                continue
            if not pd.api.types.is_string_dtype(df[config.col_name]):
                continue

            # konflik lower_case/title_case sudah divalidasi di ColumnConfig,
            # sehingga error muncul saat config dibuat, bukan saat kolom diproses.
            # Strip whitespace 
            if config.strip_string:
                df[config.col_name] = df[config.col_name].str.strip()
            # Ubah ke lowercase 
            if config.lower_case:
                df[config.col_name] = df[config.col_name].str.lower()
            # Ubah ke title case 
            if config.title_case:
                df[config.col_name] = df[config.col_name].str.title()

        return df