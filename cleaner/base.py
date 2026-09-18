from abc import ABC, abstractmethod

import pandas as pd

from config import CleaningConfig
from report import CleaningReport

# class abstract yang menyediakan metode `implement` untuk mengimplementasi
# proses pembersihan.
class BaseCleaner(ABC):
    def __init__(self, config: CleaningConfig) -> None:
        self.config: CleaningConfig = config

    @abstractmethod
    def implement(self, df: pd.DataFrame, report: CleaningReport):
        pass
