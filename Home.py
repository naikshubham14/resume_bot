import streamlit as st
import helper
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import textwrap
import io

@st.cache_data
def generate_wordcloud_image(job_description):
    st.image(helper.generate_wordcloud(job_description), use_column_width=True)

@st.cache_data
def generate_cover_letter(cover_letter_generator_prompt):
    buffer = io.BytesIO()
    content = helper.llm_call(cover_letter_generator_prompt)
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    # Set the font and size
    c.setFont("Helvetica", 12)
    # Define the starting position
    x = 70
    y = height - 100
    max_width = width - 70
    wrapped_content = textwrap.wrap(content, max_width)
    # Write each line to the PDF
    for line in wrapped_content:
        c.drawString(x, y, line)
        y -= 15  # Move to the next line
        # Check if we need to create a new page
        if y < 40:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = height - 100
    # Save the PDF file
    c.save()
    buffer.seek(0)
    return buffer    

    
def main():
    st.set_page_config(
        page_title="RESUMAGIC",
        layout="wide",
        page_icon=":material/description:"
    )

    st.markdown(
    """
    <h1 style="text-align: center; color: #4CAF50;">RESUMAGIC BOT 📄🤖</h1>
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
    main()