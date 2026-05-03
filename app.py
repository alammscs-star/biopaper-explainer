import streamlit as st
from groq import Groq
import PyPDF2
import io

st.set_page_config(page_title="BioPaper Explainer", page_icon="🧬")

st.title("🧬 BioPaper Explainer")
st.write("Upload a biology research paper PDF and get a simple explanation using Groq AI")

# API Key from Streamlit Secrets - GitHub pe safe rahegi
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

# Sidebar for options
with st.sidebar:
    st.header("Settings")
    model = st.selectbox(
        "Groq Model",
        ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
    )
    explanation_level = st.radio(
        "Explanation Level",
        ["Beginner - Simple terms", "Student - High school level", "Expert - Technical"]
    )

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Extract text from PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    st.success(f"PDF loaded! {len(pdf_reader.pages)} pages, {len(text)} characters")

    with st.expander("View extracted text"):
        st.text(text[:1000] + "...")

    if st.button("Explain This Paper", type="primary"):
        with st.spinner("Groq AI is reading the paper..."):
            try:
                prompt = f"""
                You are a biology tutor. Explain this research paper at {explanation_level} level.

                Give me:
                1. Main finding in 2 sentences
                2. Why it matters
                3. Key terms explained simply
                4. Real world application

                Paper text:
                {text[:8000]}
                """

                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=1500
                )

                st.subheader("📝 Explanation")
                st.markdown(response.choices[0].message.content)

            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Check if your GROQ_API_KEY is set in Streamlit Secrets")

else:
    st.info("👆 Upload a biology research paper PDF to get started")

st.markdown("---")
st.caption("Built with Streamlit + Groq | For Hackathon 2026")