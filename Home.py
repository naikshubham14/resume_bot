import streamlit as st
import helper
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

    # Add Bootstrap CSS
    st.markdown("""
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            .card { 
                transition: transform 0.2s; 
                min-height: 300px;
                background-color: #f8f9fa;
            }
            .card:hover { transform: translateY(-5px); }
            .card-text { color: #212529; }
            .card-title { color: #000; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(
    """
    <div class="container">
        <h1 class="text-center text-success mb-4">RESUMAGIC 2.0 📄🤖</h1>
        <h3 class="text-center text-warning mb-4">Your one-stop solution for everything you need before you hit that APPLY button</h3>
        <p class="text-center text-muted mb-5">Here are all the tools available at your disposal:</p>
    </div>
    """,
    unsafe_allow_html=True
)
    st.markdown(
        """<div class="row justify-content-center">
            <div class="col-md-4 mb-4">
                <div class="card shadow">
                    <div class="card-body d-flex flex-column justify-content-center">
                        <h5 class="card-title text-center">☝️ Resume - JD Comparison Tool 🧠</h5>
                        <p class="card-text text-center">Break down how well your resume aligns with the job you're targeting, scoring your compatibility.</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="card shadow">
                    <div class="card-body d-flex flex-column justify-content-center">
                        <h5 class="card-title text-center">✌️ Resume Analysis Tool ✍️</h5>
                        <p class="card-text text-center">Not just a score—real insights on how to make your resume stand out.</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="card shadow">
                    <div class="card-body d-flex flex-column justify-content-center">
                        <h5 class="card-title text-center">👌 Cover Letter Generation Tool 📄</h5>
                        <p class="card-text text-center">Get a tailored cover letter that highlights your strengths based on the job you're applying for.</p>
                    </div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True    )
    
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
    #helper.ensure_nltk_resources_download()
    main()