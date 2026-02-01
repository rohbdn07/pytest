import os
import requests
from requests.auth import HTTPBasicAuth
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def upload_to_jira(file_path, issue_key):
    """
    Uploads a file as an attachment to a Jira issue.
    """
    # Configuration from environment variables
    jira_domain = os.getenv("JIRA_DOMAIN")
    user_email = os.getenv("JIRA_EMAIL")
    api_token = os.getenv("JIRA_API_TOKEN")

    if not all([jira_domain, user_email, api_token]):
        print("Error: Missing Jira configuration in environment variables.")
        print("Please ensure JIRA_DOMAIN, JIRA_EMAIL, and JIRA_API_TOKEN are set.")
        return False

    # Jira API endpoint for attachments
    url = f"https://{jira_domain}/rest/api/3/issue/{issue_key}/attachments"

    headers = {
        "Accept": "application/json",
        "X-Atlassian-Token": "no-check" # Required by Jira for attachment uploads
    }

    auth = HTTPBasicAuth(user_email, api_token)

    print(f"Uploading {file_path} to {issue_key}...")

    try:
        with open(file_path, "rb") as f:
            files = {
                "file": (os.path.basename(file_path), f, "text/html")
            }
            response = requests.post(
                url,
                headers=headers,
                files=files,
                auth=auth
            )

        if response.status_code == 200:
            print(f"Successfully uploaded {file_path} to {issue_key}!")
            return True
        else:
            print(f"Failed to upload. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    # Configuration from environment variables
    # Priority: Env var > hardcoded default
    JIRA_ISSUE = os.getenv("JIRA_ISSUE", "SCRUM-1")
    
    # List of possible locations for the report
    POSSIBLE_REPORTS = [
        "report.html",
        "test_reports/report.html"
    ]
    
    report_file = None
    for path in POSSIBLE_REPORTS:
        if os.path.exists(path):
            report_file = path
            break
    
    if report_file:
        upload_to_jira(report_file, JIRA_ISSUE)
    else:
        print(f"Error: Could not find report file in any of: {POSSIBLE_REPORTS}")
