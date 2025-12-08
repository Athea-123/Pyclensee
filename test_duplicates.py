import pandas as pd
from typing import Literal
from pyclense.base import BaseCleaner

class DuplicateCleaner:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_dupes(self) -> pd.DataFrame:
        return self.df[self.df.duplicated(keep=False)].reset_index(drop=True)

    def tag_dupes(self, tag_column: str = "is_duplicate") -> pd.DataFrame:
        df_tagged = self.df.copy()
        df_tagged[tag_column] = self.df.duplicated(keep=False)
        return df_tagged

    def cull_dupes(self, keep: Literal["first", "last", False] = "first") -> pd.DataFrame:
        return self.df.drop_duplicates(keep=keep).reset_index(drop=True)

# --- Example Usage ---

data = {
    'ID': [101, 102, 101, 103, 102, 104, 105, 104],
    'Name': ['Alice', 'Bob', 'Alice', 'Charlie', 'Bob', 'Eve', 'Frank', 'Eve'],
    'Value': [100, 200, 100, 300, 200, 400, 500, 400]
}

df = pd.DataFrame(data)

print("--- 📝 Original DataFrame (Total Rows: 8) ---")
print(df)
print("-" * 40)

# Initialize the cleaner
cleaner = DuplicateCleaner(df.copy()) # Use a copy to ensure immutability

## A. Identify Duplicates (get_dupes)
duplicates_df = cleaner.get_dupes()
print("--- 🔎 Identified Duplicates (keep=False) ---")
print(duplicates_df)
print(f"\nTotal Duplicated Rows (including first instance): **{len(duplicates_df)}**")
print("-" * 40)

## B. Tag Duplicates (tag_dupes)
# This method now returns a new DataFrame with the tag, which is more predictable.
tagged_df = cleaner.tag_dupes(tag_column="is_dupe")
print("--- 🏷️ Tagged Duplicates (New DataFrame) ---")
print(tagged_df)
print("-" * 40)

## C. Cull Duplicates (cull_dupes)
final_df = cleaner.cull_dupes(keep="first")
print("--- ✂️ Final Cleaned DataFrame (keep='first') ---")
print(final_df)
print(f"\nRemaining Rows: **{len(final_df)}**")