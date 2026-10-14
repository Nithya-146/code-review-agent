import streamlit as st
import os
import sys

# Ensure project root directory is accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from app.python_parser import validate_python
    from app.java_parser import validate_java
except ModuleNotFoundError:
    from python_parser import validate_python
    from java_parser import validate_java

st.set_page_config(page_title="Code Submission & AST Validator", layout="wide")

st.title("🛡️ Secure Code Inspection Platform")
st.subheader("Step 4: Code Submission & AST Pre-Validation Module")

# Language Selection with unique key
language = st.selectbox(
    "Select Language", 
    ["Python (.py)", "Java (.java)"],
    key="lang_select_box"
)

# Submission Mode Tabs
tab_upload, tab_paste = st.tabs(["📁 File Upload", "✍️ Paste Code"])

code_content = ""
selected_lang = "python" if "Python" in language else "java"

with tab_upload:
    uploaded_file = st.file_uploader(
        "Upload a source code file (.py or .java only)", 
        type=["py", "java"],
        key="file_uploader_widget"
    )
    if uploaded_file is not None:
        file_ext = uploaded_file.name.split(".")[-1].lower()
        if file_ext not in ["py", "java"]:
            st.error("Invalid file extension! Only .py and .java files are accepted.")
        else:
            code_content = uploaded_file.read().decode("utf-8")
            st.info(f"Loaded `{uploaded_file.name}` ({len(code_content.splitlines())} lines)")

with tab_paste:
    pasted_code = st.text_area(
        "Or paste your code here directly:",
        height=250,
        placeholder="Enter your Python or Java code snippet here...",
        key="code_text_area"
    )
    if pasted_code.strip():
        code_content = pasted_code

# Run AST Validation Button
if st.button("Validate Source Code Syntax", key="validate_button"):
    if not code_content.strip():
        st.warning("Submission is empty. Please upload a file or paste code before validating.")
    else:
        st.write("---")
        if selected_lang == "python":
            result = validate_python(code_content)
        else:
            result = validate_java(code_content)

        if result["is_valid"]:
            st.success("✅ Syntax Validation Passed! The code is ready for downstream agent analysis.")
            st.json(result["metadata"])
        else:
            st.error("❌ AST Validation Failed: Syntax Error Detected")
            st.error(result["error"])
            st.warning("Fix syntax errors before submitting to the security analysis pipeline.")