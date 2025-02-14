import pandas as pd

def validate_gl(df: pd.DataFrame, parse_info=None):
    """
    GL validation checks:
      - Use parse_info for invalid date/amount messages.
      - Check negative amounts, weekend postings, date order, and large transactions.
    Returns (errors, warnings).
    """
    errors = []
    warnings = []

    if parse_info is None:
        parse_info = {"invalid_dates": 0, "invalid_amounts": 0}

    # Report parse errors if any
    if parse_info.get("invalid_dates", 0) > 0:
        errors.append(f"{parse_info['invalid_dates']} rows have invalid date formats (GL).")
    if parse_info.get("invalid_amounts", 0) > 0:
        errors.append(f"{parse_info['invalid_amounts']} rows have non-numeric or blank 'Amount' (GL).")

    # Check negative amounts
    if "parsed_amount" in df.columns:
        negative_rows = df[df["parsed_amount"] < 0]
        if not negative_rows.empty:
            warnings.append(f"{len(negative_rows)} transactions have negative amounts. Verify if this is expected.")

    # Check weekend postings
    if "parsed_date" in df.columns:
        weekend_mask = df["parsed_date"].dt.weekday >= 5  # Saturday=5, Sunday=6
        weekend_postings = df[weekend_mask]
        if not weekend_postings.empty:
            warnings.append(f"{len(weekend_postings)} transactions posted on weekends. Investigate unusual postings.")
        if not df["parsed_date"].is_monotonic_increasing:
            warnings.append("GL is not sorted by date. Transactions may be out of chronological order.")

    # Large transactions check
    threshold = 1_000_000
    if "parsed_amount" in df.columns:
        large_mask = df["parsed_amount"].abs() >= threshold
        if large_mask.any():
            warnings.append(f"{large_mask.sum()} transactions >= {threshold}. Potential large transactions.")

    return errors, warnings
