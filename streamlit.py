import streamlit as st
import requests
import json

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="centered")

st.markdown("""
    <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            border-radius: 8px;
            padding: 10px 20px;
        }
        .stTextInput>div>div>input {
            font-size: 16px;
            padding: 10px;
            border-radius: 8px;
        }
        .stFileUploader>div>div>button {
            background-color: #FF5733;
            color: white;
            font-size: 16px;
            border-radius: 8px;
            padding: 10px 15px;
        }
        .response-card {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)


st.markdown("<h1 style='text-align: center; color: #007BFF;'><b>📄 AI Resume Analyzer</b></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6c757d;'><b>Upload your Resume & Enter a Job Description to assess match</b></p>", unsafe_allow_html=True)

with st.container():
    jd_input = st.text_area("**💼 Enter Job Description:**", height=150)
    uploaded_file = st.file_uploader("**📂 Upload your Resume**", type=["pdf"])

if uploaded_file and jd_input:
    if st.button("**🔍 Analyze Resume**"):
        with st.spinner("**⏳ Analyzing... Please wait**"):
            # API Request
            url = <<get_your_own_api_via_amazon_apigateway>>
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            payload = {'job_description': jd_input}
            headers = {}

            response = requests.post(url, headers=headers, data=payload, files=files)

            if response.status_code == 200:
                try:
                    response_data = response.json()
                    st.markdown("<h3 style='color: #28A745;'><b>✅ Analysis Result</b></h3>", unsafe_allow_html=True)
                    st.markdown('<div class="response-card">', unsafe_allow_html=True)
                    st.json(response_data)  # Pretty Print JSON
                    st.markdown('</div>', unsafe_allow_html=True)

                except json.JSONDecodeError:
                    st.error("⚠️ Error: Unable to parse JSON response.")
            else:
                st.error(f"❌ API Error: {response.status_code}")
