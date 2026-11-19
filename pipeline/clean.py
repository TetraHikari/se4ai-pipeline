"""Stage 2: clean -- fix types and drop rows we cannot trust."""
import pandas as pd


def clean_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy of the raw sales.

    Guarantees for the next stage:
      * sold_date is a datetime column
      * sqft has no missing values
      * rows with an obviously wrong price (<= 10,000) are removed
    """
    df = df.copy()
    # The 2025 export writes plain dates ("2025-05-01"); the 2026 export writes
    # timestamps with a timezone ("2026-02-23T10:30:00+07:00"). ISO8601 reads both,
    # and utc=True puts them all in one timezone so the column has a single dtype.
    df["sold_date"] = pd.to_datetime(df["sold_date"], format="ISO8601", utc=True)
    # Some 2026 listings have no square footage. sqft is the strongest price signal,
    # so we drop those rows rather than invent a value for it.
    df = df.dropna(subset=["sqft"])
    df = df[df["price"] > 10_000]  # drop obvious data-entry errors (price typos)
    return df
