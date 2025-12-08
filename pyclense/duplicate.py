import pandas as pd

class DuplicateHandler:
    def __init__(self, df):
        self.df = df

    def handle_duplicates(self, action='remove'):
        """
        Handles duplicate rows in the dataframe.

        Args:
            action (str): 
                - 'remove': Drops duplicate rows (default).
                - 'blank': Replaces values in duplicate rows with empty strings,
                           keeping the row in the dataset (soft delete).
        """
        # Identify duplicates (mark True for all duplicates except the first occurrence)
        dup_mask = self.df.duplicated(keep='first')
        dup_count = dup_mask.sum()

        if dup_count == 0:
            print("No duplicate rows found.")
        else:
            if action == 'remove':
                self.df.drop_duplicates(inplace=True)
                print(f"Action 'remove': Dropped {dup_count} duplicate rows.")
                
            elif action == 'blank':
                # Set all columns for the duplicate rows to an empty string
                self.df.loc[dup_mask, :] = ""
                print(f"Action 'blank': Blanked content of {dup_count} duplicate rows.")

        return self.df