import pandas as pd
from pyclense.standardizer import Standardizer

# Setup Data
df = pd.DataFrame({'Event_Date': ['2023-01-01', '01/02/2023', 'Jan 3, 2023', '2023.04.05']})
print("❌ BEFORE:\n", df)

# Run Test
cleaner = Standardizer(df)
cleaner.standardize_dates(['Event_Date'])

print("\n✅ AFTER (Should be MM/DD/YYYY):\n", cleaner.get_dataframe())