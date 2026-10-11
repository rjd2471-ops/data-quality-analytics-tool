
import pandas as pd


class DataCleaner:
    def __init__(self, df):
        # Work on a copy so the original DataFrame is preserved.
        self.df = df.copy()

    def remove_duplicates(self):
        """Remove duplicate rows."""
        rows_before = len(self.df)
        self.df = self.df.drop_duplicates()
        return self.df

    def remove_missing_values(self):
        """Remove rows containing missing values."""
        self.df = self.df.dropna()
        return self.df

    def trim_whitespace(self):
        """Remove leading and trailing whitespace from text columns."""
        str_cols = self.df.select_dtypes(include=["object"]).columns
        self.df[str_cols] = self.df[str_cols].apply(
            lambda column: column.str.strip()
        )
        return self.df

    def standardize_categories(self):
        """Convert text values to lowercase."""
        cat_cols = self.df.select_dtypes(include=["object"]).columns
        self.df[cat_cols] = self.df[cat_cols].apply(
            lambda column: column.str.lower()
        )
        return self.df

    def convert_data_types(self, column_type_mapping):
        """Convert specified columns to requested data types."""
        for column, dtype in column_type_mapping.items():
            if column not in self.df.columns:
                raise ValueError(f"Column not found: {column}")

            self.df[column] = self.df[column].astype(dtype)

        return self.df

    def standardize_dates(self, date_columns, date_format):
        """Convert specified columns to a consistent date format."""
        for column in date_columns:
            if column not in self.df.columns:
                raise ValueError(f"Column not found: {column}")

            dates = pd.to_datetime(
                self.df[column], errors="coerce", format="mixed"
            )
            self.df[column] = dates.dt.strftime(date_format)

        return self.df

    def standardize_column_names(self):
        """Lowercase column names and replace spaces with underscores."""
        self.df.columns = (
            self.df.columns.str.strip()
            .str.lower()
            .str.replace(" ", "_", regex=False)
        )
        return self.df

    
    def cleaning_logic(self):
        """Optional automatic cleaning; not used by user-controlled cleaning."""
        self.remove_duplicates()
        self.trim_whitespace()
        self.standardize_categories()
        self.standardize_column_names()
        return self.df

    def user_control_actions(self, choices):
        """
        Apply only selected cleaning actions.

        Returns:
            cleaned_df: The cleaned DataFrame.
            cleaning_log: Details of the actions performed.
        """
        cleaning_log = []

        # Apply actions in a deliberate order.
        if choices.get("trim_whitespace", False):
            before = self.df.copy()
            self.trim_whitespace()

            changed = int(
                (before.fillna("").astype(str)
                 != self.df.fillna("").astype(str)).any(axis=1).sum()
            )
            cleaning_log.append({
                "action": "Trim whitespace",
                "rows_affected": changed,
                "details": "Trimmed leading/trailing whitespace in text columns"
            })

        if choices.get("standardize_categories", False):
            self.standardize_categories()
            cleaning_log.append({
                "action": "Standardize categories",
                "rows_affected": None,
                "details": "Converted text values to lowercase"
            })

        if choices.get("remove_duplicates", False):
            rows_before = len(self.df)
            self.remove_duplicates()
            rows_removed = rows_before - len(self.df)

            cleaning_log.append({
                "action": "Remove duplicates",
                "rows_affected": rows_removed,
                "details": f"Removed {rows_removed} duplicate rows"
            })

        if choices.get("remove_missing_values", False):
            rows_before = len(self.df)
            self.remove_missing_values()
            rows_removed = rows_before - len(self.df)

            cleaning_log.append({
                "action": "Remove missing values",
                "rows_affected": rows_removed,
                "details": f"Removed {rows_removed} rows containing missing values"
            })

        if choices.get("standardize_column_names", False):
            self.standardize_column_names()
            cleaning_log.append({
                "action": "Standardize column names",
                "rows_affected": None,
                "details": "Converted column names to lowercase_with_underscores"
            })

        return self.df, cleaning_log
