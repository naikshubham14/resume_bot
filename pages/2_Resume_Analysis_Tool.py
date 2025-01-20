import streamlit as st
import helper
from reportlab.lib.pagesizes import letter
import json


st.set_page_config(
    page_title="Analyzer",
    layout="wide",
    page_icon=":material/description:"
)

st.title("RESUME ANALYZER 📄")
st.subheader("Get real insights on how to make your resume stand out")
st.text("☝️. Make sure to provide a brief but precise work profile")
st.text("✌️. Make sure to provide the work experience number")
st.markdown(
""" If you like the project or have suggestions please feel free to reach out to me here ➡️
<a href="https://www.linkedin.com/in/shubham-rajan-naik/" target="_blank">
    LinkedIn
</a>
""",
unsafe_allow_html=True
)

# Add a file uploader
resume = st.file_uploader("Upload Resume",accept_multiple_files=False,type=("pdf", "txt"), key="resume")
col1, col2 = st.columns(2)
with col1:
    profile=st.text_area(label="Profile", placeholder="Please mention your job profile ie. Software Engineer, Data Scientist etc", key="profile")
with col2:
    experience = st.number_input("Years of Experience", min_value=0, max_value=50, step=1)
st.divider()

missing_fields = []

if resume is None:
    missing_fields.append("Resume")
if not profile.strip():
    missing_fields.append("Profile")

if missing_fields:
    # Display error message with missing fields
    st.error(f"Please add {', '.join(missing_fields)} to proceed.")
    
if(st.button("Generate", type="primary", disabled=resume is None, use_container_width=True, icon=":material/send:")):
        st.divider()
        resume_content = helper.read_file(resume)
        resume_evaluation_promt = helper.build_resume_evaluation_promt(resume_content, profile, str(experience))
        with st.spinner("Evaluating Your Resume"):
            resume_eval = helper.llm_call(resume_evaluation_promt)
            st.subheader("Resume Analysis")
            response = resume_eval.strip().replace("```json", "").replace("```", "")
            response = json.loads(response)
            st.markdown(f"""
                        <div style="width: 100%; text-align: center; margin: 20px 0;">
                            <!-- Gauge Container -->
                            <div style="position: relative; width: 80%; height: 30px; margin: 0 auto; background: linear-gradient(to right, red, orange, yellow, green); border-radius: 15px; overflow: hidden;">
                                <!-- Dynamic Bar -->
                                <div style="position: absolute; top: -5px; left: calc({response["ats_score"]}% - 5px); width: 10px; height: 40px; background-color: #000000; border-radius: 5px;"></div>
                            </div>
                            <!-- Score Text -->
                            <div style="margin-top: 10px; font-size: 1.5em; font-weight: bold; color: #333;">
                                ATS Score: {response["ats_score"]} / 100
                            </div>
                        </div>""", unsafe_allow_html=True)
            st.write(resume_eval)   
        st.divider()