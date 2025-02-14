def identify_document_type(data):
    """
    Identifies the type of financial document based on column headers.

    Args:
        data (list): A list of dictionaries representing the data read from a file.
                       Each dictionary is assumed to represent a row, and keys are column headers.

    Returns:
        str: The identified document type. Possible values:
             "Trial Balance", "General Ledger", "P&L", "Balance Sheet", "Unknown".
             Returns "Unknown" if the document type cannot be confidently identified.
    """
    if not data or not data[0]:  # Check if data is empty or has no headers
        return "Unknown"

    headers = [header.lower() for header in data[0].keys() if header] # Get headers, lowercase for easier matching

    # Keywords to identify document types (case-insensitive)
    trial_balance_keywords = ["account number", "account name", "debit", "credit", "trial balance"]
    general_ledger_keywords = ["account", "description", "amount", "date", "transaction", "general ledger"]
    profit_loss_keywords = ["revenue", "sales", "cost of goods sold", "expenses", "net income", "profit and loss", "income statement"]
    balance_sheet_keywords = ["assets", "liabilities", "equity", "balance sheet", "statement of financial position"]

    def has_keywords(headers_list, keywords_list, threshold=2):
        """Checks if at least 'threshold' keywords from keywords_list are present in headers_list."""
        count = sum(1 for keyword in keywords_list if any(keyword in header for header in headers_list))
        return count >= threshold

    if has_keywords(headers, trial_balance_keywords):
        return "Trial Balance"
    elif has_keywords(headers, general_ledger_keywords):
        return "General Ledger"
    elif has_keywords(headers, profit_loss_keywords):
        return "P&L" # Profit & Loss Statement
    elif has_keywords(headers, balance_sheet_keywords):
        return "Balance Sheet"
    else:
        return "Unknown"

if __name__ == '__main__':
    # Example Usage and Testing
    # You would typically get 'data' from reading a CSV or XLSX file
    # For testing, let's create some sample data (list of dictionaries)

    # Sample Trial Balance Data (simulated)
    sample_tb_data = [
        {"Account Number": "101", "Account Name": "Cash", "Debit": "1000", "Credit": "0"},
        {"Account Number": "201", "Account Name": "Accounts Payable", "Debit": "0", "Credit": "500"},
        {"Account Number": "301", "Account Name": "Equity", "Debit": "0", "Credit": "500"},
        {"Account Number": "...", "Account Name": "...", "Debit": "...", "Credit": "..."}
    ]

    # Sample General Ledger Data (simulated)
    sample_gl_data = [
        {"Date": "2023-10-26", "Account": "Cash", "Description": "Sales Revenue", "Amount": "1000", "Transaction ID": "TXN-001"},
        {"Date": "2023-10-26", "Account": "Rent Expense", "Description": "October Rent", "Amount": " -500", "Transaction ID": "TXN-002"},
        {"Date": "2023-10-27", "Account": "Accounts Receivable", "Description": "Invoice #123", "Amount": "2000", "Transaction ID": "TXN-003"},
        {"Date": "...", "Account": "...", "Description": "...", "Amount": "...", "Transaction ID": "..."}
    ]

    # Sample P&L Data (simulated)
    sample_pl_data = [
        {"Revenue": "100000", "Cost of Goods Sold": "40000", "Operating Expenses": "20000", "Net Income": "40000"},
        {"Revenue": "...", "Cost of Goods Sold": "...", "Operating Expenses": "...", "Net Income": "..."}
    ]

    # Sample Balance Sheet Data (simulated)
    sample_bs_data = [
        {"Assets": "500000", "Liabilities": "200000", "Equity": "300000"},
        {"Assets": "...", "Liabilities": "...", "Equity": "..."}
    ]


    print("Document Type Identification Examples:\n")

    doc_type_tb = identify_document_type(sample_tb_data)
    print(f"Sample Trial Balance Data identified as: {doc_type_tb}") # Expected: Trial Balance

    doc_type_gl = identify_document_type(sample_gl_data)
    print(f"Sample General Ledger Data identified as: {doc_type_gl}") # Expected: General Ledger

    doc_type_pl = identify_document_type(sample_pl_data)
    print(f"Sample P&L Data identified as: {doc_type_pl}") # Expected: P&L

    doc_type_bs = identify_document_type(sample_bs_data)
    print(f"Sample Balance Sheet Data identified as: {doc_type_bs}") # Expected: Balance Sheet

    doc_type_unknown = identify_document_type([{"Column1": "Value1", "Column2": "Value2"}]) # Unknown data
    print(f"Unknown Data identified as: {doc_type_unknown}") # Expected: Unknown

    doc_type_empty = identify_document_type([]) # Empty data
    print(f"Empty Data identified as: {doc_type_empty}") # Expected: Unknown