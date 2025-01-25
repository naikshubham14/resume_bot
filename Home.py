import streamlit as st
import helper
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import textwrap
import io

@st.cache_data
def generate_wordcloud_image(job_description):
    st.image(helper.generate_wordcloud(job_description), use_column_width=True)
    
def main():
    st.set_page_config(
        page_title="RESUMAGIC",
        layout="wide",
        page_icon=":material/description:"
    )

    st.markdown(
    """
    <h1 style="text-align: center; color: #4CAF50;">RESUMAGIC 2.0 📄🤖</h1>
    <h3 style="text-align: center; color: #FFC107;">Your one-stop solution for everything you need before you hit that APPLY button</h3>
    <p style="text-align: center; color: #9E9E9E; font-size: 16px;">
        Here are all the tools available at your disposal:
    </p>

    <ul style="font-size: 16px; line-height: 1.8; list-style-type: none; padding-left: 0;">
        <li style="margin-bottom: 10px;">
            <b style="color: #FF5722;">☝️ Resume - JD Comparison Tool 🧠:</b> 
            Break down how well your resume aligns with the job you're targeting, scoring your compatibility.
        </li>
        <li style="margin-bottom: 10px;">
            <b style="color: #2196F3;">✌️ Resume Analysis Tool ✍️:</b> 
            Not just a score—real insights on how to make your resume stand out.
        </li>
        <li style="margin-bottom: 10px;">
            <b style="color: #8E24AA;">👌 Cover Letter Generation Tool 📄:</b> 
            Get a tailored cover letter that highlights your strengths based on the job you're applying for.
        </li>
    </ul>
    """,
    unsafe_allow_html=True
)
    
    st.text(" ")
    st.markdown(
    """
    <div style="text-align: center; margin-top: 20px;">
        <p style="font-size: 18px; font-weight: bold;">
            If you like the project or have suggestions, feel free to reach out to me here ➡️
        </p>
        <a href="https://www.linkedin.com/in/shubham-rajan-naik/" target="_blank" 
           style="background-color: #0A66C2; color: white; text-decoration: none; 
                  padding: 10px 20px; border-radius: 5px; font-size: 16px; font-weight: bold;">
            LinkedIn
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

    

if __name__ == "__main__":
    helper.ensure_nltk_resources_download()
    main()