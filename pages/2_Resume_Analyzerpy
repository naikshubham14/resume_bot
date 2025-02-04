import streamlit as st
import helper, prompts
import json_repair
import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("sentencizer")


st.set_page_config(
    page_title="Resume Analyzer",
    layout="wide",
    page_icon=":material/description:"
)

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
            </style>""", unsafe_allow_html=True)

# Header Banner Section
st.markdown(
    """
    <div class="header-banner">
        <h1>Resume Analyzer ✍️</h1>
        <p>Get real insights on how to make your resume stand out</p>
        <p>
            <small>
            For suggestions or feedback, let's connect on <a href="https://www.linkedin.com/in/shubham-rajan-naik/" target="_blank" style="color:#fff; text-decoration:underline;">LinkedIn</a>
            </small>
        </p>
    </div>
    """, unsafe_allow_html=True
)

# Add a file uploader
st.subheader("Upload your Resume")
resume = st.file_uploader("Upload Resume",accept_multiple_files=False,type=("pdf", "txt"), key="resume", label_visibility="hidden")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Profile")
    profile=st.text_area(label="Profile", placeholder="Please mention your job profile ie. Software Engineer, Data Scientist etc", key="profile", label_visibility="hidden")
with col2:
    st.subheader("Years of Experience")
    experience = st.number_input("Years of Experience", min_value=0, max_value=50, step=1, label_visibility="hidden")
st.divider()

missing_fields = []

if resume is None:
    missing_fields.append("Resume")
if not profile.strip():
    missing_fields.append("Profile")

if missing_fields:
    # Display error message with missing fields
    st.error(f"Please add {', '.join(missing_fields)} to proceed.")
    
if(st.button("Analyze", type="primary", disabled=resume is None, use_container_width=True, icon=":material/cognition:")):
        st.divider()
        resume_content = helper.read_file(resume)
        resume_evaluation_promt = prompts.build_resume_evaluation_promt(resume_content, profile, str(experience))
        with st.spinner("Evaluating Your Resume"):
            resume_eval = helper.llm_call(resume_evaluation_promt)
            response = resume_eval.strip().replace("```json", "").replace("```", "").replace("\n", "")
            response = json_repair.loads(response)
            
            ats_score = response["ats_score"]
            
            overall_impressions = response["overall_impression"]
            
            section_breakdown = response["section_breakdown"]
            
            metrics_evaluation = [["Metric", "Score", "Comments"]]
            metric_sum = 0
            for key, value in response["metrics_evaluation"].items():
                metric_name = ' '.join([part.capitalize() for part in key.split('_')])
                score = int(value["score"])
                comment = value["comments"]
                metrics_evaluation.append([metric_name, score, comment])
                metric_sum += score
                
            ats_score = metric_sum
            
            st.markdown(f"""<h2 style='text-align: center;'>
                        Score
                        </h2>""", unsafe_allow_html=True)
            st.markdown(f"""
                        <div style="width: 100%; text-align: center; margin: 20px 0;">
                            <!-- Gauge Container -->
                            <div style="position: relative; width: 80%; height: 30px; margin: 0 auto; background: linear-gradient(to right, red, orange, yellow, green); border-radius: 15px; overflow: hidden;">
                                <!-- Dynamic Bar -->
                                <div style="position: absolute; top: -5px; left: calc({ats_score}% - 5px); width: 10px; height: 40px; background-color: #000000; border-radius: 5px;"></div>
                            </div>
                            <!-- Score Text -->
                        </div>""", unsafe_allow_html=True)
            st.markdown(f"""<h4 style='text-align: center;'>
                                ATS Score: {ats_score} / 100
                            </h4>""", unsafe_allow_html=True)
            st.divider()
            st.markdown(f"""<h2 style='text-align: center;'>
                        Key Metrics Evaluation
                        </h2>""", unsafe_allow_html=True)
            df = pd.DataFrame(metrics_evaluation[1:], columns=metrics_evaluation[0])
            st.markdown("""
                <style>
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        margin: 20px 0;
                        font-size: 16px;
                        text-align: left;
                        box-shadow: 0px 4px 8px;
                        border-radius: 10px;
                        overflow: hidden;
                    }
                    th, td {
                        border: 2px solid;
                        padding: 12px 15px;
                    }
                    th {
                        font-weight: bold;
                        text-align: center;
                    }
                </style>
            """, unsafe_allow_html=True)

            # Render the table
            st.markdown(
                df.to_html(index=False, escape=False),
                unsafe_allow_html=True
            )
            
            st.divider()
            
            st.markdown(f"""<h2 style='text-align: center;'>
                        Section Breakdown
                        </h2>""", unsafe_allow_html=True)            
            st.markdown("""
                <style>
            
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
            .small-box {
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
            </style>""", unsafe_allow_html=True)

            # Create columns for displaying content
            col3, col4 = st.columns(2)
            col5, col6 = st.columns(2)
            col7, col8 = st.columns(2)

            # Function to display each section
            def display_section(column, title, content):
                with column:
                    st.markdown(f"""
                        <div class='content-box {'small-box' if title in ["Contact Information","Objective Summary"] else ''}'>
                            <div class='section-header'>{title}</div>
                            <ul class="section-list">
                                {''.join([f'<li>{point.strip()}</li>' for point in helper.split_sentences(nlp, content) if point.strip()])}
                            </ul>
                        </div>
                    """, unsafe_allow_html=True)

            # Display each section
            display_section(col3, "Contact Information", section_breakdown["contact_information"])
            display_section(col4, "Objective Summary", section_breakdown["objective_summary"])
            display_section(col5, "Work Experience", section_breakdown["work_experience"])
            display_section(col6, "Education", section_breakdown["education"])
            display_section(col7, "Skills", section_breakdown["skills"])
            display_section(col8, "Additional Sections", section_breakdown["additional_sections"])
            
            st.divider()
            
            st.markdown(f"""<h2 style='text-align: center;'>
                        Suggestions
                        </h2>""", unsafe_allow_html=True)
            
            col9, col10 = st.columns(2)
            skill_suggestion = response["keyword_optimization"]["missing_keywords"]
            formatting_suggestion = response["formatting_suggestions"]
            with col9:
                st.markdown(f"""
                            <div class='content-box'>
                                <div class='section-header'>Skills</div>
                                <div class="pill-container">
                                    {''.join([f'<div class="pill">{skill}</div>' for skill in skill_suggestion])}
                                </div>                                
                            </div>""", unsafe_allow_html=True)
            display_section(col10, "Formatting Suggestions", formatting_suggestion)
            
            
        st.divider()
