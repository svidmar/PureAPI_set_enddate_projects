
# Pure Project End Date Updater Script

This script is designed to automatically update projects in Pure without an assigned end date in Pure's API by setting an end date three years after the project start date. It then adds a note to indicate that the end date is estimated and that the project is presumed inactive. The script also provides logging for all actions and skips projects that already have an end date.

## Features

- **End Date Calculation**: Calculates an end date by adding three years to the project start date.
- **Conditional Updates**: Only updates projects that lack an existing end date.
- **Notes Addition**: Adds a standardized note to each project indicating that an estimated end date has been assigned.
- **Logging**: Records all actions, including skipped and successfully updated projects, with start and end dates logged for each.
- **User Confirmation**: Asks for user confirmation before proceeding with updates to ensure intended modifications.
- **Secure Runtime Inputs**: Prompts for sensitive information such as the API key and username securely at runtime.

## Prerequisites

- **Python 3.x**
- **Required Libraries**: Ensure the following Python packages are installed:
  ```bash
  pip install pandas requests openpyxl
  ```

## Setup

1. Clone this repository or download the script file (`enddate.py`).
2. Place the Excel file containing project UUIDs in the same directory as `enddate.py`.
3. Ensure the Excel file has a column named `UUID` with the project UUIDs you wish to process.

## Usage

1. **Run the Script**: Execute the script from your terminal:
   ```bash
   python enddate.py
   ```
2. **Input Required Information**: The script will prompt you to enter:
   - **API Base Domain**: The base domain for Pure's API (e.g., `pureinstance.elsevierpure.com`).
   - **API Key**: A valid API key with the necessary permissions.
   - **Pure Username**: The username used to log notes in the system.
3. **User Confirmation**: After entering the details, the script will display the number of projects it’s about to modify and prompt for confirmation. Type `yes` to proceed or `no` to cancel.

### Example Workflow

1. Place your Excel file in the script’s directory (e.g., `project_list.xlsx`).
2. Run the script and follow the prompts.
3. If confirmed, the script will:
   - Fetch data for each UUID.
   - Calculate the end date if not present.
   - Add a note indicating the end date is estimated.
4. All updates and actions are logged to `project_update.log` in the same directory.

## Log Output

The script generates a log file, `project_update.log`, in the same folder. This log contains:
- The start and end of the script execution.
- Each UUID's start and end dates (if modified).
- Skipped projects that already have an end date.
- Any errors or issues encountered during execution.

## Example Log Entry

```plaintext
2024-11-06 12:00:00 - INFO - Successfully fetched data for UUID: 12345
2024-11-06 12:00:01 - INFO - Successfully updated end date for UUID: 12345 - Start Date: 2020-01-01, End Date: 2023-01-01
2024-11-06 12:00:02 - INFO - Successfully added note for UUID: 12345
...
```

## Notes

- Ensure that your API key has sufficient permissions to perform GET and PUT requests on the specified endpoints.
- Double-check your Excel file for a `UUID` column with valid project UUIDs before running the script.
