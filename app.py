import streamlit as st
from transformers import pipeline

# Set the Streamlit page configuration
st.set_page_config(page_title="Text Summarization Tool", layout="wide")

# Loading the model
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

# Load the summarizer pipeline
summarizer = load_summarizer()

# App Title and Description
st.title("📝 Text Summarization Tool")
st.markdown("Enter text below and click **Summarize** to get a concise version.")

# Text input area for user to enter content
input_text = st.text_area("Enter text to summarize:", height=300)

# When the user clicks the 'Summarize' button
if st.button("Summarize"):
    # Check if input is not empty
    if not input_text.strip():
        st.warning("⚠️ Please enter some text to summarize.")
    else:
        # Show spinner while summarizing
        with st.spinner("Summarizing... Please wait."):
            try:
                # Generate summary using the pipeline
                summary = summarizer(input_text, max_length=150, min_length=30, do_sample=False)
                summary_text = summary[0]['summary_text']
                
                # Display the summary
                st.subheader("📌 Summary:")
                st.success(summary_text)
            except Exception as e:
                # Handle and display any errors
                st.error(f"Error: {e}")
