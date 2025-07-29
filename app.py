import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime
import uuid
import torch
from sentence_transformers import SentenceTransformer, util

# --- NEW: Import gspread and its exceptions ---
import gspread
from gspread.exceptions import WorksheetNotFound, SpreadsheetNotFound

# --- Streamlit App Setup - MUST BE THE FIRST STREAMLIT COMMAND ---
st.set_page_config(
    page_title="Local Wisdom & Life Lessons",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Google Sheets Connection ---
# @st.cache_resource caches the returned object (the gspread client) for 1 hour (ttl=3600)
# This prevents re-authenticating with Google Sheets on every rerun of the script.
@st.cache_resource(ttl=3600)
def get_google_sheets_client():
    try:
        # st.secrets automatically loads secrets from .streamlit/secrets.toml locally
        # and from Hugging Face Space secrets when deployed.
        # It tries to get 'gcp_service_account' as a dictionary, or 'GCP_SERVICE_ACCOUNT' as a top-level string.
        credentials_dict = st.secrets.get("gcp_service_account", None)
        if credentials_dict is None:
            # If not found as a TOML table, try as a single string secret (common for Hugging Face UI)
            raw_credentials_str = st.secrets.get("GCP_SERVICE_ACCOUNT", None)
            if raw_credentials_str:
                credentials_dict = json.loads(raw_credentials_str) # Parse the JSON string
        
        if credentials_dict is None:
            st.error("❌ Google Sheets credentials not found in Streamlit secrets.")
            return None

        gc = gspread.service_account_from_dict(credentials_dict)
        return gc
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}. Please check your Streamlit secrets setup and JSON key format.")
        return None

# Attempt to get the Google Sheets client. If it fails, stop the app.
gc = get_google_sheets_client()
if gc is None:
    st.stop() # Stop the app if sheets connection fails

# Retrieve sheet names from secrets
PROVERBS_SHEET_NAME = st.secrets.PROVERBS_SHEET_NAME
LIFE_LESSONS_SHEET_NAME = st.secrets.LIFE_LESSONS_SHEET_NAME

# --- AI Model Loading (Cached for Performance) ---
# @st.cache_resource caches the loaded AI model for efficiency.
@st.cache_resource
def load_sentence_transformer_model():
    model_name = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
    try:
        model = SentenceTransformer(model_name)
        return model
    except Exception as e:
        print(f"Failed to load AI model: {e}")
        return None

with st.spinner("Loading AI model for semantic duplicate detection (first run may take a moment)..."):
    model = load_sentence_transformer_model()

if model is None:
    st.error("❌ AI model failed to load. Semantic duplicate detection will be unavailable. Please check logs for details.")
else:
    st.success("✅ AI model loaded successfully!")

# --- Data Management Functions (UPDATED FOR GOOGLE SHEETS) ---

# Function to load data from a specified Google Sheet
def load_data_from_sheet(sheet_name):
    try:
        sh = gc.open(sheet_name) # Open the spreadsheet by name
        worksheet = sh.worksheet("Sheet1") # Get the first worksheet (default name)
        records = worksheet.get_all_records() # Get all rows as a list of dictionaries
        return records
    except SpreadsheetNotFound:
        st.warning(f"Google Sheet '{sheet_name}' not found. Please ensure it exists and is shared correctly with the service account.")
        return []
    except WorksheetNotFound:
        st.warning(f"Worksheet 'Sheet1' not found in '{sheet_name}'. Please ensure your sheet has a 'Sheet1'.")
        return []
    except Exception as e:
        st.error(f"Error loading data from Google Sheet '{sheet_name}': {e}. Check sheet headers and data format.")
        return []

# Function to save data to a specified Google Sheet
# This function clears the sheet and rewrites all data.
# For very large datasets, consider incremental updates.
def save_data_to_sheet(data, sheet_name):
    try:
        sh = gc.open(sheet_name)
        worksheet = sh.worksheet("Sheet1")
        
        # Clear existing data but preserve the first row (headers)
        # This is a common way to avoid deleting headers if they were manually put there.
        # If your headers are part of `data[0].keys()`, clearing completely and then re-appending is fine too.
        worksheet.clear() # Clears all cells
        
        # Write headers and then all data rows
        if data:
            headers = list(data[0].keys()) # Assumes all dicts in data have same keys
            worksheet.append_row(headers) # Add header row
            rows_to_append = [list(item.values()) for item in data] # Convert list of dicts to list of lists
            worksheet.append_rows(rows_to_append) # Append all data rows
        else:
            # If data is empty, just write headers
            default_headers = ['id', 'timestamp', 'language', 'region_hint', 'contributor', 'text', 'type']
            worksheet.append_row(default_headers)

        st.success(f"Data saved to Google Sheet '{sheet_name}' successfully!")
    except Exception as e:
        st.error(f"Error saving data to Google Sheet '{sheet_name}': {e}. Your contribution might not be saved persistently.")


