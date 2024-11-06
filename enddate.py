import pandas as pd
import requests
from datetime import datetime
import logging
import getpass
import os

# Setup logging to a file in the same directory as the script
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), 'project_update.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def read_uuids_from_excel(file_name):
    """Reads UUIDs from an Excel file in the same directory."""
    df = pd.read_excel(file_name)
    return df['UUID'].dropna().tolist()

def fetch_project_data(uuid, base_url, headers):
    """Fetch project data for a specific UUID."""
    url = f"https://{base_url}/ws/api/projects/{uuid}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        logging.info(f"Successfully fetched data for UUID: {uuid}")
        return response.json()
    else:
        logging.warning(f"Failed to fetch data for UUID: {uuid} - Status Code: {response.status_code}")
        return None

def calculate_end_date(start_date_str):
    """Calculate the end date by adding 3 years to the start date."""
    start_year = int(start_date_str[:4])
    end_year = start_year + 3
    # Replace the year in the end date with the calculated end year
    end_date = f"{end_year}{start_date_str[4:]}"
    return end_date

def update_project_end_date(uuid, start_date, end_date, base_url, headers):
    """Update the project with the calculated end date."""
    url = f"https://{base_url}/ws/api/projects/{uuid}"
    data = {
        "period": {
            "startDate": start_date,
            "endDate": end_date
        }
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 200:
        logging.info(f"Successfully updated end date for UUID: {uuid} - Start Date: {start_date}, End Date: {end_date}")
    else:
        logging.warning(f"Failed to update end date for UUID: {uuid} - Status Code: {response.status_code}")

def add_project_note(uuid, base_url, headers, username):
    """Add a note to the project indicating a presumed inactive status and estimated end date."""
    url = f"https://{base_url}/ws/api/projects/{uuid}/notes"
    data = {
        "username": username,
        "text": "Project is presumed inactive, and an estimated end date has been assigned. Best regards, The VBN Team."
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 200:
        logging.info(f"Successfully added note for UUID: {uuid}")
    else:
        logging.warning(f"Failed to add note for UUID: {uuid} - Status Code: {response.status_code}")

def main():
    """Main function to process each UUID and update the end date and notes."""
    # Secure input for base domain, API key, and Pure username
    base_domain = input("Enter the base domain for the API (e.g., pure123.elsevierpure.com): ")
    api_key = getpass.getpass("Enter the API key: ")
    pure_username = input("Enter your Pure username: ")

    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }

    # Specify the Excel file name in the same directory
    file_name = "enddates.xlsx"
    uuids = read_uuids_from_excel(file_name)
    
    # Confirm with the user before executing modifications
    confirm = input(f"About to modify {len(uuids)} projects. Do you want to proceed? (yes/no): ")
    if confirm.lower() != "yes":
        print("Operation canceled.")
        return

    # Log the start of the script execution
    logging.info("Script execution started.")

    modified_count = 0  # Counter for the number of modified projects

    for uuid in uuids:
        project_data = fetch_project_data(uuid, base_domain, headers)
        if project_data and "period" in project_data and "startDate" in project_data["period"]:
            start_date = project_data["period"]["startDate"]
            # Check if an end date already exists
            if "endDate" in project_data["period"]:
                logging.info(f"End date already exists for UUID: {uuid}, skipping update.")
                continue
            # Calculate the new end date and update
            end_date = calculate_end_date(start_date)
            update_project_end_date(uuid, start_date, end_date, base_domain, headers)
            add_project_note(uuid, base_domain, headers, pure_username)
            modified_count += 1
        else:
            logging.warning(f"No start date found for UUID: {uuid}")

    # Log the end of the script execution
    logging.warning(f"Total projects modified: {modified_count}")
    logging.info("Script execution finished.")

# Run the main function
if __name__ == "__main__":
    main()
