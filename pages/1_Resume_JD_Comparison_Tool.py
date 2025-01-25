
import streamlit as st
import helper
import json_repair
import prompts


st.set_page_config(
    page_title="RESUMAGIC - JD Analyzer",
    layout="wide",
    page_icon=":material/description:"
)

@st.cache_data
def generate_wordcloud_image(job_description):
    st.image(helper.generate_wordcloud(job_description), use_column_width=True)

st.title("JOB DESCRIPTION - RESUME ANALYZER 📄")
st.subheader("Check how your resume stacks up against the job requirements")
st.text("Here are a few tips to get the most out of the tool")
st.text("☝️. Make sure to provide comprehensive job description which includes role details, required skills.")
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
with col2:
    st.subheader("Paste the Job Description")
    job_description=st.text_area("Job Description", height=325, placeholder="Paste Job Description", key="job_description", label_visibility="hidden")

if(resume is None or len(job_description) == 0):
    if(resume is None and len(job_description) == 0):
        st.error("Please upload add Resume and Job Description to proceed.")
    if (resume is None and len(job_description) != 0):
        st.error("Please upload Resume to proceed.")
    if (resume is not None and len(job_description) == 0):
        st.error("Please upload Job Description to proceed")

if(st.button("Compare", type="primary", disabled=resume is None or len(job_description) == 0, use_container_width=True, icon=":material/compare_arrows:")):
        st.divider()
        resume_content = helper.read_file(resume)
        resume_jd_eval_prompt = prompts.build_resume_jd_eval_prompt(resume_content, job_description)
        with st.spinner("Mathcing the job description"):
            response = helper.llm_call(resume_jd_eval_prompt).strip().replace("```json", "").replace("```", "").replace("\n", "")
            response = json_repair.loads(response)
            # Define match level colors
            match_level_colors = {
                "Excellent Match": "#4CAF50",  # Green
                "Potential Match": "#FFA500",  # Orange
                "Not a Match": "#FF5252"      # Red/Amber
            }

            # Get the color for the match level
            match_color = match_level_colors.get(response["match_level"], "#000000")  # Default to black if no match

            # Custom CSS for horizontal skill pills with fixed height
            st.markdown("""
            <style>
            .pill-container {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin-top: 5px;
                max-height: 100px; /* Fixed height */
                overflow-y: auto; /* Scroll if content exceeds the height */
            }
            .pill {
                background-color: #e1f5fe;
                color: #0277bd;
                border-radius: 12px;
                padding: 5px 10px;
                font-size: 14px;
                display: inline-block;
                margin: 0;
            }
            .pill-jd {
                background-color: #e8f5e9;
                color: #1b5e20;
            }
            </style>
            """, unsafe_allow_html=True)

            # Title
            st.markdown(f"""<h1 style='text-align: center;'>
                        Resume vs Job Description Analysis
                        </h1>""", unsafe_allow_html=True)

            # Match Level as the centerpiece with dynamic color
            st.markdown(f"""
            <h2 style='text-align: center; color: {match_color};'>
                {response['match_level']}
            </h1>
            """, unsafe_allow_html=True)
            st.divider()
            # Resume and JD Extraction Table
            st.markdown("<h2 style='text-align: center;'>Resume and JD Extraction</h2>", unsafe_allow_html=True)

            col3, col4 = st.columns(2)
            # Resume extraction
            with col3:
                st.subheader("Resume Extraction")
                st.markdown("### Skills")
                st.markdown('<div class="pill-container">' + ''.join([f'<div class="pill">{skill}</div>' for skill in response["resume_extraction"]["skills"]]) + '</div>', unsafe_allow_html=True)
            with col4:
                st.subheader("Job Description Extraction")
                st.markdown("### Skills")
                st.markdown('<div class="pill-container">' + ''.join([f'<div class="pill pill-jd">{skill}</div>' for skill in response["job_description_extraction"]["skills"]]) + '</div>', unsafe_allow_html=True)
            st.divider()

            col5, col6 = st.columns(2)  
            with col5:
                st.markdown("### Education")
                st.write(response["resume_extraction"]["education"])
            with col6:
                st.markdown("### Education")
                st.write(response["job_description_extraction"]["education"])
            st.divider()
            
            col7, col8 = st.columns(2)
            with col7:
                st.markdown("### Work Experience")
                st.write("\n".join(response["resume_extraction"]["work_experience"]))
            with col8:
                st.markdown("### Work Experience")
                st.write("\n".join(response["job_description_extraction"]["work_experience"]))
            st.divider()

            # Comparison Analysis
            st.markdown("<h2 style='text-align: center;'>Comparison Analysis</h2>", unsafe_allow_html=True)
            
            col9, col10 = st.columns(2)
            # Skills alignment
            with col9:
                st.markdown("#### Skills Alignment")
                matching_skills = ', '.join(response['comparison_analysis']['skills_alignment']['matching_skills'])
                missing_skills = ', '.join(response['comparison_analysis']['skills_alignment']['missing_skills'])
                # Using HTML to style the text
                st.markdown(f"<span style='color: green;'> **Matching Skills:** </span> {matching_skills}", unsafe_allow_html=True)
                st.markdown(f"<span style='color: red;'> **Missing Skills:** </span> {missing_skills}", unsafe_allow_html=True)            
            # Education alignment
            with col10:
                st.markdown("#### Education Alignment")
                st.write(response["comparison_analysis"]["education_alignment"])
            st.divider()
            
            col11, col12 = st.columns(2)
            # Work experience alignment
            with col11:
                st.markdown("#### Work Experience Alignment")
                st.markdown(f"<span style='color: green;'>**Matching Experience:**</span> {', '.join(response['comparison_analysis']['work_experience_alignment']['matching_experience'])}", unsafe_allow_html=True)
                st.markdown(f"<span style='color: red;'>**Gaps in Experience:**</span> {', '.join(response['comparison_analysis']['work_experience_alignment']['gaps_in_experience'])}", unsafe_allow_html=True)
            
            # Conclusion (less prominent)
            with col12:
                st.markdown("<h3>Conclusion</h3>", unsafe_allow_html=True)
                st.write(response["conclusion"])
            st.divider()
            st.markdown("<h2 style='text-align: center;'>Wordcloud based on Job Description Phrase Weightage</h2>", unsafe_allow_html=True)
            generate_wordcloud_image(job_description)