# Wisdom Jotter: Preserving India's Cultural Wisdom

## 📜 Project Overview

The "Wisdom Jotter" is an open-source, AI-powered Streamlit application designed to collaboratively collect, preserve, and showcase valuable cultural and experiential knowledge from across India. This initiative directly supports Viswam.ai's mission to develop AI that deeply understands India's linguistic and cultural diversity.

**Key Features:**
* **Contribute Local Wisdom:** Easily submit traditional proverbs and life lessons in various Indian languages.
* **AI-Powered Duplicate Detection:** Utilizes a multilingual sentence transformer model (`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`) to check for semantic similarity, ensuring the collection of unique and high-quality data.
* **Cloud-Based Storage:** All contributions are securely stored in Google Sheets for persistent, accessible, and easily manageable data.
* **Publicly Browsable Corpus:** View all submitted proverbs and life lessons directly within the app.
* **CSV Export:** Download the entire collected corpus for research and analysis.
* **Accessibility First:** Designed with a focus on low-internet bandwidth regions, featuring minimal data transfer and a responsive UI.

## 🚀 Live Application

Experience the Wisdom Jotter app live on Hugging Face Spaces:

[**Access the Wisdom Jotter App Here!**](https://huggingface.co/spaces/stacyv/wisdom-jotter)


## ✨ How to Contribute Wisdom

It's simple to share your unique insights:

1.  Visit the [live application link](https://huggingface.co/spaces/stacyv/wisdom-jotter).
2.  Select whether you want to share a "Proverb" or a "Life Lesson".
3.  Enter the wisdom in the provided text area, specifying its language and (optionally) region.
4.  The app will automatically check for similar existing entries using AI to help maintain a unique corpus.
5.  Click "Submit" – your contribution will be instantly saved and added to the collection!

## 🛠️ Technical Architecture

* **Frontend & Application Framework:** [Streamlit](https://streamlit.io/)
    * **Justification:** Enables rapid development of interactive web applications in Python, providing inherent responsiveness crucial for mobile and low-bandwidth accessibility.
* **Backend & Data Storage:** Python with [Google Sheets](https://docs.gspread.org/en/latest/)
    * **Implementation:** Utilizes the `gspread` library for secure interaction with Google Sheets. A Google Cloud Service Account facilitates authentication, with credentials stored securely as secrets on Hugging Face Spaces.
    * **Benefit:** Provides persistent, scalable, and easily manageable cloud storage for all contributions, overcoming the ephemeral storage limitations of free deployment tiers.
* **AI Integration:** Semantic Similarity using [Sentence Transformers](https://www.sbert.net/)
    * **Model:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
    * **Purpose:** Converts text into numerical embeddings, allowing the application to calculate cosine similarity between new and existing entries to detect and flag potential duplicates.

## 📦 Project Structure


WISDOM JOTTER APP/
├── .streamlit/
│   └── config.toml           # Streamlit application configuration (theme, etc.)
├── app.py                    # The main Streamlit application code
├── .gitignore                # Specifies files and folders to be ignored by Git (e.g., secrets.toml)
├── requirements.txt          # Lists all Python dependencies
├── README.md                 # This file
├── LICENSE                   # Project license information
├── CONTRIBUTING.md           # Guidelines for contributors
└── [other project files like CHANGELOG.md, REPORT.md, etc.]

## ⚙️ Local Development Setup

To run this application on your local machine:

1.  **Clone the repository:**
    ```bash
    git clone [https://code.swecha.org/Stacy_Vangepuram/wiadom-jotter-app.git](https://code.swecha.org/Stacy_Vangepuram/wisdom-jotter-app.git)
    cd wisdom-jotter-app
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Google Cloud Credentials:**
    * Follow the "Google Cloud Setup" steps as outlined in the project documentation (or previous instructions provided). This involves:
        * Creating a Google Cloud Project.
        * Enabling the Google Sheets API.
        * Creating a Service Account and generating its JSON key.
    * **Crucially, create a folder named `.streamlit` in your project's root directory.**
    * **Inside `.streamlit`, create a file named `secrets.toml`.**
    * **Copy the entire content of your downloaded Google Service Account JSON key file into `secrets.toml`** under a `[gcp_service_account]` section, converting it to TOML format. It should look like this:
        ```toml
        # .streamlit/secrets.toml
        [gcp_service_account]
        type = "service_account"
        project_id = "your-project-id-from-json"
        private_key_id = "your-private-key-id-from-json"
        private_key = """-----BEGIN PRIVATE KEY-----
        YOUR_ENTIRE_MULTI_LINE_PRIVATE_KEY_HERE
        -----END PRIVATE KEY-----"""
        client_email = "your-service-account-email-from-json"
        client_id = "your-client-id-from-json"
        auth_uri = "[https://accounts.google.com/o/oauth2/auth](https://accounts.google.com/o/oauth2/auth)"
        token_uri = "[https://oauth2.googleapis.com/token](https://oauth2.googleapis.com/token)"
        auth_provider_x509_cert_url = "[https://www.googleapis.com/oauth2/v1/certs](https://www.googleapis.com/oauth2/v1/certs)"
        client_x509_cert_url = "[https://www.googleapis.com/robot/v1/metadata/x509/your-service-account-email-url-encoded](https://www.googleapis.com/robot/v1/metadata/x509/your-service-account-email-url-encoded)"
        universe_domain = "googleapis.com"

        PROVERBS_SHEET_NAME = "WisdomJotter_Proverbs"
        LIFE_LESSONS_SHEET_NAME = "WisdomJotter_LifeLessons"
        ```
    * **Prepare your Google Sheets:** Create two new Google Sheets named `WisdomJotter_Proverbs` and `WisdomJotter_LifeLessons` in your Google Drive.
    * **Share both Google Sheets with your Service Account's email address (from `client_email` in your JSON/TOML) with "Editor" access.**

5.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
    This will open the application in your web browser.

## 🤝 Contributing

We welcome contributions to the Wisdom Jotter project! Whether you're fixing bugs, adding new features, or improving documentation, your help is appreciated.

Please refer to our [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the [LICENSE file name, e.g., Apache License 2.0]. See the [LICENSE](LICENSE) file for details.



---