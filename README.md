# Wisdom Jotter App

![Streamlit App](https://img.shields.io/badge/Streamlit-Cloud-orange?style=flat-square&logo=streamlit)
![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-Apache%202.0-red?style=flat-square)

A Streamlit-powered web application designed to collect, store, and share timeless proverbs and valuable life lessons. This project leverages Google Sheets for robust data persistence and integrates AI for semantic duplicate detection, ensuring the uniqueness and quality of contributions.

## Table of Contents

-   [Features](#features)
-   [Live Application](#live-application)
-   [Local Development Setup](#local-development-setup)
-   [Project Structure](#project-structure)
-   [Data Persistence](#data-persistence)
-   [AI Integration Details](#ai-integration-details)
-   [Deployment (Streamlit Community Cloud)](#deployment-streamlit-community-cloud)
-   [Contributing](#contributing)
-   [License](#license)

## Features

* **Wisdom Submission:** Users can easily submit new proverbs and life lessons via an intuitive form.
* **AI Duplicate Detection:** Utilizes a pre-trained sentence transformer model to identify semantically similar submissions, preventing redundancy.
* **Google Sheets Backend:** All submitted data is securely stored and retrieved from Google Sheets, providing a flexible and scalable database.
* **Browse Wisdom:** A dedicated section to view all collected proverbs and life lessons.
* **Data Export:** Functionality to download the entire corpus as CSV files.
* **User-Friendly Interface:** Built with Streamlit for a clean and interactive web experience.

## Live Application

Access the deployed Wisdom Jotter application here:
**[https://wisdom-jotter-6mk3tcttspcvyk9qiqqwph.streamlit.app/](https://wisdom-jotter-6mk3tcttspcvyk9qiqqwph.streamlit.app/)**

## Local Development Setup

To run this application locally for development or testing:

1.  **Clone the repository:**
    ```bash
    git clone [https://code.swecha.org/Stacy_Vangepuram/wisdom-jotter-app.git](https://code.swecha.org/Stacy_Vangepuram/wisdom-jotter-app.git)
    cd wisdom-jotter-app # Navigate into your project directory
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    * **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set up Google Cloud Credentials:**
    * Follow the instructions in the [Data Persistence](#data-persistence) section to obtain your Google Service Account JSON key.
    * Create a `.streamlit` folder in your project's root directory if it doesn't exist.
    * Inside the `.streamlit` folder, create a file named `secrets.toml`.
    * Add your Google Service Account key and Google Sheet names to `secrets.toml` in the following format:
        ```toml
        # .streamlit/secrets.toml
        GCP_SERVICE_ACCOUNT = '''
        {
          "type": "service_account",
          "project_id": "your-project-id",
          "private_key_id": "your-private_key-id",
          "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
          "client_email": "your-service-account-email@your-project-id.iam.gserviceaccount.com",
          "client_id": "your-client-id",
          "auth_uri": "[https://accounts.google.com/o/oauth2/auth](https://accounts.google.com/o/oauth2/auth)",
          "token_uri": "[https://oauth2.googleapis.com/token](https://oauth2.googleapis.com/token)",
          "auth_provider_x509_cert_url": "[https://www.googleapis.com/oauth2/v1/certs](https://www.googleapis.com/oauth2/v1/certs)",
          "client_x509_cert_url": "[https://www.googleapis.com/robot/v1/metadata/x509/your-service-account-email@your-project-id.iam.gserviceaccount.com](https://www.googleapis.com/robot/v1/metadata/x509/your-service-account-email@your-project-id.iam.gserviceaccount.com)",
          "universe_domain": "googleapis.com"
        }
        '''
        PROVERBS_SHEET_NAME = "WisdomJotter_Proverbs"
        LIFE_LESSONS_SHEET_NAME = "WisdomJotter_LifeLessons"
        ```
    * **Important:** Ensure `.streamlit/secrets.toml` is included in your `.gitignore` file to prevent it from being pushed to your public repository.

6.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
    The app will open in your default web browser.

## Project Structure

WISDOM JOTTER APP/
├── .streamlit/             # Streamlit configuration files
│   └── config.toml         # Streamlit general configurations
│   └── secrets.toml        # Streamlit secrets (ignored by Git)
├── app.py                  # Main Streamlit application script
├── .gitignore              # Specifies intentionally untracked files to ignore
├── CHANGELOG.md            # Documents all notable changes to the project
├── CONTRIBUTING.md         # Guidelines for contributing to the project
├── LICENSE                 # Project's open-source license (Apache License 2.0)
├── README.md               # Project overview and setup instructions
├── REPORT.md               # Project report/documentation (if applicable)
└── requirements.txt        # Python dependencies required for the project

## Data Persistence

The Wisdom Jotter App uses Google Sheets for data storage.

1.  **Create Google Sheets:**
    * Create two new Google Sheets in your Google Drive: `WisdomJotter_Proverbs` and `WisdomJotter_LifeLessons`.
    * Ensure they have appropriate headers for your data (e.g., "ID", "Content", "Language", "Region", "Timestamp", "Duplicates Detected" etc.).

2.  **Set up a Google Service Account:**
    * Go to Google Cloud Console: [https://console.cloud.google.com/](https://console.cloud.google.com/)
    * Create a new project (if you don't have one) or select an existing one.
    * Enable the "Google Sheets API" and "Google Drive API" for your project.
    * Go to **IAM & Admin -> Service Accounts**.
    * Create a new Service Account.
    * Grant it the `Editor` role (or more specific roles like `Google Sheets API Editor`, `Drive API Editor` if available and preferred for security).
    * Create a new JSON key for this service account and download it. This JSON file contains your `GCP_SERVICE_ACCOUNT` credentials.

3.  **Share Google Sheets with Service Account:**
    * Open your `WisdomJotter_Proverbs` and `WisdomJotter_LifeLessons` Google Sheets.
    * Click the "Share" button.
    * Add the **client_email** from your downloaded service account JSON key file (e.g., `your-service-account-email@your-project-id.iam.gserviceaccount.com`) as an editor.

## AI Integration Details

The application incorporates an AI model for semantic duplicate detection of submitted proverbs and life lessons.

* **Model:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
* **Functionality:** When a new wisdom entry is submitted, its semantic similarity is compared against existing entries in the Google Sheet. If a high similarity score is detected, the submission is flagged as a potential duplicate, preventing redundant entries and maintaining data quality.

## Deployment (Streamlit Community Cloud)

This application is deployed on Streamlit Community Cloud for easy public access.

**Deployment Process:**

1.  **Ensure your project is in a GitHub or GitLab repository:** The Streamlit Community Cloud primarily deploys directly from Git repositories.
2.  **Verify `requirements.txt`:** Make sure your `requirements.txt` file lists all necessary Python libraries (e.g., `streamlit`, `gspread`, ``pandas`, `torch`, `sentence-transformers`).
3.  **Secure your secrets:** Your Google Service Account key and sheet names are stored as environment variables (secrets) directly within the Streamlit Cloud app settings, not in your public repository.
    * **How to add secrets on Streamlit Cloud:**
        * Go to your Streamlit Cloud dashboard (`share.streamlit.io`).
        * Click "New app".
        * Select your GitLab repository and branch.
        * Before deploying, under "Advanced settings," you'll find a section for "Secrets."
        * Add your secrets in the format:
            ```
            GCP_SERVICE_ACCOUNT="""{
              "type": "service_account",
              ... (full JSON content) ...
            }"""
            PROVERBS_SHEET_NAME="WisdomJotter_Proverbs"
            LIFE_LESSONS_SHEET_NAME="WisdomJotter_LifeLessons"
            ```
            *Make sure the `GCP_SERVICE_ACCOUNT` JSON is wrapped in triple quotes (`"""..."""`) as shown.*
4.  **Deploy:** Click "Deploy!" Streamlit Cloud will pull your code, install dependencies, and run your app. Any subsequent pushes to your connected GitLab/GitHub branch will automatically trigger a redeployment.

## Contributing

We welcome contributions! Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to report bugs, suggest features, and contribute code.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for full details.
