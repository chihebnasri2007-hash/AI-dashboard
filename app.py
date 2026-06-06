import streamlit as st
import pandas as pd
import google.generativeai as genai

# Configure the free API key (Get one from Google AI Studio for $0)
genai.configure(api_key="YOUR_API_KEY_HERE")

st.title("📊 Free Local Data AI Assistant")
st.write("Upload a CSV and ask questions in plain English.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(uploaded_file, encoding='latin-1')
        except:
            df = pd.read_csv(uploaded_file, encoding='cp1252')
    # Capture user question
    user_question = st.text_input("What would you like to know about this data?")
    
    if user_question:
        # Construct a strict prompt telling the model to return ONLY clean code
        prompt = f"""
        You are an expert data analyst. You are given a pandas DataFrame named 'df' with the following columns: {list(df.columns)}.
        The data types are:\n{df.dtypes}.
        
        Write the exact Python pandas code to answer this question: '{user_question}'.
        Return ONLY executable Python code using the variable 'df'. Do not include explanations, code blocks (```), or markdown.
        If a chart is requested, use streamlit command like 'st.bar_chart()' or 'st.line_chart()'. Otherwise, print the result using 'st.write()'.
        """
        
        model = genai.GenerativeModel("gemini-3-flash-preview")
        response = model.generate_content(prompt)
        cleaned_code = response.text.strip().replace("```python", "").replace("```", "")
        
        st.write("### Executing Generated Code:")
        st.code(cleaned_code, language="python")
        
        # Execute the generated code locally against the dataframe
        try:
            exec(cleaned_code)
        except Exception as e:
            st.error(f"Execution Error: {e}")