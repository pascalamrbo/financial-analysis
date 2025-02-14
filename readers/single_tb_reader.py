import pandas as pd

def read_single_tb_excel_dynamic(filepath_or_buffer):
    """
    Reads a single trial balance (one set of Debit/Credit columns) from Excel.
    Dynamically finds the row where "Debit" and "Credit" appear as headers.

    Returns a DataFrame with columns ["Account", "Debit", "Credit"].
    """

    temp_df = pd.read_excel(filepath_or_buffer, header=None, dtype=str)
    header_row_index = None
    max_rows_to_check = min(20, len(temp_df))

    for i in range(max_rows_to_check):
        row_values = temp_df.iloc[i].fillna("").str.lower().str.strip().tolist()
        if "debit" in row_values and "credit" in row_values:
            header_row_index = i
            # Debug: print(f"Detected header at row {i}: {row_values}")
            break

    if header_row_index is None:
        raise ValueError(
            "Could not find a row containing 'Debit' and 'Credit' within the first 20 rows."
        )

    # Now read again, telling Pandas that row is the header
    df = pd.read_excel(
        filepath_or_buffer,
        header=header_row_index,
        skiprows=header_row_index + 1,
        dtype=str
    )

    # Lowercase columns
    df.columns = [col.lower().strip() for col in df.columns]

    # Identify account column (improved synonyms)
    possible_acct_cols = [
        c for c in df.columns
        if any(keyword in c for keyword in ["account", "acct", "name", "description"])
    ]
    if possible_acct_cols:
        account_col = possible_acct_cols[0]
    else:
        # fallback
        account_col = df.columns[0]

    if "debit" not in df.columns or "credit" not in df.columns:
        raise ValueError("Failed to find columns named 'debit'/'credit' after dynamic detection.")

    # Rename to standard
    df.rename(columns={
        account_col: "Account",
        "debit": "Debit",
        "credit": "Credit"
    }, inplace=True)

    # Keep only these columns
    df = df[["Account", "Debit", "Credit"]]

    # Convert numeric
    df["Debit"] = pd.to_numeric(df["Debit"], errors="coerce").fillna(0.0)
    df["Credit"] = pd.to_numeric(df["Credit"], errors="coerce").fillna(0.0)

    # Clean up account
    df["Account"] = df["Account"].astype(str).str.strip()
    df = df[df["Account"] != ""]

    df.reset_index(drop=True, inplace=True)
    return df
