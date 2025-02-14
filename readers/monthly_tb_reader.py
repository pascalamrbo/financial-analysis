import pandas as pd
import datetime, re

def read_monthly_tb_excel_dynamic(filepath):
    """
    Reads a wide monthly TB with multiple Debit/Credit pairs:
      - 1 row for months (e.g., "Jan. 2024", "Feb. 2024", etc.)
      - 1 row below it with 'Debit'/'Credit' repeated.

    Dynamically scans the first 20 rows to find that 2-row header.
    Returns a DataFrame with columns: [Account, Month, Debit, Credit].
    """

    # Read entire sheet with no header
    temp_df = pd.read_excel(filepath, header=None, dtype=str)
    nrows = len(temp_df)

    header_row_pair = None
    max_rows_to_check = min(20, nrows)

    for i in range(max_rows_to_check - 1):
        row1 = temp_df.iloc[i].fillna("").str.lower().str.strip().tolist()
        row2 = temp_df.iloc[i+1].fillna("").str.lower().str.strip().tolist()

        # Very simplistic check: row2 should have at least one "debit" and one "credit"
        if "debit" in row2 and "credit" in row2:
            header_row_pair = (i, i+1)
            break

    if not header_row_pair:
        raise ValueError(
            "Could not find a 2-row header that includes 'Debit'/'Credit' across columns. "
            "Check the file format or row layout."
        )

    # Now read again with multi-row header
    df = pd.read_excel(
        filepath,
        header=[header_row_pair[0], header_row_pair[1]],
        dtype=str
    )

    # Drop entirely empty columns
    df.dropna(how="all", axis=1, inplace=True)
    # Drop entirely empty rows
    df.dropna(how="all", axis=0, inplace=True)

    # Force the first column to be "Account"
    old_first_col = df.columns[0]
    df.rename(columns={old_first_col: ("Account", "Account")}, inplace=True)

    # Melt from wide to long
    df_long = df.melt(
        id_vars=[("Account","Account")],
        var_name=["MonthCol","Type"],
        value_name="Amount"
    )

    df_long.rename(columns={("Account","Account"): "Account"}, inplace=True)

    # Parse the MonthCol (e.g., 'Jan. 2024') => datetime or keep as string
    df_long["Month"] = df_long["MonthCol"].apply(_parse_month_year)
    df_long.drop(columns=["MonthCol"], inplace=True)

    # Pivot so we get separate Debit/Credit columns
    df_result = df_long.pivot_table(
        index=["Account","Month"],
        columns="Type",
        values="Amount",
        aggfunc="sum"
    ).reset_index()

    # Ensure columns exist
    for col in ["Debit","Credit"]:
        if col not in df_result.columns:
            df_result[col] = 0.0

    df_result = df_result[["Account","Month","Debit","Credit"]]

    # Convert numeric
    df_result["Debit"] = pd.to_numeric(df_result["Debit"], errors="coerce").fillna(0.0)
    df_result["Credit"] = pd.to_numeric(df_result["Credit"], errors="coerce").fillna(0.0)

    # Clean up account
    df_result["Account"] = df_result["Account"].astype(str).str.strip()
    df_result = df_result[df_result["Account"] != ""]

    # Sort by Month if wanted
    df_result.sort_values(by=["Month", "Account"], inplace=True, ignore_index=True)

    return df_result

def _parse_month_year(text):
    """
    Converts strings like 'Jan. 2024' to a date object of the 1st of that month.
    If parse fails, returns the original text.

    Improved to handle possible variations (e.g., "Jan 24", "January 2024").
    """
    if not isinstance(text, str):
        return text

    text = text.strip().replace(".", "")
    # e.g. 'January 2024', 'JAN 2024', 'Jan 24'
    pattern = r"([A-Za-z]+)\s+(\d{2,4})"
    match = re.search(pattern, text)
    if match:
        month_str = match.group(1)[:3].capitalize()  # e.g. 'Jan'
        year_str = match.group(2)
        month_map = {
            "Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6,
            "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12
        }
        if month_str in month_map:
            mm = month_map[month_str]
            yyyy = int(year_str)
            # Adjust 2-digit year if needed
            if yyyy < 100:
                yyyy += 2000
            try:
                return datetime.date(yyyy, mm, 1)
            except ValueError:
                return text
    return text
