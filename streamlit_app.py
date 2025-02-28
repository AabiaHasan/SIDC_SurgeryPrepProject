import streamlit as st
import pandas as pd
import datetime
from io import StringIO
import fitz  # PyMuPDF for PDF processing
from PIL import Image

# Set page config with a blue theme
st.set_page_config(page_title="Patient Surgery Prep", layout="wide")

# Apply custom styling
st.markdown(
    """
    <style>
    body {
        background-color: #e3f2fd;
        color: #0d47a1;
    }
    .stButton>button {
        background-color: #2196f3;
        color: white;
        border-radius: 10px;
        padding: 8px 16px;
    }
    .stButton>button:hover {
        background-color: #1976d2;
    }
    .stExpander {
        border: 1px solid #90caf9;
        background-color: #bbdefb;
        border-radius: 10px;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
        border: 1px solid #64b5f6;
    }
    .css-1d391kg, .css-1v3fvcr {
        background-color: #e3f2fd !important;
    }
    h1, h2, h3 {
        color: #0d47a1;
    }
    .stSidebar {
        background-color: #bbdefb !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Homepage
st.title("🏥 Welcome to the Patient Surgery Prep Site")
st.write("This site helps hospital staff organize and reach out to patients. Use the **Patients** tab to manage patient details and prioritize follow-ups. The **Documents** tab allows you to upload medical documents for AI-generated summaries and next steps.")

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
tab = st.sidebar.radio("Go to:", ["🩺 Patients", "📄 Documents"])

# Patients Data Management
if "patients" not in st.session_state:
    st.session_state.patients = []
if "show_add_patient" not in st.session_state:
    st.session_state.show_add_patient = False

if tab == "🩺 Patients":
    st.header("👨‍⚕️ Patients List")
    
    if st.button("➕ Add Patient"):
        st.session_state.show_add_patient = not st.session_state.show_add_patient
    
    if st.session_state.show_add_patient:
        with st.form("add_patient_form"):
            name = st.text_input("📝 Patient Name")
            age = st.number_input("🎂 Age", min_value=0, max_value=120, step=1)
            weight = st.number_input("⚖️ Weight (kg)", min_value=0.0, step=0.1)
            height = st.number_input("📏 Height (cm)", min_value=0.0, step=0.1)
            contact = st.text_input("📞 Contact Information")
            surgery = st.selectbox("🏥 Surgery Type", ["Simple", "Medium", "Complex"])
            surgery_date = st.date_input("📅 Surgery Date", min_value=datetime.date.today())
            last_contacted = st.date_input("📬 Last Contacted", min_value=datetime.date(2000, 1, 1))
            submitted = st.form_submit_button("✅ Add Patient")
            
            if submitted and name:
                st.session_state.patients.append({
                    "Name": name,
                    "Age": age,
                    "Weight": weight,
                    "Height": height,
                    "Contact": contact,
                    "Surgery": surgery,
                    "Surgery Date": surgery_date,
                    "Last Contacted": last_contacted
                })
                st.session_state.show_add_patient = False
                st.success(f"Added patient {name}")
    
    if not st.session_state.patients:
        st.write("❌ No patients added.")
    else:
        # Sorting patients by priority
        def priority_sort(patient):
            surgery_priority = {"Simple": 1, "Medium": 2, "Complex": 3}
            days_until_surgery = (patient["Surgery Date"] - datetime.date.today()).days
            days_since_contact = (datetime.date.today() - patient["Last Contacted"]).days
            return (-surgery_priority[patient["Surgery"]], days_until_surgery, -days_since_contact)

        st.session_state.patients.sort(key=priority_sort)
        
        # Display patient cards
        for patient in st.session_state.patients:
            with st.expander(f"👤 {patient['Name']} ({patient['Surgery']}) - Surgery on {patient['Surgery Date']}"):
                st.write(f"**🎂 Age:** {patient['Age']}")
                st.write(f"**⚖️ Weight:** {patient['Weight']} kg")
                st.write(f"**📏 Height:** {patient['Height']} cm")
                st.write(f"**📞 Contact:** {patient['Contact']}")
                st.write(f"**📬 Last Contacted:** {patient['Last Contacted']}")

# Document Upload and Placeholder for AI Summary
elif tab == "📄 Documents":
    st.header("📂 Upload Medical Documents")
    uploaded_file = st.file_uploader("📤 Upload a PDF", type=["pdf"])
    
    if uploaded_file:
        st.write("📑 **Uploaded File:**", uploaded_file.name)
        
        # Extract text from PDF
        def extract_text_from_pdf(file):
            doc = fitz.open(stream=file.read(), filetype="pdf")
            text = "\n".join([page.get_text("text") for page in doc])
            return text
        
        pdf_text = extract_text_from_pdf(uploaded_file)
        
        # Placeholder for AI Summary
        st.subheader("🤖 AI-Generated Summary")
        st.write("🚧 AI summary functionality is under development. Please check back later.")
