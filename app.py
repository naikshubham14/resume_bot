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

    st.title("RESUMAGIC BOT 📄🤖")
    st.subheader("Your one stop solution for everything you need before you hit that APPLY button")
    st.text("Here are a few tips to get the most out of resumagic")
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

    with col1:
        # Add a file uploader
        st.subheader("Upload your Resume")
        resume = st.file_uploader("Upload Resume",accept_multiple_files=False,type=("pdf", "txt"), key="resume", label_visibility="hidden")
        st.divider()
        st.subheader("Upload your Cover Letter")
        cover_letter = st.file_uploader("Cover Letter",accept_multiple_files=False,type=("pdf", "txt"), key="cover_letter", label_visibility="hidden")

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
    if(cover_letter is None):
        st.warning("Please upload Cover Letter for best results")
            
    if(st.button("Generate", type="primary", disabled=resume is None or len(job_description) == 0, use_container_width=True, icon=":material/send:")):
        st.divider()
        resume_content = helper.read_file(resume)
        cover_letter_content = ""
        if cover_letter is not None:
            cover_letter_content = helper.read_file(cover_letter)
        resume_jd_eval_prompt = helper.build_resume_jd_eval_prompt(resume_content, job_description)
        resume_eval_prompt = helper.build_resume_evaluation_promt(resume_content)
        cover_letter_generator_prompt = helper.build_cover_letter_generator_promt(resume_content, job_description, cover_letter_content)
        col3, col4 = st.columns(2)
        with col3:
            with st.spinner("Mathcing the job description"):
                jd_fit_eval = helper.llm_call(resume_jd_eval_prompt)
                st.subheader("Job fit analysis")
                st.write(jd_fit_eval)   
            st.divider()
        with col4:
            with st.spinner("Evaluating your resume"):
                st.subheader("Resume analysis")
                st.write(helper.llm_call(resume_eval_prompt))
                
        col5, col6 = st.columns(2)
        with col5:
            with st.spinner("Generating wordcloud"):
                st.subheader("Required skills wordcloud as per the job description")
                generate_wordcloud_image(job_description)
        with col6:
            with st.spinner("Generating Cover Letter"):
                cover_letter = helper.llm_call(cover_letter_generator_prompt)
                st.divider()
                with open("output.txt", "w") as file:
                # Write the string to the file
                    file.write(cover_letter)
                    st.download_button(
                        label="Download your custom cover letter",
                        data=cover_letter,
                        file_name="cover_letter.txt",
                        mime="text/txt",
                        icon=":material/download:"
                    )
    

if __name__ == "__main__":
    main()