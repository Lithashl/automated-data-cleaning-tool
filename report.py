from pydantic import BaseModel, Field


class CleaningReport(BaseModel):
    initial_rows: int
    initial_cols: int
    final_rows: int = 0
    final_cols: int = 0

    duplicated_removed: int = 0
    columns_dropped: list[str] = Field(default_factory=list)
    missing_handled: dict[str, int] = Field(default_factory=dict)
    outliers_handled: dict[str, int] = Field(default_factory=dict)
    type_conversion_failed: dict[str, int] = Field(default_factory=dict)
    type_conversion_failed_reason: dict[str, int] = Field(default_factory=dict)
    invalid_values_deleted: dict[str, int] = Field(default_factory=dict)

    def generate(self) -> str:
        result = [
            "Cleaning Result",
            f"Rows: {self.initial_rows} -> {self.final_rows}",
            f"Cols: {self.initial_cols} -> {self.final_cols}",
            f"Duplicates removed: {self.duplicated_removed}",
        ]
        if self.columns_dropped:
            result.append(
                f"Columns dropped (missing > threshold): {self.columns_dropped}"
            )
        if self.missing_handled:
            result.append(f"Missing values handled per column: {self.missing_handled}")
        if self.outliers_handled:
            result.append(f"Outliers handled per column: {self.outliers_handled}")
        if self.type_conversion_failed:
            result.append(f"Type conversion failed: {self.type_conversion_failed}")
        if self.type_conversion_failed_reason:
            result.append(
                f"Failed convertion reason: {self.type_conversion_failed_reason}"
            )
        if self.invalid_values_deleted:
            result.append(f"Invalid values deleted: {self.invalid_values_deleted}")

        return "\n".join(result)
