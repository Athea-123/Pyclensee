import pandas as pd
import numpy as np

class MissingValueHandler:
    def __init__(self, df):
        self.df = df.copy()

    def check_missing(self):
        """Checks for missing values and returns a summary."""
        missing_count = self.df.isnull().sum()
        missing_count = missing_count[missing_count > 0]
        
        if missing_count.empty:
            print("No missing values found.")
            return None
        
        print("Missing values per column:")
        print(missing_count)
        return missing_count

    def handle_missing(self, action='drop_rows', subset=None, fill_value=None, strategy=None):
        """
        Handles missing values in the dataframe.

        Args:
            action (str):
                - 'drop_rows': Drop rows containing NaNs (default).
                - 'drop_cols': Drop columns containing NaNs.
                - 'fill': Fill NaNs with a specified value (requires fill_value).
                - 'impute': Fill NaNs with a strategy ('mean', 'median', 'mode').
                - 'ffill': Forward fill (propagates last valid observation).
                - 'bfill': Backward fill (uses next valid observation).
            subset (list, optional): Columns to consider.
            fill_value (any): Value to use when action='fill'.
            strategy (str): 'mean', 'median', or 'mode' for action='impute'.
        """
        if self.df.isnull().sum().sum() == 0:
            print("No missing values to handle.")
            return self.df

        if action == 'drop_rows':
            before = len(self.df)
            self.df.dropna(subset=subset, inplace=True)
            print(f"Action 'drop_rows': Dropped {before - len(self.df)} rows.")

        elif action == 'drop_cols':
            before_cols = self.df.shape[1]
            if subset:
                # Drop only the specific columns if they have NaNs
                cols_to_drop = [col for col in subset if self.df[col].isnull().any()]
                self.df.drop(columns=cols_to_drop, inplace=True)
            else:
                self.df.dropna(axis=1, inplace=True)
            print(f"Action 'drop_cols': Dropped {before_cols - self.df.shape[1]} columns.")

        elif action == 'fill':
            if fill_value is None:
                print("Error: Action 'fill' requires a 'fill_value'.")
            else:
                if subset:
                    self.df[subset] = self.df[subset].fillna(fill_value)
                else:
                    self.df.fillna(fill_value, inplace=True)
                print(f"Action 'fill': Filled missing values with '{fill_value}'.")

        elif action == 'impute':
            if strategy not in ['mean', 'median', 'mode']:
                print("Error: Action 'impute' requires strategy 'mean', 'median', or 'mode'.")
            else:
                cols = subset if subset else self.df.columns
                for col in cols:
                    if self.df[col].isnull().any():
                        if strategy == 'mode':
                            if not self.df[col].mode().empty:
                                self.df[col].fillna(self.df[col].mode()[0], inplace=True)
                        # Mean/Median only work on numeric columns
                        elif pd.api.types.is_numeric_dtype(self.df[col]):
                            if strategy == 'mean':
                                self.df[col].fillna(self.df[col].mean(), inplace=True)
                            elif strategy == 'median':
                                self.df[col].fillna(self.df[col].median(), inplace=True)
                        else:
                            print(f"Skipping non-numeric column '{col}' for strategy '{strategy}'.")
                print(f"Action 'impute': Imputed missing values using '{strategy}'.")
        
        elif action == 'ffill':
            self.df.fillna(method='ffill', inplace=True)
            print("Action 'ffill': Forward filled values.")
            
        elif action == 'bfill':
            self.df.fillna(method='bfill', inplace=True)
            print("Action 'bfill': Backward filled values.")

        return self.df
