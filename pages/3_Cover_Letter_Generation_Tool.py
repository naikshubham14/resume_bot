import streamlit as st
import helper, prompts
import base64

st.set_page_config(
    page_title="RESUMAGIC - Cover Letter Generator",
    layout="wide",
    page_icon=":material/description:"
)

@st.cache_data
def generate_wordcloud_image(job_description):
    st.image(helper.generate_wordcloud(job_description), use_column_width=True)

st.title("COVER LETTER GENERATOR 📄")
st.subheader("Get a tailored cover letter that highlights your strengths based on the job you’re applying for")
st.text("Here are a few tips to get the most out of the tool")
st.text("☝️. Make sure to provide comprehensive job description which includes role details, required skills.")
st.text("✌️. Make sure the include the details and the name of the company in the job description")
st.text(" ")
st.markdown(
""" If you like the project or have suggestions please feel free to reach out to me here ➡️
<a href="https://www.linkedin.com/in/shubham-rajan-naik/" target="_blank">
    LinkedIn
</a>
""",
unsafe_allow_html=True
)

col1, col2 = st.columns(2)

# Add a file uploader
with col1:
        st.subheader("Upload your Resume")
        resume = st.file_uploader("Upload Resume",accept_multiple_files=False,type=("pdf", "txt"), key="resume", label_visibility="hidden")
        company=st.text_area(label="Company", placeholder="Name of the company you are applying at.", key="company")
        position=st.text_area(label="Position", placeholder="Title of the position you are applying for.", key="position")

with col2:
    st.subheader("Paste the Job Description")
    job_description=st.text_area("Job Description", height=355, placeholder="Paste Job Description", key="job_description", label_visibility="hidden")

if(resume is None or len(job_description) == 0):
    if(resume is None and len(job_description) == 0):
        st.error("Please upload add Resume and Job Description to proceed.")
    if (resume is None and len(job_description) != 0):
        st.error("Please upload Resume to proceed.")
    if (resume is not None and len(job_description) == 0):
        st.error("Please upload Job Description to proceed")

if(st.button("Generate", type="primary", disabled=resume is None or len(job_description) == 0, use_container_width=True, icon=":material/contract_edit:")):
    resume_content = helper.read_file(resume)
    cover_letter_generator_prompt = prompts.build_cover_letter_generator_promt(resume_content, job_description, company, position)
    with st.spinner("Generating Cover Letter"):
                cover_letter = helper.llm_call(cover_letter_generator_prompt)
                st.divider()
                b64_content = base64.b64encode(cover_letter.encode()).decode()
                st.markdown(f'''
                <a href="data:file/txt;base64,{b64_content}" download="Cover Letter.txt" 
                style="text-decoration:none;color:white;background:#28a745;padding:15px 25px;border-radius:8px;
                        box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3);font-size:16px;font-weight:bold;
                        transition: background-color 0.3s, box-shadow 0.3s;">
                Download Your Cover Letter
                </a>
                <style>
                    a:hover {{
                        background-color: #218838;
                        box-shadow: 0 6px 12px rgba(0, 123, 255, 0.4);
                    }}
                </style>
            ''', unsafe_allow_html=True)
