import csv

def read_csv_file(file_path):
    """
    Reads data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        list: A list of dictionaries, where each dictionary represents a row
              in the CSV file and keys are the header names.
              Returns an empty list if there's an error reading the file.
    """
    data = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                data.append(row)
    except FileNotFoundError:
        print(f"Error: File not found at path: {file_path}")
        return []  # Return empty list to indicate failure
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []  # Return empty list to indicate failure
    return data

if __name__ == '__main__':
    # Example usage (for testing the reader module independently)
    example_file = 'yourfile.csv'  # Replace with a sample CSV file for testing
    data = read_csv_file(example_file)
    if data:
        print(f"Data read from {example_file}:")
        for row in data[:5]: # Print first 5 rows as example
            print(row)
    else:
        print(f"No data read from {example_file} or an error occurred.")