import pandas as pd

from cleaner.base import BaseCleaner
from report import CleaningReport


class Deduplicator(BaseCleaner):
    def implement(self, df: pd.DataFrame, report: CleaningReport):
        # Cek dulu apakah user mau hapus duplikat atau tidak
        if not self.config.drop_duplicated:
            return df

        # Simpan jumlah baris sebelum dedup
        n_before = len(df)

        # Hapus duplikat — pakai subset kalau user tentukan, kalau tidak cek semua kolom
        df = df.drop_duplicates(subset=self.config.duplicate_subset)

        # Catat berapa baris yang terhapus ke report
        report.duplicated_removed = n_before - len(df)

        return df