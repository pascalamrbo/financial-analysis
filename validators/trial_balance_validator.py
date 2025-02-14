def validate_trial_balance_debits_equal_credits(data):
    """
    Validates if total debits equal total credits in a Trial Balance data set.

    Args:
        data (list): A list of dictionaries representing Trial Balance data.
                       Each dictionary should have 'Debit' and 'Credit' keys
                       (case-insensitive). Debit and Credit values should be convertible to numbers.

    Returns:
        dict: A dictionary containing validation results:
              {'is_valid': True/False, 'errors': [list of error messages]}
              'errors' will be an empty list if validation is successful.
    """
    total_debits = 0
    total_credits = 0
    errors = []

    if not data:
        return {'is_valid': False, 'errors': ["Trial Balance data is empty."]}

    for row in data:
        try:
            debit = float(row.get('debit', 0)) # Get debit, default to 0 if missing, convert to float
            credit = float(row.get('credit', 0)) # Get credit, default to 0 if missing, convert to float
            total_debits += debit
            total_credits += credit
        except ValueError:
            errors.append(f"Invalid debit or credit value in row: {row}. Must be a number.")
        except Exception as e:
            errors.append(f"Error processing row: {row}. Error: {e}")

    if errors: # If there were errors during data processing, validation fails
        return {'is_valid': False, 'errors': errors}

    if abs(total_debits - total_credits) > 1e-6: # Use a small tolerance for floating point comparison
        errors.append(f"Trial Balance is unbalanced. Total Debits: {total_debits:.2f}, Total Credits: {total_credits:.2f}")
        return {'is_valid': False, 'errors': errors}
    else:
        return {'is_valid': True, 'errors': []} # Validation successful


if __name__ == '__main__':
    # Example Usage and Testing
    valid_tb_data = [
        {'Account': 'Cash', 'Debit': '1000', 'Credit': '0'},
        {'Account': 'Accounts Payable', 'Debit': '0', 'Credit': '500'},
        {'Account': 'Equity', 'Debit': '0', 'Credit': '500'},
    ]

    invalid_tb_data = [
        {'Account': 'Cash', 'Debit': '1000', 'Credit': '0'},
        {'Account': 'Accounts Payable', 'Debit': '100', 'Credit': '500'}, # Unbalanced
    ]

    data_with_errors = [
        {'Account': 'Cash', 'Debit': 'abc', 'Credit': '0'}, # Invalid debit value
        {'Account': 'Accounts Payable', 'Debit': '0', 'Credit': '500'},
    ]

    validation_result_valid = validate_trial_balance_debits_equal_credits(valid_tb_data)
    print(f"Valid Trial Balance Validation Result: {validation_result_valid}") # Expected: {'is_valid': True, 'errors': []}

    validation_result_invalid = validate_trial_balance_debits_equal_credits(invalid_tb_data)
    print(f"Invalid Trial Balance Validation Result: {validation_result_invalid}") # Expected: {'is_valid': False, 'errors': ['Trial Balance is unbalanced...']}

    validation_result_errors = validate_trial_balance_debits_equal_credits(data_with_errors)
    print(f"Trial Balance with Data Errors Result: {validation_result_errors}") # Expected: {'is_valid': False, 'errors': ['Invalid debit or credit value in row...']}