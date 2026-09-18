from enum import Enum

# class ini berisi berbagai strategi yang kita sediakan
# untuk menghandle missing values
class MissingStrategy(str, Enum):
    DROP = "drop"
    MEAN = "mean"
    MEDIAN = "median"
    MODE = "mode"
    FFILL = "ffill"
    BFILL = "bfill"
    FFILL_TO_BFILL = "ffill_to_bfill"
    BFILL_TO_FFILL = "bfill_to_ffill"
    NONE = "none"
    CONSTANT = "constant"

# class ini berisi berbagai strategi yang kita sediakan
# untuk menghandle outlier
class OutlierStrategy(str, Enum):
    IQR = "iqr"
    ZSCORE = "zscore"
    NONE = "none"
