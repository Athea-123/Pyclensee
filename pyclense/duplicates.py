import pandas as pd
from typing import Literal
from .base import BaseCleaner


class DuplicateCleaner(BaseCleaner):

    def get_dupes(self):
        """
        Identify all duplicate rows in the dataset.
        Returns a DataFrame of all duplicates (including the first occurrence).
        """
        return self._df[self._df.duplicated(keep=False)]

    def tag_dupes(self, tag_column: str = "is_duplicate"):
        """
        Add a boolean column that marks duplicate rows.
        """
        # mark all duplicate rows (including first occurrences)
        self._df[tag_column] = self._df.duplicated(keep=False)

        self.record_change(f"Tagged duplicates in column '{tag_column}'")

    def cull_dupes(self, keep: Literal["first", "last", False] = "first"):
        """
        Remove duplicate rows.
        """
        before = len(self._df)

        self._df = self._df.drop_duplicates(keep=keep)

        after = len(self._df)
        removed = before - after

        self.record_change(f"Removed {removed} duplicate rows")
        # record a simple summary of the removal
        self.record_change(f"remove_duplicates: before={before}, after={after}, keep={keep}")

        return self._df

    def clean(self):
        """Run the duplicate removal clean step and return the cleaned DataFrame."""
        return self.cull_dupes()