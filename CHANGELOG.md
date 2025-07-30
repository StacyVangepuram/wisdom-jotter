# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-07-29

### Added

* **Initial MVP Release:** Core Streamlit application for collecting proverbs and life lessons.
* **Google Sheets Integration:** Implemented persistent data storage using Google Sheets (`WisdomJotter_Proverbs` and `WisdomJotter_LifeLessons`) via the `gspread` library.
* **AI-Powered Semantic Duplicate Detection:** Integrated `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` model to identify and flag semantically similar contributions.
* **Hugging Face Spaces Deployment:** Project configured for deployment on Hugging Face Spaces, leveraging `st.secrets` for secure credential management.
* **User Contribution Form:** Intuitive form to submit proverbs and life lessons with language and region hints.
* **Public Browse Section:** Allows users to view all submitted proverbs and life lessons within the application.
* **CSV Data Export:** Functionality to download the collected corpus as CSV files for analysis.
* **Initial Documentation:** `README.md`, `requirements.txt`, and `LICENSE` files.
* **Comprehensive `.gitignore`:** Configured to exclude sensitive credentials (`secrets.toml`) and other unnecessary files from version control.

### Changed

* **Data Persistence Mechanism:** Switched from local JSON files (`data/proverbs.json`, `data/life_lessons.json`) to Google Sheets for reliable, cloud-based data storage.

### Fixed

* **`StreamlitAPIException`:** Resolved issue where `st.set_page_config()` was not the first Streamlit command, ensuring proper app initialization.
* **Secrets File Parsing:** Corrected `.streamlit/secrets.toml` format to adhere to TOML specifications for robust credential loading.

### Removed

* **Local JSON Data Files:** `data/proverbs.json` and `data/life_lessons.json` are no longer used for persistence and have been removed from the repository.