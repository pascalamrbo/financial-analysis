import datetime

def validate_general_ledger_data(data):
    """
    Validates General Ledger data for required fields and data types.

    Args:
        data (list): A list of dictionaries representing General Ledger transaction data.
                       Each dictionary is expected to have keys like 'Date', 'Account',
                       'Description', and 'Amount' (case-insensitive).

    Returns:
        dict: A dictionary containing validation results:
              {'is_valid': True/False, 'errors': [list of error messages]}
              'errors' will be a list of error messages if validation fails,
              or an empty list if validation is successful.
    """
    errors = []
    required_headers = ['date', 'account', 'description', 'amount'] # Expected headers (lowercase for matching)

    if not data:
        return {'is_valid': False, 'errors': ["General Ledger data is empty."]}

    # Check for required headers in the first row (if headers are present)
    if data and data[0]:
        data_headers = [header.lower() for header in data[0].keys() if header] # Get headers, lowercase
        missing_headers = [header for header in required_headers if header not in data_headers]
        if missing_headers:
            errors.append(f"Missing required headers: {', '.join(missing_headers)}. Required headers are: {', '.join(required_headers)}")
            return {'is_valid': False, 'errors': errors} # Early exit if required headers are missing


    for index, row in enumerate(data):
        row_num = index + 1 # For user-friendly error messages (row numbers start from 1)

        # Check for missing required fields in each row
        for header in required_headers:
            if not row.get(header): # Use .get() to avoid KeyError, handles missing columns
                errors.append(f"Row {row_num}: Missing required field: '{header}'.")

        # Validate 'Date' field
        date_str = row.get('date')
        if date_str:
            try:
                datetime.datetime.strptime(date_str, '%Y-%m-%d') # Example date format, adjust if needed
            except ValueError:
                errors.append(f"Row {row_num}: Invalid date format in 'Date' field. Expected format: YYYY-MM-DD, got: '{date_str}'.")

        # Validate 'Amount' field
        amount_str = row.get('amount')
        if amount_str:
            try:
                float(amount_str) # Try converting to float to check if it's numeric
            except ValueError:
                errors.append(f"Row {row_num}: Invalid numeric format in 'Amount' field: '{amount_str}'.")

    if errors:
        return {'is_valid': False, 'errors': errors}
    else:
        return {'is_valid': True, 'errors': []}


if __name__ == '__main__':
    # Example Usage and Testing

    valid_gl_data = [
        {'Date': '2023-10-27', 'Account': 'Sales Revenue', 'Description': 'Online Sale', 'Amount': '150.00'},
        {'Date': '2023-10-26', 'Account': 'Rent Expense', 'Description': 'Office Rent - Oct', 'Amount': '-2500.00'},
    ]

    invalid_gl_data_missing_fields = [
        {'Date': '2023-10-27', 'Account': 'Sales Revenue', 'Amount': '150.00'}, # Missing 'Description'
        {'Account': 'Rent Expense', 'Description': 'Office Rent - Oct', 'Amount': '-2500.00'}, # Missing 'Date'
    ]

    invalid_gl_data_bad_data = [
        {'Date': '2023-10-27', 'Account': 'Sales Revenue', 'Description': 'Online Sale', 'Amount': 'abc'}, # Invalid Amount
        {'Date': '2023/10/26', 'Account': 'Rent Expense', 'Description': 'Office Rent - Oct', 'Amount': '-2500.00'}, # Invalid Date format
    ]

    validation_result_valid = validate_general_ledger_data(valid_gl_data)
    print(f"Valid GL Data Validation Result: {validation_result_valid}") # Expected: {'is_valid': True, 'errors': []}

    validation_result_missing_fields = validate_general_ledger_data(invalid_gl_data_missing_fields)
    print(f"Invalid GL Data (Missing Fields) Result: {validation_result_missing_fields}")
    # Expected: {'is_valid': False, 'errors': [...'Missing required field: 'description'...'Missing required field: 'date'...]}

    validation_result_bad_data = validate_general_ledger_data(invalid_gl_data_bad_data)
    print(f"Invalid GL Data (Bad Data) Result: {validation_result_bad_data}")
    # Expected: {'is_valid': False, 'errors': [...'Invalid numeric format in 'Amount' field...'Invalid date format in 'Date' field...']}