# --- Streamlit App Content ---
st.title("📜 Local Wisdom & Life Lessons")
st.markdown(
    """
    **Preserve your heritage!** Share local proverbs, idioms, and valuable life lessons passed down through generations.
    This data will help build AI that understands India's rich linguistic and cultural diversity.
    """
)
st.markdown("---")

# --- Submit New Contribution Section ---
st.header("Share Your Wisdom")

contribution_type = st.radio(
    "What would you like to share today?",
    ("Proverb", "Life Lesson"),
    index=0
)

with st.form("wisdom_submission_form", clear_on_submit=True):
    if contribution_type == "Proverb":
        text_content_label = "Enter the proverb or saying here:"
        text_content_placeholder = "Example: కష్టే ఫలి (Kashte Phali) - Hard work pays off."
        text_content_help = "A short, traditional saying that expresses a general truth or piece of advice."
        target_sheet_name = PROVERBS_SHEET_NAME
        duplicate_threshold = 0.85
    else: # Life Lesson
        text_content_label = "Share your life lesson here:"
        text_content_placeholder = "Example: Always listen to your elders, for their experiences are a treasure map."
        text_content_help = "A piece of advice or insight gained from personal experience, often longer than a proverb."
        target_sheet_name = LIFE_LESSONS_SHEET_NAME
        duplicate_threshold = 0.80

    text_content = st.text_area(text_content_label, height=150,
                                placeholder=text_content_placeholder, help=text_content_help)

    language_options = ["Telugu", "Hindi", "Tamil", "Kannada", "Malayalam", "Bengali", "Marathi", "Gujarati", "Odia", "Punjabi", "English", "Other (Please Specify)"]
    language = st.selectbox("Language:", options=language_options)

    if language == "Other (Please Specify)":
        custom_lang_input = st.text_input("Please specify the language (e.g., 'Konkani', 'Bhojpuri'):")
        language = custom_lang_input.strip() if custom_lang_input.strip() else "Unknown"

    region_hint = st.text_input("Optional: Any specific region/district this is common in?",
                                placeholder="Example: Andhra Pradesh, Telangana, Rural Punjab")
    contributor_name = st.text_input("Optional: Your Name (for credit!):", placeholder="Anonymous")

    submitted = st.form_submit_button("Submit " + contribution_type)

    if submitted:
        if text_content.strip():
            current_data = load_data_from_sheet(target_sheet_name)
            processed_new_text = text_content.strip()

            is_duplicate = False

            if model is not None and current_data:
                # Filter out entries where 'text' key might be missing or empty for robustness
                existing_texts_for_similarity = [item['text'] for item in current_data if 'text' in item and item['text']]
                
                if existing_texts_for_similarity: # Only run similarity if there are texts to compare against
                    with st.spinner(f"Checking for similar {contribution_type.lower()}s using AI..."):
                        try:
                            existing_embeddings = model.encode(existing_texts_for_similarity, convert_to_tensor=True)
                            new_embedding = model.encode([processed_new_text], convert_to_tensor=True)

                            cosine_scores = util.cos_sim(new_embedding, existing_embeddings)[0]

                            for i, score in enumerate(cosine_scores):
                                if score >= duplicate_threshold:
                                    st.warning(
                                        f"⚠️ Potential duplicate found! Your {contribution_type.lower()} is very similar to: "
                                        f"**'{existing_texts_for_similarity[i]}'** (Similarity: {score:.2f}). "
                                        "Please consider if yours is truly unique or a slight variation."
                                    )
                                    is_duplicate = True
                                    break
                        except Exception as e:
                            st.error(f"🚨 Error during AI similarity check: {e}. Submitting without full duplicate check for now.")
                else:
                    st.info(f"ℹ️ No existing {contribution_type.lower()}s to compare against for duplicate detection.")
            elif model is None:
                st.info(f"ℹ️ AI model not loaded. Semantic duplicate detection skipped for {contribution_type.lower()}s.")
            else: # current_data is empty
                st.info(f"ℹ️ No existing {contribution_type.lower()}s in the corpus yet. Your contribution will be the first!")


            if not is_duplicate:
                new_entry = {
                    "id": str(uuid.uuid4()),
                    "type": contribution_type,
                    "text": processed_new_text,
                    "language": language,
                    "region_hint": region_hint.strip(),
                    "contributor": contributor_name.strip() if contributor_name.strip() else "Anonymous",
                    "timestamp": datetime.now().isoformat()
                }
                
                # Append the new entry to the data loaded from the sheet
                current_data.append(new_entry)
                # Save the updated list back to the sheet
                save_data_to_sheet(current_data, target_sheet_name)
                st.success(f"✅ Thank you for your contribution! Your {contribution_type.lower()} has been added.")
        else:
            st.warning("⚠️ Please enter the text before submitting.")

st.markdown("---")

# --- Browse All Contributions Section ---
st.header("Browse Shared Wisdom")

# --- Proverbs Section ---
st.subheader("📚 Shared Proverbs")
proverbs_to_display = load_data_from_sheet(PROVERBS_SHEET_NAME)

