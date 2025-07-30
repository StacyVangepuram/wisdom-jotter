## Project Report: Wisdom Jotter

### 1.1 Team Information

* Team Name: Team 2-2 of Matrusri Engineering College
* Team Members:
    * Stacy Vangepuram
    * Nerella Sushanth
    * Bonakurthi Dhikshith
    * Safaa Mairaj
    * M.K. Varnitha 
* Internship Program: Viswam.ai Open-Source AI Internship Program
* Project Title: Wisdom Jotter

### 1.2 Application Overview

* The "Wisdom Jotter" is an open-source, AI-powered Streamlit application designed to collaboratively collect, preserve, and showcase valuable cultural and experiential knowledge from across India.
* This application serves as a "Corpus Collection Engine" for Viswam.ai's mission to develop AI that deeply understands India's linguistic and cultural diversity.
* The MVP developed in a few days sprint allows users to easily contribute either traditional proverbs or life lessons they learned from their grandparents or parents in their native languages.
* All contributions are stored distinctly, publicly browsable, and are checked for semantic similarity using an open-source AI model to minimize redundant data, thereby ensuring the collection of high-quality, diverse linguistic and cultural data.
* The application is built with a strong emphasis on accessibility, particularly for users in low-internet bandwidth regions, supporting multilingual input and requiring minimal data transfer.

### 1.3 AI Integration Details

The application integrates Artificial Intelligence primarily for semantic duplicate detection during the data contribution process. This ensures the collected corpus is unique, high-quality, and valuable for training future AI models.

