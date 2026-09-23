from pandas import DataFrame

from cleaner.base import BaseCleaner
from config import CleaningConfig
from cleaner.missing_val_column_dropper import MissingValColumnDropper
from cleaner.data_type_converter import DataTypeConverter
from cleaner.outlier_handler import OutlierHandler
from cleaner.deduplicator import Deduplicator
from cleaner.allowed_values_filter import AllowedValuesFilter
from cleaner.string_normalizer import StringNormalizer
from cleaner.missing_value_imputer import MissingValueImputer
from report import CleaningReport


class DataCleaner:
    def __init__(self, config: CleaningConfig):
        self.DEFAULT_FLOWS: list[type[BaseCleaner]] = [
            AllowedValuesFilter,
            StringNormalizer,
            MissingValColumnDropper,
            MissingValueImputer,
            OutlierHandler,
            DataTypeConverter,
            Deduplicator,
        ]
        self.config = config

    def clean(self, data_raw: DataFrame, flows: list[type[BaseCleaner]] | None = None):
        report = CleaningReport(
            initial_rows=len(data_raw), initial_cols=len(data_raw.columns)
        )

        flows = [flow(self.config) for flow in (flows or self.DEFAULT_FLOWS)]

        df_result = data_raw.copy()
        for flow in flows:
            df_result = flow.implement(df_result, report)

        report.final_rows = len(df_result)
        report.final_cols = len(df_result.columns)
        return df_result.reset_index(drop=True), report