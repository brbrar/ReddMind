import pandas as pd
import os

FILE_PATH = "history.csv"


def save_history(title, verdict):
    """Save analysis history to a CSV file."""

    new_entry = pd.DataFrame([[title, verdict]], columns=["Title", "Verdict"])

    if not os.path.exists(FILE_PATH):
        new_entry.to_csv(FILE_PATH, index=False)
    else:
        new_entry.to_csv(FILE_PATH, mode="a", header=False, index=False)


def load_history():
    """Load analysis history from a CSV file."""

    if os.path.exists(FILE_PATH):
        return pd.read_csv(FILE_PATH)
    else:
        return pd.DataFrame
