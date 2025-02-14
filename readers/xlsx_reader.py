import openpyxl

def read_xlsx_file(file_path):
    """
    Reads data from an XLSX (Excel) file.

    Args:
        file_path (str): The path to the XLSX file.

    Returns:
        list: A list of dictionaries, where each dictionary represents a row
              in the XLSX file. The keys are the header names from the first row.
              Returns an empty list if there's an error reading the file.
    """
    data = []
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active  # Get the active sheet

        header_row = [cell.value for cell in sheet[1]]  # Assume headers are in the first row

        for row_num in range(2, sheet.max_row + 1):  # Start from row 2 (after headers)
            row_values = [cell.value for cell in sheet[row_num]]
            row_dict = {}
            for i, header in enumerate(header_row):
                if header: # Ensure header is not None
                    row_dict[header] = row_values[i] if i < len(row_values) else None # Handle potential shorter rows
            data.append(row_dict)

    except FileNotFoundError:
        print(f"Error: File not found at path: {file_path}")
        return []  # Return empty list to indicate failure
    except Exception as e:
        print(f"Error reading XLSX file: {e}")
        return []  # Return empty list to indicate failure
    return data

if __name__ == '__main__':
    # Example usage (for testing the XLSX reader module independently)
    example_file = 'yourfile.xlsx'  # Replace with a sample XLSX file for testing
    data = read_xlsx_file(example_file)
    if data:
        print(f"Data read from {example_file}:")
        for row in data[:5]: # Print first 5 rows as example
            print(row)
    else:
        print(f"No data read from {example_file} or an error occurred.")