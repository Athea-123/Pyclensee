from base import BaseCleaner
import pandas as pd
from typing import Optional

class Standardizer(BaseCleaner):
    """
    A class used to standardize formats of data in a DataFrame.
    Inherits from BaseCleaner.
    """

    def standardize_dates(self, columns: list, format: str = '%m/%d/%Y') -> 'FormatStandardizer':
        """
        Converts specified columns to a standard date format.

        Parameters:
        -----------
        columns : list
            A list of column names containing date strings.
        format : str, optional
            The format to convert the dates into (default is '%m/%d/%Y', e.g., 12/31/2023).

        Returns:
        --------
        FormatStandardizer
            Returns self to allow method chaining.
        """
        for col in columns:
            if col in self._df.columns:
                # Convert to datetime objects first, then format them back to strings
                self._df[col] = pd.to_datetime(self._df[col], errors='coerce').dt.strftime(format)
                self._log_change('standardize_dates', {'column': col, 'format': format})
        return self

    def capitalize_names(self, columns: list) -> 'FormatStandardizer':
        """
        Converts text in specified columns to Title Case (e.g., 'john doe' -> 'John Doe').

        Parameters:
        -----------
        columns : list
            A list of column names to capitalize.

        Returns:
        --------
        FormatStandardizer
            Returns self to allow method chaining.
        """
        for col in columns:
            if col in self._df.columns:
                self._df[col] = self._df[col].astype(str).str.title()
                self._log_change('capitalize_names', {'column': col})
        return self

    def convert_to_lowercase(self, columns: list) -> 'FormatStandardizer':
        """
        Converts text in specified columns to lowercase (e.g., 'John Doe' -> 'john doe').

        Parameters:
        -----------
        columns : list
            A list of column names to convert.

        Returns:
        --------
        FormatStandardizer
            Returns self to allow method chaining.
        """
        for col in columns:
            if col in self._df.columns:
                self._df[col] = self._df[col].astype(str).str.lower()
                self._log_change('convert_to_lowercase', {'column': col})
        return self

    def fix_whitespace(self, columns: Optional[list] = None) -> 'FormatStandardizer':
        """
        Removes leading/trailing whitespace and replaces multiple spaces with a single space.
        Example: "  Hello    World  " -> "Hello World"

        Parameters:
        -----------
        columns : list, optional
            A list of specific columns to clean. If None, it automatically selects all text columns.

        Returns:
        --------
        FormatStandardizer
            Returns self to allow method chaining.
        """
        # If no columns are provided, find all text columns automatically
        if columns is None:
            columns = self._df.select_dtypes(include=['object']).columns.tolist()
            
        for col in columns:
            if col in self._df.columns:
                # Count how many rows have extra spaces before fixing them (for the log)
                before = (self._df[col].str.contains(r'\s{2,}', na=False)).sum()
                
                # .strip() removes side spaces, .replace(r'\s+', ' ') fixes middle spaces
                self._df[col] = self._df[col].astype(str).str.strip().str.replace(r'\s+', ' ', regex=True)
                
                self._log_change('fix_whitespace', {'columns': columns[:2], 'fixed_spaces': before})
        return self

    def remove_special_chars(self, columns: list) -> 'FormatStandardizer':
        """
        Removes special characters and emojis, keeping only letters, numbers, and spaces.
        
        Parameters:
        -----------
        columns : list
            A list of column names to clean.

        Returns:
        --------
        FormatStandardizer
            Returns self to allow method chaining.
        """
        for col in columns:
            if col in self._df.columns:
                # Regex Explanation: [^a-zA-Z0-9\s] means "Find anything that is NOT a letter, number, or space"
                # and replace it with empty string ''.
                self._df[col] = self._df[col].astype(str).str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
                self._log_change('remove_special_chars', {'column': col})
        return self

    def standardize_booleans(self, columns: list) -> 'FormatStandardizer':
        """
        Converts columns with various Yes/No formats into standard Python Booleans (True/False).
        Handles: 'yes', 'y', 'true', '1' -> True
        Handles: 'no', 'n', 'false', '0' -> False

        Parameters:
        -----------
        columns : list
            A list of column names to standardize.

        Returns:
        --------
        FormatStandardizer
            Returns self to allow method chaining.
        """
        # A map of all common ways people write "Yes" or "No"
        bool_map = {
            'yes': True, 'y': True, 'true': True, '1': True, 't': True,
            'no': False, 'n': False, 'false': False, '0': False, 'f': False
        }

        for col in columns:
            if col in self._df.columns:
                # Convert to string and lowercase so "Yes" and "yes" both match the map
                self._df[col] = self._df[col].astype(str).str.lower().map(bool_map)
                self._log_change('standardize_booleans', {'column': col})
        return self