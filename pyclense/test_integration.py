from pyclense import BaseCleaner, Standardizer, DuplicateHandler, MissingValueHandler

# 1. Initialize and Load
# Note: Ensure the file path is correct. If 'mydata' folder doesn't exist, it might fail.
cleaner = BaseCleaner("mydata/dataset.csv")
df = cleaner.load_data(header=1)

# 2. Standardize Data
std = Standardizer(df)

# The methods 'strip_whitespace' and 'normalize_dashes' do not exist in the Standardizer class.
# Instead, we use 'clean_column_names' which handles stripping and title casing.
std.clean_column_names() 

# If you need to clean specific columns like currency, you can add that logic 
# or use 'standardize_dates' if applicable.
# std.standardize_dates(subset=['Date Column'])

# 3. Handle Duplicates
dup = DuplicateHandler(df)
# Updated method name from 'remove_duplicates' to 'handle_duplicates' with action='remove'
dup.handle_duplicates(action='remove')

# 4. Handle Missing Values
miss = MissingValueHandler(df)
# Updated argument from 'method' to 'action' and value to 'drop_rows'
miss.handle_missing(action='drop_rows')

# 5. Save
# Sync the dataframe back to the cleaner before saving to ensure latest changes are kept
cleaner.set_data(df) 
cleaner.save_data("mydata/cleaned_dataset.csv")