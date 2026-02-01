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

    # Diagnostic prints (without revealing values)
    print("--- Environment Check ---")
    print(f"JIRA_DOMAIN set: {'Yes' if jira_domain else 'No'}")
    print(f"JIRA_EMAIL set: {'Yes' if user_email else 'No'}")
    print(f"JIRA_API_TOKEN set: {'Yes' if api_token else 'No'}")
    
    if jira_domain:
        print(f"JIRA_DOMAIN format check: Starts with https? {'Yes (Check this!)' if jira_domain.startswith('http') else 'No (Good)'}")
        print(f"JIRA_DOMAIN format check: Ends with slash? {'Yes (Check this!)' if jira_domain.endswith('/') else 'No (Good)'}")

    # Jira API endpoint for attachments
    url = f"https://{jira_domain}/rest/api/3/issue/{issue_key}/attachments"
    print(f"Target URL: {url}")
    print("------------------------")

    if not all([jira_domain, user_email, api_token]):
        missing = [name for name, val in [
            ("JIRA_DOMAIN", jira_domain),
            ("JIRA_EMAIL", user_email),
            ("JIRA_API_TOKEN", api_token)
        ] if not val]
        print(f"Error: Missing Jira configuration for: {', '.join(missing)}")
        return False

    headers = {
        "Accept": "application/json",
        "X-Atlassian-Token": "no-check" # Required by Jira for attachment uploads
    }

    auth = HTTPBasicAuth(user_email, api_token)

    # 1. Connectivity/Auth Check
    print("--- Connectivity Check ---")
    myself_url = f"https://{jira_domain}/rest/api/3/myself"
    try:
        myself_resp = requests.get(myself_url, auth=auth)
        if myself_resp.status_code == 200:
            user_data = myself_resp.json()
            print(f"Auth Success! Logged in as: {user_data.get('displayName')} ({user_data.get('emailAddress')})")
        else:
            print(f"Auth Failed! Status: {myself_resp.status_code}")
            print(f"Response: {myself_resp.text}")
            return False
    except Exception as e:
        print(f"Connectivity error: {e}")
        return False
    print("--------------------------")

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
    JIRA_ISSUE = os.getenv("JIRA_ISSUE")
    
    if not JIRA_ISSUE:
        print("Error: JIRA_ISSUE environment variable is not set.")
        # Optional: You could still fall back to a default here if you want safety
        # JIRA_ISSUE = "SCRUM-1" 
        # exit(1) # Or return
    
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