if not proverbs_to_display:
    st.info("ℹ️ No proverbs submitted yet. Share some local wisdom!")
else:
    # Sort by timestamp (assuming it's in ISO format and thus lexicographically sortable)
    # Ensure 'timestamp' key exists before sorting
    proverbs_to_display.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    for proverb in proverbs_to_display:
        st.markdown(f"**Proverb:** {proverb.get('text', 'N/A')}")
        st.markdown(f"**Language:** {proverb.get('language', 'N/A')}")
        if proverb.get('region_hint'):
            st.markdown(f"**Region:** {proverb.get('region_hint', 'N/A')}")
        contributor_info = proverb.get('contributor', 'Anonymous')
        timestamp_str = proverb.get('timestamp')
        display_timestamp = ""
        if timestamp_str:
            try:
                # Only attempt conversion if it's a valid ISO format
                if isinstance(timestamp_str, str) and len(timestamp_str) >= 19: # Basic check for ISO format length
                    display_timestamp = f" on {datetime.fromisoformat(timestamp_str).strftime('%Y-%m-%d %H:%M')}"
                else:
                    display_timestamp = f" (Timestamp: {timestamp_str})" # Fallback if format is wrong/not string
            except ValueError:
                display_timestamp = f" (Timestamp: {timestamp_str})" # Fallback if parsing fails
        st.markdown(f"**Contributed By:** {contributor_info}{display_timestamp}")
        st.markdown("---")

# --- Life Lessons Section ---
st.subheader("💡 Shared Life Lessons")
life_lessons_to_display = load_data_from_sheet(LIFE_LESSONS_SHEET_NAME)

if not life_lessons_to_display:
    st.info("ℹ️ No life lessons submitted yet. Share a valuable insight!")
else:
    life_lessons_to_display.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    for lesson in life_lessons_to_display:
        st.markdown(f"**Life Lesson:** {lesson.get('text', 'N/A')}")
        st.markdown(f"**Language:** {lesson.get('language', 'N/A')}")
        if lesson.get('region_hint'):
            st.markdown(f"**Region:** {lesson.get('region_hint', 'N/A')}")
        contributor_info = lesson.get('contributor', 'Anonymous')
        timestamp_str = lesson.get('timestamp')
        display_timestamp = ""
        if timestamp_str:
            try:
                if isinstance(timestamp_str, str) and len(timestamp_str) >= 19:
                    display_timestamp = f" on {datetime.fromisoformat(timestamp_str).strftime('%Y-%m-%d %H:%M')}"
                else:
                    display_timestamp = f" (Timestamp: {timestamp_str})"
            except ValueError:
                display_timestamp = f" (Timestamp: {timestamp_str})"
        st.markdown(f"**Contributed By:** {contributor_info}{display_timestamp}")
        st.markdown("---")

st.markdown("---")

# --- Admin/Corpus Download Section ---
st.header("Download Collected Corpus (For Research & Analysis)")
st.write("This section allows researchers and administrators to download all collected data for corpus analysis.")

col1, col2 = st.columns(2)

with col1:
    if st.button("Download Proverbs as CSV"):
        data_to_download = load_data_from_sheet(PROVERBS_SHEET_NAME)
        if data_to_download:
            df = pd.DataFrame(data_to_download)
            if 'id' in df.columns:
                df['id'] = df['id'].astype(str)
            # Define all expected columns to ensure they are present in the CSV
            required_columns = ['id', 'timestamp', 'language', 'region_hint', 'contributor', 'text', 'type']
            # Add any missing columns with default None/empty string to avoid DataFrame errors
            for col in required_columns:
                if col not in df.columns:
                    df[col] = None
            df = df[required_columns] # Ensure correct order and inclusion of all relevant columns
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Click to Download Proverbs CSV",
                data=csv_data,
                file_name="local_wisdom_proverbs_corpus.csv",
                mime="text/csv",
                key="download_proverbs_csv"
            )
        else:
            st.info("ℹ️ No proverbs to download yet.")

with col2:
    if st.button("Download Life Lessons as CSV"):
        data_to_download = load_data_from_sheet(LIFE_LESSONS_SHEET_NAME)
        if data_to_download:
            df = pd.DataFrame(data_to_download)
            if 'id' in df.columns:
                df['id'] = df['id'].astype(str)
            required_columns = ['id', 'timestamp', 'language', 'region_hint', 'contributor', 'text', 'type']
            for col in required_columns:
                if col not in df.columns:
                    df[col] = None
            df = df[required_columns]
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Click to Download Life Lessons CSV",
                data=csv_data,
                file_name="local_wisdom_life_lessons_corpus.csv",
                mime="text/csv",
                key="download_life_lessons_csv"
            )
        else:
            st.info("ℹ️ No life lessons to download yet.")

st.markdown("---")
st.info("Built with ❤️ for Viswam.ai's mission to understand India's linguistic diversity.")