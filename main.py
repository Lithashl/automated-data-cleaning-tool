import argparse # library untuk mengambil argumen dari terminal
import os # disini dipakai untuk mengecek apakah sebuah path itu ada atau tidak
from pathlib import Path # untuk membuat Path dari string

import pandas as pd # library untuk memanipulasi data

from config import CleaningConfig, ColumnConfig # custom kelas untuk membuat aturan pembersihan
from cleaner import DataCleaner # kelas untuk membungkus implementasi logika dan alur pembersihan
from strategy import MissingStrategy, OutlierStrategy

"""
    Kode ini akan dieksekusi ketika kita memanggil python main.py dari terminal.

    Contoh jika kode dipanggil dari dalam folder yang sama dengan main.py:

        python main.py --file_path data_loyalitas.csv --data_type data_loyalitas
"""
if __name__ == "__main__":
    # Pastikan user memasukkan argumen --file_path dan --data_type saat memanggil python main.py
    parser = argparse.ArgumentParser(description="Data Cleaner tool")
    parser.add_argument("--file_path", type=str, help="Path ke data yang akan diproses")
    parser.add_argument("--data_type", type=str, help="Tipe data yang akan diproses")
    args = parser.parse_args()

    # Jika --file_path dan --data_type tidak dimasukkan, berikan error yang representatif
    if not args.file_path:
        raise ValueError("Masukkan path file Anda sebagai argumen --file_path")
    if not args.data_type:
        raise ValueError(
            "Masukkan tipe data laporan yang akan diproses dengan argumen --data_type"
        )

    # Jika ketika memasukkan --file_path ternyata user typo atau salah, berikan error tidak ada file ditemukan
    if not os.path.exists(args.file_path):
        raise FileNotFoundError(f"Tidak ada file yang ditemukan di {args.file_path}")

    # selanjutnya, kita bisa mulai mengimport data ke workspace.
    # karena format data bisa berupa .csv dan atau .tsv, maka kita harus memastikan bahwa kita
    # memanggil fungsi import dengan parameter yang benar.
    file_path = Path(args.file_path)
    extension = file_path.suffix.lower()
    data = None
    if extension == ".csv":
        data = pd.read_csv(file_path)
    if extension == ".tsv":
        data = pd.read_csv(file_path, delimiter="\t")

    # Selanjutnya, kita membuat konfigurasi pembersihan berdasarkan jenis --data_type
    # yang diinput oleh user. Jika user memberikan input selain dari yang sudah
    # kita tentukan, berikan error sebagai petunjuk.
    config = None
    if args.data_type == "data_loyalitas":
        config = CleaningConfig(
            drop_duplicated=True,
            duplicate_subset=["ID_Pelanggan", "Nama_Pelanggan"],
            column_configs=[
                ColumnConfig(
                    col_name="Nama_Pelanggan",
                    dtype="str",
                    strip_string=True,
                    title_case=True,
                ),
                ColumnConfig(
                    col_name="Tanggal_Bergabung",
                    dtype="datetime",
                    missing_strategy=MissingStrategy.CONSTANT,
                    fill_value=pd.NaT,
                ),
                ColumnConfig(
                    col_name="Tingkat_Member",
                    dtype="str",
                    missing_strategy=MissingStrategy.MODE,
                    allowed_values=["Gold", "Silver", "Bronze"],
                ),
                ColumnConfig(
                    col_name="Poin_Loyalitas",
                    dtype="int",
                    missing_strategy=MissingStrategy.CONSTANT,
                    fill_value=0,
                ),
            ],
        )
    elif args.data_type == "data_penjualan":
        config = CleaningConfig(
            drop_duplicated=True,
            column_configs=[
                ColumnConfig(
                    col_name="ID_Transaksi",
                    dtype="str",
                    strip_string=True,
                ),
                ColumnConfig(
                    col_name="Tanggal_Transaksi",
                    dtype="datetime",
                    missing_strategy=MissingStrategy.CONSTANT,
                    fill_value=pd.NaT,
                ),
                ColumnConfig(
                    col_name="Kategori_Produk",
                    dtype="str",
                    missing_strategy=MissingStrategy.MODE,
                    strip_string=True,
                    title_case=True,
                ),
                ColumnConfig(
                    col_name="Total_Pendapatan",
                    dtype="int",
                    missing_strategy=MissingStrategy.MODE,
                    outlier_strategy=OutlierStrategy.IQR,
                    strip_string=True,
                    title_case=True,
                ),
                ColumnConfig(
                    col_name="Status_Transaksi",
                    dtype="str",
                    missing_strategy=MissingStrategy.CONSTANT,
                    fill_value="Batal",
                    strip_string=True,
                    title_case=True,
                ),
            ],
        )
    else:
        raise ValueError(f"Tidak dapat membuat config untuk --data_type: {args.data_type}.")

    # untuk robustness, kita check apakah config sudah benar2 terinisialisasi atau belum
    # Berikan error jika konfig tidak berhasil diinisialisasi
    if config is None:
        raise ValueError("Gagal membuat config.")

    # Buat object data cleaner, lalu panggil method clean
    cleaner = DataCleaner(config)
    df_result, report = cleaner.clean(data)

    print(df_result)
    print(report.generate())
