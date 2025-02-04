import streamlit as st
import helper
import json_repair
import prompts
import spacy

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("sentencizer")



st.set_page_config(
    page_title="Job Fit Analyzer",
    layout="wide",
    page_icon=":material/description:"
)

@st.cache_data
def generate_wordcloud_image(job_description):
    st.image(helper.generate_wordcloud(job_description), use_column_width=True)

# Custom CSS for horizontal skill pills with fixed height
st.markdown("""
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
<style>
.header-banner {
background: linear-gradient(135deg, #4e54c8, #8f94fb);
color: #fff;
padding: 2rem 0;
text-align: center;
border-radius: 30px 30px 30px 30px;
box-shadow: 0 2px 10px rgba(0,0,0,0.1);
margin-bottom: 20px;
}
.header-banner h1 {
font-size: 3rem;
margin-bottom: 0.5rem;
}
.header-banner p {
font-size: 1.25rem;
}
.pill {
    background-color: #a6d4e9;
    color: #246a93;
    border-radius: 12px;
    padding: 5px 10px;
    font-size: 14px;
    display: inline-block;
    margin: 3px;
}
.pill-jd {
    background-color: #b6f9bb;
    color: #007909;
}
.content-box {
    background: #f8f9fa;
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
    height: 300px; /* Fixed height */
    overflow-y: auto; /* Enable vertical scrolling */
}
.education-box {
    height: 150px;
}
.section-header {
        font-weight: bold;
        color: #2b547e;
        margin-bottom: 10px;
        text-align: center;
        font-size: 20px;
        text-decoration: underline;
}
.section-list {
    padding-left: 20px;
    list-style-type: disc;
    color: #333; /* Neutral text color */
    line-height: 1.6;
    
</style>
""", unsafe_allow_html=True)

# Header Banner Section
st.markdown(
    """
    <div class="header-banner">
        <h1>Job Fit Analyzer 🧠</h1>
        <p>Discover how your resume measures up against job requirements</p>
        <p>
            <small>
            For suggestions or feedback, let's connect on <a href="https://www.linkedin.com/in/shubham-rajan-naik/" target="_blank" style="color:#fff; text-decoration:underline;">LinkedIn</a>
            </small>
        </p>
    </div>
    """, unsafe_allow_html=True
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
                st.markdown(f"""
                            <div class='content-box'>
                                <div class='section-header'>Skills</div>
                                <div class="pill-container">
                                    {''.join([f'<div class="pill">{skill}</div>' for skill in response["resume_extraction"]["skills"]])}
                                </div>
                            </div>""", unsafe_allow_html=True)
            with col4:
                st.subheader("Job Description Extraction")
                st.markdown(f"""
                            <div class='content-box'>
                                <div class='section-header'>Skills</div>
                                <div class="pill-container">
                                    {''.join([f'<div class="pill pill-jd">{skill}</div>' for skill in response["job_description_extraction"]["skills"]])}
                                </div>
                            </div>""" , unsafe_allow_html=True)
            st.divider()

            col5, col6 = st.columns(2)  
            with col5:
                st.markdown(f"""
                            <div class='content-box education-box'>
                                <div class='section-header'>Education</div>
                                <span style='color: black;'>
                                    {response["resume_extraction"]["education"]}
                                </span>
                            </div>""" , unsafe_allow_html=True)
            with col6:
                st.markdown(f"""
                            <div class='content-box education-box'>
                                <div class='section-header'>Education</div>
                                <span style='color: black;'>
                                    {response["job_description_extraction"]["education"]}
                                    </span>
                            </div>""" , unsafe_allow_html=True)
            st.divider()
            
            col7, col8 = st.columns(2)
            with col7:
                st.markdown(f"""
                            <div class='content-box'>
                                <div class='section-header'>Work Experience</div>
                                    <span style='color: black;'>
                                    {"\n".join(response["resume_extraction"]["work_experience"])}
                                    </span>
                            </div>""" , unsafe_allow_html=True)
            with col8:
                st.markdown(f"""
                            <div class='content-box'>
                                <div class='section-header'>Work Experience</div>
                                    <span style='color: black;'>
                                    {"\n".join(response["job_description_extraction"]["work_experience"])}
                                    </span>
                            </div>""" , unsafe_allow_html=True)
            st.divider()

            # Comparison Analysis
            st.markdown("<h2 style='text-align: center;'>Comparison Analysis</h2>", unsafe_allow_html=True)
            
            col9, col10 = st.columns(2)
            # Skills alignment
            with col9:
                st.markdown("""
                            <div class='content-box'>
                                <div class='section-header'>Skills Alignment</div>
                                <div style='display: flex; text-align: center;'>
                                    <div style='flex: 1;'>
                                        <span style='color: green; font-weight: bold;'>Matching Skills</span>
                                        <ul style='list-style-type: disc; text-align: left;'>
                                            {matching_skills_list}
                                        </ul>
                                    </div>
                                    <div style='flex: 1;'>
                                        <span style='color: red; font-weight: bold;'>Missing Skills</span>
                                        <ul style='list-style-type: disc; text-align: left;'>
                                            {missing_skills_list}
                                        </ul>
                                    </div>
                                </div>
                            </div>""".format(
                                matching_skills_list=''.join(f"<li style='color: black;'>{skill}</li>" 
                                    for skill in response['comparison_analysis']['skills_alignment']['matching_skills']),
                                missing_skills_list=''.join(f"<li style='color: black;'>{skill}</li>" 
                                    for skill in response['comparison_analysis']['skills_alignment']['missing_skills'])
                            ), unsafe_allow_html=True)
            # Education alignment
            with col10:
                st.markdown("""
                            <div class='content-box'>
                                <div class='section-header'>Work Experience Alignment</div>
                                <div style='display: flex;'>
                                    <div style='flex: 1;'>
                                        <span style='color: green; font-weight: bold;'>Matching Experience:</span>
                                        <ul style='list-style-type: disc;'>
                                            {matching_exp_list}
                                        </ul>
                                    </div>
                                    <div style='flex: 1;'>
                                        <span style='color: red; font-weight: bold;'>Gaps in Experience:</span>
                                        <ul style='list-style-type: disc;'>
                                            {gaps_exp_list}
                                        </ul>
                                    </div>
                                </div>
                            </div>""".format(
                                matching_exp_list=''.join(f"<li style='color: black;'>{exp}</li>" 
                                    for exp in response['comparison_analysis']['work_experience_alignment']['matching_experience']),
                                gaps_exp_list=''.join(f"<li style='color: black;'>{exp}</li>" 
                                    for exp in response['comparison_analysis']['work_experience_alignment']['gaps_in_experience'])
                            ), unsafe_allow_html=True)
                
            st.divider()
            
            col11, col12 = st.columns(2)
            # Work experience alignment
            with col11:
                st.markdown(f"""
                            <div class='content-box'>
                                <div class='section-header'>Education Alignment</div>
                                <span style='color: black;'>
                                    {response["comparison_analysis"]["education_alignment"]}
                                </span>
                            </div>""" , unsafe_allow_html=True)
            # Conclusion (less prominent)
            with col12:
                st.markdown(f"""
                            <div class='content-box'>
                                <div class='section-header'>Conclusion Alignment</div>
                                <span style='color: black;'>
                                    {response["conclusion"]}
                                </span>
                            </div>""" , unsafe_allow_html=True)
            st.divider()
            st.markdown("<h2 style='text-align: center;'>Wordcloud based on Job Description Phrase Weightage</h2>", unsafe_allow_html=True)
            generate_wordcloud_image(job_description)
            
            