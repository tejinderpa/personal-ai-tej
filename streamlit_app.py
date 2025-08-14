import streamlit as st
import google.generativeai as genai
from langchain.prompts import PromptTemplate

# --- App Title and Description ---
st.title("🤖 Your Personal AI Assistant")
st.write("This application leverages the power of Google's Generative AI to answer your questions on any topic.")

import os
import streamlit as st

# Try environment variable first, then Streamlit secrets
API_KEY = os.getenv("API_KEY") or st.secrets.get("API_KEY")

if not API_KEY:
    st.error("API_KEY is missing. Please set it in environment variables or Streamlit Secrets.")
    st.stop()


# import os

# API_KEY = os.environ.get("API_KEY")
# if not API_KEY:
#     raise ValueError("API_KEY environment variable not set.")

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
    except Exception as e:
        st.sidebar.error(f"Failed to configure API key: {e}")

# --- Prompt Template Definition ---
template = """
You are an expert on the topic of {topic}.
Your task is to provide a clear and concise answer to the following question:

Question: {question}

Answer:
"""

prompt_template = PromptTemplate(
    input_variables=["topic", "question"],
    template=template
)

# --- User Input ---
st.header("Ask a Question")
topic_input = st.text_input("Enter a topic:", "History")
question_input = st.text_area("What is your question?")

# --- Generate Response ---
if st.button("Get Answer"):
    if not API_KEY:
        st.warning("Please enter your API key in the sidebar to proceed.")
    elif not topic_input or not question_input:
        st.warning("Please provide both a topic and a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                # Initialize the model
                model = genai.GenerativeModel('gemini-2.0-flash')

                # Create the prompt from the template
                formatted_prompt = prompt_template.format(topic=topic_input, question=question_input)

                # Generate content
                response = model.generate_content(formatted_prompt)

                # Display the answer
                st.subheader("Answer:")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"An error occurred: {e}")