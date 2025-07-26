import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime
import uuid
import torch
from sentence_transformers import SentenceTransformer, util

# --- Streamlit App Setup - MUST BE THE FIRST STREAMLIT COMMAND ---
st.set_page_config(
    page_title="Local Wisdom & Life Lessons",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Configuration ---
DATA_DIR = "data"
PROVERBS_FILE = os.path.join(DATA_DIR, "proverbs.json")
LIFE_LESSONS_FILE = os.path.join(DATA_DIR, "life_lessons.json")

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# --- AI Model Loading (Cached for Performance) ---
@st.cache_resource
def load_sentence_transformer_model():
    """Loads the multilingual Sentence Transformer model."""
    model_name = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
    try:
        model = SentenceTransformer(model_name)
        return model
    except Exception as e:
        print(f"Failed to load AI model: {e}")
        return None

# Load the model globally (once per app instance)
with st.spinner("Loading AI model for semantic duplicate detection (first run may take a moment)..."):
    model = load_sentence_transformer_model()

if model is None:
    st.error("❌ AI model failed to load. Semantic duplicate detection will be unavailable. Please check logs for details.")
else:
    st.success("✅ AI model loaded successfully!")

# --- Data Management Functions ---
def load_data(file_path):
    """Loads data from a specified JSON file."""
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            st.warning(f"Data file '{os.path.basename(file_path)}' is corrupted or empty. Starting with an empty collection.")
            return []
    return []

def save_data(data, file_path):
    """Saves data to a specified JSON file."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        st.error(f"Error saving data to {os.path.basename(file_path)}: {e}. Your contribution might not be saved persistently.")

# --- Streamlit App Content ---
st.title("📜 Local Wisdom & Life Lessons")
st.markdown("---")
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
    index=0 # Default to Proverb
)

with st.form("wisdom_submission_form", clear_on_submit=True):
    if contribution_type == "Proverb":
        input_label = "Enter the proverb or saying here:"
        input_placeholder = "Example: కష్టే ఫలి (Kashte Phali) - Hard work pays off."
        help_text = "A short, traditional saying that expresses a general truth or piece of advice."
        target_file = PROVERBS_FILE
    else: # Life Lesson
        input_label = "Share your life lesson here:"
        input_placeholder = "Example: Always listen to your elders, for their experiences are a treasure map."
        help_text = "A piece of advice or insight gained from personal experience, often longer than a proverb."
        target_file = LIFE_LESSONS_FILE

    text_content = st.text_area(input_label, height=150, placeholder=input_placeholder, help=help_text)
    
    language_options = ["Telugu", "Hindi", "Tamil", "Kannada", "Malayalam", "Bengali", "Marathi", "Gujarati", "Odia", "Punjabi", "English", "Other (Please Specify)"]
    language = st.selectbox("Language:", options=language_options, index=0)
    
    if language == "Other (Please Specify)":
        language_custom = st.text_input("Please specify the language (e.g., 'Konkani', 'Bhojpuri'):")
        if language_custom:
            language = language_custom
        else:
            st.warning("Please specify the custom language.")
            language = "Unknown"

    region_hint = st.text_input("Optional: Any specific region/district this is common in?",
                                placeholder="Example: Andhra Pradesh, Telangana, Rural Punjab")
    contributor_name = st.text_input("Optional: Your Name (for credit!):", placeholder="Anonymous")

    submitted = st.form_submit_button("Submit " + contribution_type)

    if submitted:
        if text_content.strip():
            current_data = load_data(target_file)
            processed_new_text = text_content.strip()

            is_duplicate = False
            # Adjust threshold if life lessons are expected to be longer and more varied
            # A proverb might need 0.85, a life lesson might be fine with 0.75-0.80 depending on expected length/variation
            duplicate_threshold = 0.80 if contribution_type == "Life Lesson" else 0.85 

            if model is not None and current_data:
                with st.spinner(f"Checking for similar {contribution_type.lower()}s using AI..."):
                    existing_texts = [item['text'] for item in current_data]
                    try:
                        existing_embeddings = model.encode(existing_texts, convert_to_tensor=True)
                        new_embedding = model.encode([processed_new_text], convert_to_tensor=True)

                        cosine_scores = util.cos_sim(new_embedding, existing_embeddings)[0]

                        for i, score in enumerate(cosine_scores):
                            if score >= duplicate_threshold:
                                st.warning(
                                    f"⚠️ Potential duplicate found! Your {contribution_type.lower()} is very similar to: "
                                    f"**'{existing_texts[i]}'** (Similarity: {score:.2f}). "
                                    "Please consider if yours is truly unique or a slight variation."
                                )
                                is_duplicate = True
                                break
                    except Exception as e:
                        st.error(f"🚨 Error during AI similarity check: {e}. Submitting without full duplicate check for now.")
                        # Decide how to handle this: allow submission or block.
                        # For now, it proceeds with submission if error occurs during check.
            elif model is None:
                st.info(f"ℹ️ AI model not loaded. Semantic duplicate detection skipped for {contribution_type.lower()}s. (Will be submitted)")
            
            if not is_duplicate:
                new_entry = {
                    "id": str(uuid.uuid4()),
                    "type": contribution_type, # Store the type
                    "text": processed_new_text,
                    "language": language,
                    "region_hint": region_hint.strip(),
                    "contributor": contributor_name.strip() if contributor_name.strip() else "Anonymous",
                    "timestamp": datetime.now().isoformat()
                }
                
                current_data.append(new_entry)
                save_data(current_data, target_file)
                st.success(f"✅ Thank you for your contribution! Your {contribution_type.lower()} has been added.")
                st.experimental_rerun()
        else:
            st.warning("⚠️ Please enter the text before submitting.")

st.markdown("---")

# --- Browse All Contributions Section ---
st.header("Browse Shared Wisdom")

# --- Proverbs Section ---
st.subheader("📚 Shared Proverbs")
proverbs_to_display = load_data(PROVERBS_FILE)

if not proverbs_to_display:
    st.info("ℹ️ No proverbs submitted yet. Share some local wisdom!")
else:
    proverbs_to_display.sort(key=lambda x: x['timestamp'], reverse=True)
    for proverb in proverbs_to_display:
        st.markdown(f"**Proverb:** {proverb['text']}")
        st.markdown(f"**Language:** {proverb['language']}")
        if proverb['region_hint']:
            st.markdown(f"**Region:** {proverb['region_hint']}")
        st.markdown(f"**Contributed By:** {proverb['contributor']} on {datetime.fromisoformat(proverb['timestamp']).strftime('%Y-%m-%d %H:%M')}")
        st.markdown("---")

# --- Life Lessons Section ---
st.subheader("💡 Shared Life Lessons")
life_lessons_to_display = load_data(LIFE_LESSONS_FILE)

if not life_lessons_to_display:
    st.info("ℹ️ No life lessons submitted yet. Share a valuable insight!")
else:
    life_lessons_to_display.sort(key=lambda x: x['timestamp'], reverse=True)
    for lesson in life_lessons_to_display:
        st.markdown(f"**Life Lesson:** {lesson['text']}")
        st.markdown(f"**Language:** {lesson['language']}")
        if lesson['region_hint']:
            st.markdown(f"**Region:** {lesson['region_hint']}")
        st.markdown(f"**Contributed By:** {lesson['contributor']} on {datetime.fromisoformat(lesson['timestamp']).strftime('%Y-%m-%d %H:%M')}")
        st.markdown("---")


# --- Admin/Corpus Download Section ---
st.header("Download Collected Corpus (For Research & Analysis)")
st.write("This section allows researchers and administrators to download all collected data for corpus analysis.")

col1, col2 = st.columns(2)

with col1:
    if st.button("Download Proverbs as CSV"):
        if proverbs_to_display:
            df = pd.DataFrame(load_data(PROVERBS_FILE))
            df['id'] = df['id'].astype(str)
            df = df[['id', 'timestamp', 'language', 'region_hint', 'contributor', 'text', 'type']] # Include type
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
        if life_lessons_to_display:
            df = pd.DataFrame(load_data(LIFE_LESSONS_FILE))
            df['id'] = df['id'].astype(str)
            df = df[['id', 'timestamp', 'language', 'region_hint', 'contributor', 'text', 'type']] # Include type
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