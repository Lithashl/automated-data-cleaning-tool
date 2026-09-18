from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator

from strategy import MissingStrategy, OutlierStrategy

DtypeLiteral = Literal["str", "float", "int", "bool", "datetime"]

# Class untuk menampung aturan pembersihan di level kolom (columnwise)
# Pengaturan ini mungkin unik setiap kolom,
# Satu kolom akan memiliki satu ColumnConfig.
class ColumnConfig(BaseModel):
    # memastikan setiap nilai string dari data seperti col_name tidak mengandung spasi berlebih.
    # meastikan penggunaan tipe enum dibandingkan value dari enum tersebut
    model_config = ConfigDict(str_strip_whitespace=True, use_enum_values=False)

    # nama kolom yang dikonfigurasi
    col_name: str
    # tipe kolom yang benar
    dtype: DtypeLiteral

    # jika ada missing value, bagaimana cara menghandle-nya?
    missing_strategy: MissingStrategy = MissingStrategy.MEAN
    # diisi hanya jika menggunakan CONSTAN pada missing strategy
    fill_value: Any = None

    # jika ada outlier di dalam data, apa yang harus dilakukan
    outlier_strategy: OutlierStrategy = OutlierStrategy.NONE

    # pengaturan untuk string normalizer
    strip_string: bool = True
    lower_case: bool = False
    title_case: bool = True

    # Masukkan nilai untuk memastikan kolom ini hanya akan berisi salah satu nilai di sini.
    allowed_values: list[Any] | None = None

    # memvalidasi kondisi dimana ketika memilih CONSTANT sebagai missing strategy, user
    # harus memasukkan nilai fill_value
    @model_validator(mode="after")
    def check_fill_value(self) -> "ColumnConfig":
        if (
            self.missing_strategy == MissingStrategy.CONSTANT
            and self.fill_value is None
        ):
            raise ValueError(
                f"Column {self.col_name}: needs fill_value for CONSTANT type MissingStrategy"
            )

        return self

# Class untuk menampung aturan pembersihan di level global (dataframe)
class CleaningConfig(BaseModel):
    # apakah ingin menghapus duplikasi data
    drop_duplicated: bool = True
    # berdasarkan kolom apa pengecekan duplikasi dilakukan
    duplicate_subset: list[str] | None = None
    # berapa besar threshold sebelum memutuskan untuk menghapus
    # satu kolom karena banyak nilai missing-nya
    drop_col_threshold: float = Field(default=0.5, ge=0.0, le=1.0)

    # tempat memasukkan konfigurasi setiap kolom
    column_configs: list[ColumnConfig] = Field(default_factory=list)

    # karena konfigurasi kolom langsung dimasukkan seluruhnya,
    # kita perlu memanggil setiap konfigurasi ketika akan melakukan pembersihan terhadap satu kolom.
    def get_column_config(self, column_name: str) -> ColumnConfig | None:
        return next((r for r in self.column_configs if r.col_name == column_name), None)
