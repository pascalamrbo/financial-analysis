import pandas as pd

def validate_trial_balance(df: pd.DataFrame):
    """
    Basic + advanced checks for a trial balance DataFrame:
      - Must have [Account, Debit, Credit] columns
      - Check if Debits == Credits
      - Check for negative debits or credits
      - Identify extremely large balances
    Returns (errors, warnings).
    """
    errors = []
    warnings = []

    required_cols = ["Account","Debit","Credit"]
    for col in required_cols:
        if col not in df.columns:
            errors.append(f"Missing column: {col}")
            return errors, warnings

    total_debit = df["Debit"].sum()
    total_credit = df["Credit"].sum()

    # 1) Basic balance check
    if abs(total_debit - total_credit) > 0.0001:
        errors.append(f"TB out of balance. Debits={total_debit}, Credits={total_credit}")

    # 2) Negative debits or credits
    negative_debits = df[df["Debit"] < 0]
    if not negative_debits.empty:
        warnings.append(f"{len(negative_debits)} rows have negative debits, unusual for a TB.")
    negative_credits = df[df["Credit"] < 0]
    if not negative_credits.empty:
        warnings.append(f"{len(negative_credits)} rows have negative credits, unusual for a TB.")

    # 3) Large balances
    # You might define "large" as above X million
    threshold = 10_000_000
    df["Net"] = df["Debit"] - df["Credit"]
    big_balances = df[abs(df["Net"]) >= threshold]
    if not big_balances.empty:
        warnings.append(
            f"{len(big_balances)} accounts with net balances >= {threshold:,} (Possible outliers?)."
        )

    # 4) Could also check for missing typical accounts
    # e.g., if "Retained Earnings" or "Cash" accounts are missing, you might flag an error

    return errors, warnings
