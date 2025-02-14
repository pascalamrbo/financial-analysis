import openpyxl
import pandas as pd

def read_gl_excel_dynamic(filepath):
    """
    Reads a GL export from Excel, scanning the first ~20 rows with openpyxl
    to find a row containing 'Date' and 'Amount'. Then uses skiprows=i-1 in Pandas
    so that row becomes the header.

    Returns:
      (df, parse_info)
      - df: the cleaned pandas DataFrame.
      - parse_info: a dictionary with details about parse errors 
                    (e.g., invalid_dates, invalid_amounts).
    """
    wb = openpyxl.load_workbook(filepath, data_only=True)
    sheet = wb.active  # Use the active sheet or specify a sheet if needed

    header_row = None
    max_rows_to_check = 20

    # Function to check if a cell's value matches 'Amount' (including synonyms)
    def _matches_amount(cell_value):
        if cell_value is None:
            return False
        cell_value = str(cell_value).lower().strip()
        return cell_value in ["amount", "amt", "total amount"]

    # 1) Identify the header row by scanning the first 20 rows
    for i, row in enumerate(sheet.iter_rows(values_only=True), start=1):
        if i > max_rows_to_check:
            break
        row_str_values = [str(cell).lower().strip() if cell else "" for cell in row]
        if "date" in row_str_values and any(_matches_amount(val) for val in row):
            header_row = i
            break

    if header_row is None:
        raise ValueError(
            "Could not find a row containing 'Date' and 'Amount' within the first 20 rows. "
            "Check the file format or merged cells."
        )

    # 2) Read the Excel file with Pandas (all columns as strings)
    df = pd.read_excel(
        filepath,
        skiprows=header_row - 1,
        header=0,  # The detected row becomes the header
        dtype=str
    )

    # 3) Normalize column names to lowercase and strip extra spaces
    df.columns = [col.lower().strip() for col in df.columns]

    # 4) Map columns to canonical names
    col_map = {
        "date": "Date",
        "transaction type": "Transaction Type",
        "#": "#",
        "number": "#",
        "name": "Name",
        "memo": "Memo/Description",
        "description": "Memo/Description",
        "memo/description": "Memo/Description",
        "split": "Split",
        "amount": "Amount",
        "balance": "Balance"
    }
    # Handle any synonyms for "Amount"
    for c in df.columns:
        if c.startswith("amount") or c.startswith("amt"):
            col_map[c] = "Amount"

    final_cols = {}
    for c in df.columns:
        if c in col_map:
            final_cols[c] = col_map[c]
    df.rename(columns=final_cols, inplace=True)

    # 5) Keep only the relevant columns
    keep_cols = [
        "Date",
        "Transaction Type",
        "#",
        "Name",
        "Memo/Description",
        "Split",
        "Amount",
        "Balance"
    ]
    existing_cols = [c for c in keep_cols if c in df.columns]
    df = df[existing_cols]

    # 6) Clean up text columns using .str.strip() so we don't call .strip() on a Series
    text_cols = ["Date", "Transaction Type", "#", "Name", "Memo/Description", "Split"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str).str.strip()

    # 7) Prepare a parse_info dictionary to track conversion issues
    parse_info = {"invalid_dates": 0, "invalid_amounts": 0}

    # Convert Balance column to numeric if it exists
    if "Balance" in df.columns:
        df["Balance"] = pd.to_numeric(df["Balance"], errors="coerce")

    # 8) Convert the Date column to datetime and store as 'parsed_date'
    df["parsed_date"] = pd.to_datetime(df["Date"], errors="coerce")
    invalid_date_mask = df["Date"].astype(bool) & df["parsed_date"].isna()
    parse_info["invalid_dates"] = invalid_date_mask.sum()

    # 9) Convert the Amount column to numeric and store as 'parsed_amount'
    if "Amount" in df.columns:
        df["parsed_amount"] = pd.to_numeric(df["Amount"], errors="coerce")
        invalid_amount_mask = df["Amount"].astype(bool) & df["parsed_amount"].isna()
        parse_info["invalid_amounts"] = invalid_amount_mask.sum()
    else:
        df["parsed_amount"] = None

    # 10) Remove rows that are completely empty (both parsed_date and parsed_amount missing)
    mask_keep = df["parsed_date"].notna() | df["parsed_amount"].notna()
    df = df[mask_keep].copy()
    df.reset_index(drop=True, inplace=True)

    return df, parse_info
