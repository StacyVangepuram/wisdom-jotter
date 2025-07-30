# Contributing to Wisdom Jotter

We welcome and appreciate contributions to the Wisdom Jotter project! Whether you're reporting a bug, suggesting a new feature, or submitting code changes, your help makes this project better.

Please take a moment to review this document to understand how to contribute effectively.

## Code of Conduct

Please note that this project is released with a [LICENSE](LICENSE) file. By participating in this project, you are expected to uphold this code.

## How Can I Contribute?

### 1. Reporting Bugs

If you find a bug in the application, please help us by reporting it.

* **Before reporting:** Check the existing [Issues](https://code.swecha.org/Stacy_Vangepuram/wisdom-jotter-app/-/issues) on our GitLab repository to see if the bug has already been reported.
* **How to report:**
    * Open a new issue on our [GitLab Issues page](https://code.swecha.org/Stacy_Vangepuram/wisdom-jotter-app/-/issues).
    * Provide a clear and concise title for the issue.
    * **Describe the bug in detail:**
        * Steps to reproduce the behavior (e.g., "Go to 'Submit Wisdom', enter X, click Y").
        * Expected behavior.
        * Actual behavior.
        * Screenshots or recordings (if applicable) are highly encouraged.
        * Your operating system, browser, and any relevant app versions.

### 2. Suggesting Enhancements & New Features

We'd love to hear your ideas for improving Wisdom Jotter!

* **Before suggesting:** Check existing [Issues](https://code.swecha.org/Stacy_Vangepuram/wisdom-jotter-app/-/issues) to see if your idea has already been discussed.
* **How to suggest:**
    * Open a new issue on our [GitLab Issues page](https://code.swecha.org/Stacy_Vangepuram/wisdom-jotter-app/-/issues).
    * Provide a clear and descriptive title (e.g., "Feature Request: Add user accounts").
    * **Describe the enhancement/feature:** Explain why it would be useful, potential use cases, and how it might work.

### 3. Contributing Code

If you'd like to contribute code, please follow these steps:

#### 3.1. Local Development Setup

Refer to the [README.md](README.md) file for instructions on how to set up the project locally. This includes:
* Cloning the repository.
* Setting up a virtual environment.
* Installing dependencies (`requirements.txt`).
* Configuring Google Cloud credentials for local development (`.streamlit/secrets.toml`).
* Running the Streamlit application.

#### 3.2. Making Changes

1.  **Fork the repository** (if you don't have direct write access) or **clone the repository** if you're a team member.
    ```bash
    git clone [https://code.swecha.org/Stacy_Vangepuram/wisdom-jotter-app.git](https://code.swecha.org/Stacy_Vangepuram/wisdom-jotter-app.git)
    cd wisdom-jotter-app
    ```
2.  **Create a new branch** for your changes. Use a descriptive name (e.g., `feature/add-search`, `fix/bug-duplicate-check`).
    ```bash
    git checkout -b feature/your-awesome-feature
    ```
3.  **Implement your changes.** Write clean, well-commented code.
4.  **Test your changes thoroughly** to ensure they work as expected and don't introduce new bugs.
5.  **Update `CHANGELOG.md`:** Add an entry for your changes under an "Unreleased" or new version header, following the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.
6.  **Ensure your `.gitignore` is up-to-date:** Specifically, `secrets.toml` and virtual environments should always be ignored.
7.  **Commit your changes** with a clear and concise commit message.
    ```bash
    git add .
    git commit -m "feat: Add new awesome feature" # Use conventional commits if applicable
    ```
    (e.g., `fix:`, `feat:`, `docs:`, `chore:`, `refactor:`)

#### 3.3. Submitting Your Changes (Merge Request)

1.  **Push your new branch to your GitLab fork/repository:**
    ```bash
    git push origin feature/your-awesome-feature
    ```
2.  **Open a Merge Request (MR) on GitLab.**
    * Go to your project on [code.swecha.org](https://code.swecha.org/Stacy_Vangepuram/wisdom-jotter-app).
    * You should see a prompt to create a new Merge Request from your pushed branch.
    * **Provide a clear title and description for your MR.** Explain what your changes do, why they are needed, and any potential impacts.
    * If your MR addresses an existing issue, link it (e.g., "Closes #123").
    * Request a review from a team member.

### 4. Code Style & Standards

* **Python Formatting:** We generally follow [PEP 8](https://www.python.org/dev/peps/pep-0008/). Use tools like `black` or `flake8` to format and lint your code if possible.
* **Commenting:** Add comments where the code logic isn't immediately obvious.
* **Docstrings:** Use docstrings for functions and classes where appropriate.

## Questions?

If you have any questions about contributing, feel free to open an issue or reach out to the team directly.

Thank you for your interest in contributing to Wisdom Jotter!