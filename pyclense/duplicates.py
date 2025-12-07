try:
    from .base import BaseCleaner
except ImportError:
    from base import BaseCleaner

class DuplicateCleaner(BaseCleaner):
    """Removes duplicate rows"""

    def detect(self):
        return self._df[self._df.duplicated()]

    def remove(self, keep="first"):
        before = len(self._df)
        self._df = self._df.drop_duplicates(keep=keep) 
        after = len(self._df)

        removed = before - after
        self.record_change(f"Removed {removed} duplicate rows")

        return self._df

    def clean(self):
        return self.remove()
