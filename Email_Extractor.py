import json
import os
from datetime import datetime

def extract_emails_from_json(file_path):
    """
    Extract emails from a JSON file on Windows.
    
    Args:
        file_path (str): Path to the JSON file
    
    Returns:
        list: A list of extracted email addresses
    """
    try:
        # Normalize the file path for Windows
        normalized_path = os.path.normpath(file_path)
        
        # Open and load the JSON file
        with open(normalized_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # List to store extracted emails
        extracted_emails = []
        
        # Function to recursively search for emails
        def find_emails(obj):
            # If the input is a dictionary
            if isinstance(obj, dict):
                for key, value in obj.items():
                    # If the key is 'email', add the value to extracted emails
                    if key.lower() == 'email':
                        if isinstance(value, str):
                            extracted_emails.append(value)
                    # Recursively search nested structures
                    elif isinstance(value, (dict, list)):
                        find_emails(value)
            
            # If the input is a list
            elif isinstance(obj, list):
                for item in obj:
                    find_emails(item)
        
        # Start the recursive search
        find_emails(data)
        
        return extracted_emails
    
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file {file_path}")
        return []
    except PermissionError:
        print(f"Error: Permission denied when trying to access {file_path}")
        return []

def save_emails_to_file(emails, input_file_path):
    """
    Save extracted emails to a text file.
    
    Args:
        emails (list): List of email addresses
        input_file_path (str): Original input file path
    
    Returns:
        str: Path to the output file
    """
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), 'email_extracts')
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    input_filename = os.path.splitext(os.path.basename(input_file_path))[0]
    output_filename = f"emails_{input_filename}_{timestamp}.txt"
    output_path = os.path.join(output_dir, output_filename)
    
    # Write emails to file
    try:
        with open(output_path, 'w', encoding='utf-8') as outfile:
            for email in emails:
                outfile.write(email + '\n')
        
        print(f"\nEmails saved to: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error saving emails: {e}")
        return None

# Example usage
def main():
    # Prompt user for the file path
    file_path = input("Enter the full path to your JSON file: ").strip('"')
    
    # Extract emails
    emails = extract_emails_from_json(file_path)
    
    # Print extracted emails to console
    if emails:
        print("\nExtracted Emails:")
        for email in emails:
            print(email)
        
        # Save emails to file
        save_emails_to_file(emails, file_path)
    else:
        print("No emails found.")

# Pause to keep the console window open
if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")
