# Standard library imports
import argparse
import sys
import os
import re
from datetime import datetime, timedelta, timezone

# Third-party imports from requirements.txt
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve environment variables
ITS_PRO_DOMAIN = os.getenv('ITS_PRO_DOMAIN')
ITS_PRO_ACCESS_TOKEN = os.getenv('ITS_PRO_ACCESS_TOKEN')

def parse_time(time_str):
    """Parse the input time and convert it to seconds, assuming hours if ≤ 8 else minutes."""
    match = re.match(r'^(\d+)(m|h)?$', time_str)
    if not match:
        print("Error: Invalid time format. Time should be a number optionally followed by 'm' or 'h'.")
        sys.exit(1)
    amount, unit = match.groups()
    amount = int(amount)
    if unit == 'h' or (unit is None and amount <= 8):
        return amount * 3600  # Convert hours to seconds
    elif unit == 'm' or (unit is None and amount > 8):
        return amount * 60  # Convert minutes to seconds
    else:
        print("Error: Invalid time specifier. Use 'm' for minutes or 'h' for hours.")
        sys.exit(1)

def log_time(issue_id, time_spent):
    """
    Logs the specified time to an ITS PRO issue by making a POST request to the ITS PRO worklog API.

    Converts `time_spent` to seconds based on whether it's in hours or minutes, calculates the start time in UTC
    using timezone-aware datetime objects, and sends the data along with an empty comment to the specified ITS PRO issue.
    Handles different response codes, printing appropriate success or error messages, and exits on failure.

    Args:
    issue_id (str): ITS PRO issue ID to log time to.
    time_spent (str): Time spent in hours or minutes (e.g., '2', '2h', '30', '30m').
                      If no unit is provided, values ≤ 8 are assumed to be hours, and values > 8 are assumed to be minutes.
    """
    # Parse the time and convert it to seconds
    time_seconds = parse_time(time_spent)

    # Calculate the start time using a timezone-aware datetime object in UTC
    start_time = datetime.now(timezone.utc) - timedelta(seconds=time_seconds)

    # Construct the API URL for logging time to the specified ITS PRO issue
    url = f"https://{ITS_PRO_DOMAIN}/rest/api/2/issue/{issue_id}/worklog"

    # Construct the API request payload
    payload = {
        'timeSpentSeconds': time_seconds,
        'started': start_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+0000',  # UTC timezone-aware
        'comment': ''  # Empty comment field added
    }

    # Make the API request
    headers = {
        'Authorization': f'Bearer {ITS_PRO_ACCESS_TOKEN}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # Send the POST request
    print(f"Attempting to log time to {issue_id}.")
    response = requests.post(url, json=payload, headers=headers)
    
    # Handle the response
    if response.status_code == 201:
        print(f"Successfully logged time to {issue_id}.")
    else:
        print(f"Failed to log time: HTTP {response.status_code} - {response.text}")
        if response.status_code == 401:
            print("Check your API token or permissions.")
        elif response.status_code == 404:
            print("Issue ID not found. Please check the issue ID and try again.")
        elif response.status_code == 400:
            print("Bad request. Please check the format of the request.")
        elif response.status_code == 500:
            print("Internal server error. There might be a configuration issue on the server.")
        sys.exit(1)

def main():
    """Main function to parse arguments and call the time logging function."""
    parser = argparse.ArgumentParser(description='Log time to ITS PRO', add_help=False)  # Removed default help option
    parser.add_argument('issue_id', type=str, nargs='?', help='ITS PRO issue ID to which time will be logged')
    parser.add_argument('time_spent', type=str, nargs='?', help='Amount of time spent (e.g., 30, 30m, 2, 2h)')
    
    # Parse the arguments
    args = parser.parse_args()

    # If arguments are missing or bad, print friendly error and usage
    if not args.issue_id or not args.time_spent:
        print("Error: Missing required parameters.")
        print("Usage: lt [ITS PRO Issue ID] [Time Spent] (Make sure the 'lt' alias is set up as described in the README.)")
        print("\nLog time to ITS PRO using the 'lt' command:")
        print("\nParameters:")
        print("  ITS PRO Issue ID    The ITS PRO issue ID to log time to (e.g., SVCOPS-619)")
        print("  Time Spent          Amount of time spent (e.g., 30, 30m, 2, 2h)")
        sys.exit(1)

    # Call the function to log time
    log_time(args.issue_id, args.time_spent)

if __name__ == "__main__":
    main()
