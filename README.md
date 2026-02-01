# pytest Learning Project

This project is designed for learning and practicing `pytest`, a popular testing framework for Python.

## Project Structure

- `src/`: Contains the source code.
- `tests/`: Contains the test modules.
- `scripts/`: Contains utility scripts (e.g., for Jira integration).

## Prerequisites

- Python 3.x
- `pip` (Python package installer)

## Installation

1.  **Clone the repository** (if applicable) or navigate to the project directory.

2.  **Create a virtual environment** (recommended):
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Running Tests

To run all tests:
```sh
pytest
```

To run tests with verbose output:
```sh
pytest -v
```

### Generating Reports

To generate an HTML report (requires `pytest-html`):
```sh
pytest --html=report.html
```

## CI/CD

This project uses GitHub Actions for Continuous Integration. The workflow is defined in `.github/workflows/tests.yml`.

-   **Triggers**: Pushes to `main` and Pull Requests.
-   **Actions**:
    -   Sets up Python 3.13.
    -   Installs dependencies.
    -   Runs tests using `pytest` and generates HTML/XML reports.
    -   Uploads test reports as artifacts (`pytest-reports`).
    -   Uploads report to Jira (requires secrets configuration).

### Configuring GitHub Secrets

To make the Jira integration work in CI/CD, you need to add the following secrets to your GitHub repository:

1.  Go to your GitHub repository.
2.  Navigate to **Settings** > **Secrets and variables** > **Actions**.
3.  Click **New repository secret** and add:
    -   `JIRA_DOMAIN`: Your Atlassian domain (e.g., `your-domain.atlassian.net`).
    -   `JIRA_EMAIL`: Your Atlassian account email.
    -   `JIRA_API_TOKEN`: Your Jira API token.
    -   `JIRA_ISSUE` (Optional): The Jira issue key to attach the report to (defaults to `SCRUM-1`).
