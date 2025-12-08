import pandas as pd
from base import BaseCleaner

class DuplicateCleaner(BaseCleaner):
    """
    A class for detecting, tagging, removing, and merging duplicate rows in a dataset.
    Attributes:
        _df (pd.DataFrame): The dataset to clean.
    """

    def get_dupes(self):
        """
        Identify all duplicate rows in the dataset.
        Parameters:
            None
        Returns:
            pd.DataFrame: All duplicate rows in the dataset, including the first occurrence.
        """
        return self._df[self._df.duplicated(keep=False)]

    def tag_dupes(self, tag_column='is_duplicate'):
        """
        Tag duplicate rows with a boolean flag in a new column.
        Parameters:
            tag_column (str): Name of the column to store duplicate status. Defaults to 'is_duplicate'.
        Returns:
            None: Modifies the dataset in-place.
        """
        self._df[tag_column] = self._df.duplicated(keep=False)
        self.record_change(f"Tagged duplicates in column '{tag_column}'")

    def cull_dupes(self, keep='first'):
        """
        Remove duplicate rows from the dataset.
        Parameters:
            keep (str): Determines which duplicate to keep. Options: 'first', 'last', False.
                        'first' keeps the first occurrence, 'last' keeps the last, False removes all duplicates.

        Returns:
            pd.DataFrame: Dataset with duplicates removed.
        """
        before = len(self._df)
        self._df = self._df.drop_duplicates(keep=keep)
        after = len(self._df)

        removed = before - after
        self.record_change(f"Removed {removed} duplicate rows")

        return self._df

    def duple_dupes(self, subset=None, method='first'):
        """
        Merge duplicate rows by filling missing values from duplicates into the first occurrence.

        Parameters:
            subset (list or None): Columns to consider when identifying duplicates. If None, all columns are used.
            method (str): Row selection method to keep as the base. Currently supports 'first' only.

        Returns:
            pd.DataFrame: Dataset with duplicates merged.
        """
        if method != 'first':
            raise ValueError("Currently, only 'first' method is supported for duple_dupes.")