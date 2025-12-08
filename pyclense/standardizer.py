import pandas as pd
import re

class Standardizer:
    def __init__(self, df):
        self.df = df

    def clean_column_names(self):
        """Standardizes column names to Title Case and strips spaces."""
        if self.df is not None:
            # Convert headers to string, strip whitespace, and Title Case
            self.df.columns = [str(c).strip().title() for c in self.df.columns]
            print(f"Cleaned column names: {list(self.df.columns)}")

    def standardize_dates(self, subset=None):
        """Converts specific columns to datetime objects."""
        if self.df is not None and subset:
            for col in subset:
                if col in self.df.columns:
                    self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
            print(f"Standardized Dates in: {subset}")

    # Legacy method from your previous scripts (Currency Cleaning)
    def clean_currency_column(self, col):
        """Removes symbols like '$' from currency columns and converts to numeric."""
        if self.df is not None and col in self.df.columns:
            self.df[col] = pd.to_numeric(
                self.df[col].astype(str).str.replace(r'[^\d.]', '', regex=True),
                errors='coerce'
            )
            print(f"Cleaned currency column: '{col}'")
    
    # Legacy method from your previous scripts (Guest Cleaning)
    def clean_guests_column(self, col):
        """Extracts numbers from strings like '6+' -> 6."""
        if self.df is not None and col in self.df.columns:
             self.df[col] = pd.to_numeric(
                 self.df[col].astype(str).str.extract(r'(\d+)')[0], 
                 errors='coerce'
             )
             print(f"Cleaned guests column: '{col}'")