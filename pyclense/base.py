import pandas as pd
import os

class BaseCleaner:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

    def load_data(self, **kwargs):
        """
        Loads data from CSV. 
        kwargs can be used for pd.read_csv arguments (e.g., header=1).
        """
        if not os.path.exists(self.filepath):
            # Fallback for demonstration if file doesn't exist in 'mydata'
            if os.path.exists(os.path.basename(self.filepath)):
                self.filepath = os.path.basename(self.filepath)
            else:
                raise FileNotFoundError(f"File not found: {self.filepath}")
        
        self.df = pd.read_csv(self.filepath, **kwargs)
        print(f"Data loaded successfully. Shape: {self.df.shape}")
        return self.df

    def save_data(self, output_path):
        """Saves the current dataframe to a CSV file."""
        if self.df is not None:
            # Ensure directory exists if path contains one
            directory = os.path.dirname(output_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                
            self.df.to_csv(output_path, index=False)
            print(f"Data saved to {output_path}")
        else:
            print("No data to save.")

    def set_data(self, df):
        self.df = df