* AI Task: Semantic Similarity/Near-Duplicate Detection.
* Open-Source AI Model Used:
    * `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
    * Description: This is a pre-trained Transformer-based model from the Sentence Transformers library. It converts input text (proverbs or life lessons) into dense numerical vectors (embeddings) that capture their semantic meaning.
    * Reason for Selection: Chosen for its open-source license (Apache 2.0), its multilingual capabilities (crucial for supporting diverse Indian languages), its relatively small size for efficient deployment, and its effectiveness in identifying semantically similar phrases even if the wording differs.

* Integration Method:
    * The model is loaded once at the application startup using Streamlit's `@st.cache_resource` decorator to optimize performance.
    * Upon a user submitting a new proverb or life lesson, the application generates an embedding for the new text.
    * It then calculates the cosine similarity between this new embedding and the embeddings of all existing entries within the same category (proverbs are compared with proverbs, life lessons with life lessons).
    * A pre-defined similarity threshold (0.85 for proverbs, 0.80 for life lessons) is used to flag potential duplicates, informing the user and preventing redundant submissions.

* Contribution to Viswam.ai's Mission: By ensuring the uniqueness and quality of the collected proverbs and life lessons, this AI integration directly contributes to building a cleaner, more diverse, and more effective dataset for training advanced AI models that can better understand and generate content related to India's unique linguistic and cultural nuances.

### 1.4. Technical Architecture & Development

* Frontend & Application Framework: Streamlit
    * Justification: Chosen for its rapid prototyping capabilities, ease of development for Python-centric applications, and inherent responsiveness, which aids mobile and low-bandwidth accessibility.

* Backend & Data Storage: Python with Google Sheets for cloud-based persistence.
    * Implementation: `gspread` library is used to interact with Google Sheets. Data is read from and written to dedicated Google Sheets (`WisdomJotter_Proverbs` and `WisdomJotter_LifeLessons`). Authentication is handled securely using a Google Cloud Service Account key, which is loaded via Streamlit's `st.secrets` for secure deployment on platforms like Hugging Face Spaces.
    * Justification: Google Sheets provide a simple, accessible, and easily shareable cloud-based database solution for the MVP. This eliminates the need for a separate database server setup, offers persistent storage on deployment platforms (solving the ephemeral storage limitation of free tiers), and allows for easy data viewing and management.

* Core Libraries:
    * `streamlit`: For building the interactive web UI.
    * `gspread`: Crucial for connecting to and interacting with Google Sheets.
    * `json`, `os`, `datetime`, `uuid`: Standard Python libraries for unique ID generation, timestamps, and handling service account JSON.
    * `pandas`: Used for converting the collected data into a tabular format (DataFrame) for easy CSV export.
    * `torch`: The underlying deep learning framework required by `sentence-transformers`.
    * `sentence_transformers`: The library for loading and using the Sentence Transformer AI model.

* Development Practices:
    * Version Control: Git
    * Code Structure: Single `app.py` file with modular functions for data loading/saving and model management.
    * Dependency Management: `requirements.txt` for clear and reproducible environment setup.

* Offline-First Considerations:
    * Minimal Data Transfer: The application primarily deals with text data, ensuring very small payloads over the network, which is crucial for low-bandwidth environments.
    * UI Responsiveness: Streamlit's inherent responsiveness makes the application usable and navigable on mobile devices with varying screen sizes and internet speeds.
    * Client-Side Operation (limited): While the core AI processing and data storage happen server-side (on Hugging Face Spaces), the UI itself loads quickly, and user input is client-side.
    * Future Enhancements for Offline-First: While a full offline-first PWA (Progressive Web App) is beyond Streamlit's direct capabilities without significant custom component development, future versions could explore browser-side caching of already-browsed proverbs/lessons (if not on Hugging Face Spaces). For this MVP, the focus is on efficient, low-bandwidth operation.

### 1.5. User Testing & Feedback (Methodology for testing in Week 2)

A. Methodology (Planned for Week 2):
* Recruitment:
    * Leverage personal networks: Friends, family, and colleagues who use smartphones and are comfortable with web browsers.
    * Reach out to cultural groups or language enthusiasts within local communities (e.g., Hyderabad, via social media or community forums) if possible.
    * Target individuals in areas known for varying internet connectivity (e.g., semi-urban or rural contacts).

* Tasks Given to Testers:
    * Task 1 (Submission): "Share at least two proverbs and two life lessons you know. Try to use your native language/dialect."
    * Task 2 (Browse): "Browse through the submitted wisdom. How easy is it to read and navigate?"
    * Task 3 (Duplicate Test): "Try submitting a proverb or life lesson that is very similar to one already existing (or one you just submitted). Observe the app's response."
    * Task 4 (Connectivity Test): "If possible, try using the app on a slower internet connection (e.g., 2G/3G mobile data, or intentionally throttling your connection). Note any performance issues."

* Feedback Collection:
    * Google Form: A simple online form with structured questions covering ease of use, UI/UX, clarity of instructions, performance on different connections, and any bugs encountered.
    * Direct Interviews/Conversations: For a smaller pool of testers, direct conversations to gather qualitative feedback and observe usage patterns.
    * Screenshots/Screen Recordings: Requesting testers to provide screenshots or short screen recordings of issues.

B. Insights & Iterations (To be filled after Week 2):
* Date of Feedback Collection:
* Number of Testers:
* Key Feedback Received:

### 1.6. Project Lifecycle & Roadmap

A. Week 1: Rapid Development Sprint (Week: )
* Plan:
    * Day 1-2: Core Setup & Basic Functionality: Streamlit app scaffolding, Google Sheets integration setup (API enablement, service account creation, JSON key download), basic input form for one type (e.g., proverb), saving to Google Sheet, and displaying entries.
    * Day 3-4: AI Integration (Semantic Duplicate Detection): Integrate sentence-transformers model, implement embedding generation, cosine similarity calculation, and duplicate warning logic.
    * Day 5: Feature Expansion (Life Lessons & Separate Storage): Implement radio button for contribution type, conditional input fields, separate Google Sheet storage for life lessons, and distinct display sections.
    * Day 6: Download & Polish: Implement CSV download for both proverbs and life lessons. Refine UI/UX, add helpful hints, error messages, and basic styling (e.g., via `config.toml`).
    * Day 7: Initial Deployment & Documentation: Deploy MVP to Hugging Face Spaces (ensuring secure secret management for Google Service Account credentials), create `requirements.txt`, `README.md`, `LICENSE`, `CONTRIBUTING.md`, and start drafting `REPORT.md`.

* Execution (Self-Assessment): [To be filled out after Week 1 completion]

* Key Deliverables (End of Week 1):
    * A functional Streamlit application (Wisdom Jotter).
    * Deployed to Hugging Face Spaces (URL: ).
    * Core features: Submit proverbs/life lessons, store in separate Google Sheets, browse all entries, semantic duplicate detection (using `paraphrase-multilingual-MiniLM-L12-v2`).
    * Offline-first considerations: Text-only data, responsive UI, minimal data transfer.
    * Initial `README.md`, `requirements.txt`, `LICENSE`.

B. Week 2: Beta Testing & Iteration Cycle (Week: )
* Methodology:
* Insights & Iterations:

C. Weeks 3-4: User Acquisition & Corpus Growth Campaign (Week: )
* Target Audience & Channels:
    * Primary Target: Indian citizens interested in preserving cultural heritage, students, and individuals with strong family ties to traditional wisdom.
    * Channels:
        * WhatsApp Groups: Family groups, Friend groups. Justification: Active engagement within Indian communities, enabling direct sharing.
        * University/College Student Groups: Especially those in Arts, Humanities, or Linguistics departments. Justification: Tech-savvy individuals who can easily access and use the app, and often have projects related to cultural documentation.

* Growth Strategy & Messaging:
    * Key Message: "Contribute to India's AI future by preserving your unique family wisdom and local heritage!"
    * Promotional Materials:
        * Short Explainer Video: (1-2 minutes) Demonstrating app usage, highlighting the cultural preservation aspect and the AI contribution. (Example: "See how your family's sayings can help build AI that truly understands India!")
        * WhatsApp Text Snippets: Short, engaging messages with the app link, emphasizing cultural pride and community contribution.

* Execution & Results (To be filled after Weeks 3-4):
    * Week 3 Actions:
    * Week 4 Actions:

* Metrics (To be filled after Weeks 3-4):
    * Unique Users Acquired: [Number, e.g., "50 unique users identified via unique contributor names"]
    * Individual Data Contributions (Corpus Units):
        * Total Proverbs Collected:
        * Total Life Lessons Collected:
    * User Feedback from Real-World Usage:

D. Post-Internship Vision & Sustainability Plan

* Major Future Features:
    * Advanced AI Features: Implement AI-powered translation for submitted content (e.g., translate a Telugu proverb to English), categorization of proverbs/lessons (e.g., "wisdom", "humor," "advice"), or AI-driven generation of similar proverbs/lessons for creative inspiration.
    * User Accounts & Profiles: Allow users to create profiles, track their contributions, and potentially follow other contributors.
    * Search & Filter: Implement robust search functionality (by keyword, language, region, contributor) for the collected corpus.
    * Upvoting/Commenting: Introduce social features like upvoting popular contributions or allowing comments to foster community engagement.
    * Image Association: Allow users to upload an image context (e.g., a photo of a village, a specific cultural event) associated with a proverb or life lesson.

* Community Building:
    * Moderation System: Implement a simple moderation system (e.g., flagging inappropriate content) to maintain data quality.
    * Featured Contributions: Highlight unique or highly-rated proverbs/lessons.
    * Community Challenges: Run themed submission challenges (e.g., "Share a proverb about agriculture").
    * Partnerships: Formalize partnerships with cultural institutions, universities, and schools to integrate the app into educational or cultural preservation programs.

* Scaling Data Collection:
    * Database Migration: Migrate from Google Sheets to a more robust and scalable database solution (e.g., PostgreSQL, MongoDB) to handle very large volumes of data, more complex queries, and concurrent users.
    * API for Data Contribution: Develop a simple API endpoint for more automated or programmatic data contributions from other platforms or tools.
    * Gamification: Introduce points, badges, or leaderboards to incentivize more contributions.

* Sustainability:
    * Open-Source Project: Maintain the project as a fully open-source initiative on `code.swecha.org`, encouraging community contributions to the codebase.
    * Documentation: Maintain comprehensive documentation for both users and developers.
    * Funding/Grants: Seek grants or funding opportunities for cultural preservation or AI for social good initiatives.
    * Collaboration with Viswam.ai: Continue close collaboration with Viswam.ai, ensuring the collected corpus remains valuable and integrated into their broader AI research and development efforts.