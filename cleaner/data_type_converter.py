import pandas as pd

from cleaner.base import BaseCleaner


class DataTypeConverter(BaseCleaner):
    # ini adalah translasi 1 banding 1 dengan dtype yang kita
    # tentukan di konfigurasi kolom (ColumnConfig)
    _DTYPE_MAP = {
        "int": "int64",
        "float": "float64",
        "str": "string",
        "bool": "boolean",
        "datetime": "datetime64[ns]",
    }

    # implementasi dari abstact method [WAJIB]
    def implement(self, df, report):
        # looping setiap configurasi = looping setiap aturan pembersihan kolom
        for config in self.config.column_configs:
            # meastikan user input dtype di konfigurasi dan kolom yang saat ini dicek
            # terdaftar di data raw
            if not config.dtype or config.col_name not in df.columns:
                continue

            # menghitung jumlah missing sebelum konverter dijalankan
            na_before = df[config.col_name].isna().sum()

            # melakukan eksekusi kode yang jika gagal akan trigger except blok
            # except blok digunakan untuk menampung kolom yang gagal di proses dan alasan
            # kenapa gagal di proses.
            try:
                # memproses dtype berbentuk datetime
                if config.dtype == "datetime":
                    df[config.col_name] = pd.to_datetime(
                        df[config.col_name], errors="coerce"
                    )
                # memproses dtype berbentuk selain datetime
                else:
                    df[config.col_name] = (
                        pd.to_numeric(df[config.col_name], errors="coerce")
                        if config.dtype in ("int", "float")
                        else df[config.col_name]
                    )
                    df[config.col_name] = df[config.col_name].astype(
                        self._DTYPE_MAP[config.dtype]
                    )
            # mengeksekusi blok ini ketika kode gagal dijalankan.
            except Exception as e:
                report.type_conversion_failed[config.col_name] = -1
                report.type_conversion_failed_reason[config.col_name] = e

        return df
