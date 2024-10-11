import re
import unicodedata
from wordcloud import WordCloud
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
from io import BytesIO
from together import Together
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv, find_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
nltk.download('stopwords')
nltk.download('wordnet')

def basic_clean(string):
    '''
    This function takes in a string and
    returns the string normalized.
    '''
    string = unicodedata.normalize('NFKD', string)\
             .encode('ascii', 'ignore')\
             .decode('utf-8', 'ignore')
    string = re.sub(r'[^\w\s]', '', string).lower()
    return string

def tokenize(string):
    '''
    This function takes in a string and
    returns a tokenized string.
    '''
    # Create tokenizer.
    tokenizer = nltk.tokenize.ToktokTokenizer()
    # Use tokenizer
    string = tokenizer.tokenize(string, return_str = True)
    return string

def stem(string):
    '''
    This function takes in a string and
    returns a string with words stemmed.
    '''
    # Create porter stemmer.
    ps = nltk.porter.PorterStemmer()
    # Use the stemmer to stem each word in the list of words we created by using split.
    stems = [ps.stem(word) for word in string.split()]
    # Join our lists of words into a string again and assign to a variable.
    string = ' '.join(stems)
    return string

def lemmatize(string):
    '''
    This function takes in string for and
    returns a string with words lemmatized.
    '''
    # Create the lemmatizer.
    wnl = nltk.stem.WordNetLemmatizer()
    # Use the lemmatizer on each word in the list of words we created by using split.
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    # Join our list of words into a string again and assign to a variable.
    string = ' '.join(lemmas)
    
    return string

def remove_stopwords(string, extra_words = [], exclude_words = []):
    '''
    This function takes in a string, optional extra_words and exclude_words parameters
    with default empty lists and returns a string.
    '''
    # Create stopword_list.
    stopword_list = stopwords.words('english')
    # Remove 'exclude_words' from stopword_list to keep these in my text.
    stopword_list = set(stopword_list) - set(exclude_words)
    # Add in 'extra_words' to stopword_list.
    stopword_list = stopword_list.union(set(extra_words))
    # Split words in string.
    words = string.split()
    # Create a list of words from my string with stopwords removed and assign to variable.
    filtered_words = [word for word in words if word not in stopword_list]
    # Join words in the list back into strings and assign to a variable.
    string_without_stopwords = ' '.join(filtered_words)
    
    return string_without_stopwords

def clean(text):
    '''
    This function combines the above steps and added extra stop words to clean text
    '''
    return remove_stopwords(lemmatize(basic_clean(text)))

def generate_wordcloud(text):
    """
    Generate a wordcloud image from the given text.

    Parameters:
    text (str): The text from which the wordcloud will be generated.

    Returns:
    BytesIO: A BytesIO object containing the generated wordcloud image in PNG format.
    """
    clean_jd = clean(text)  # Clean the text using the clean function
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(clean_jd)  # Generate wordcloud
    wordcloud_image = wordcloud.to_image()  # Convert wordcloud to image
    buffer = BytesIO()  # Create a BytesIO object to store the image
    wordcloud_image.save(buffer, format="PNG")  # Save the image to the BytesIO object
    buffer.seek(0)  # Move the file pointer to the beginning of the BytesIO object
    return buffer  # Return the BytesIO object containing the wordcloud image

def read_file(file):
    """
    This function reads a file and returns its content as a string.
    It supports reading both PDF and TXT files.

    Parameters:
    file (FileIO): The file to be read. The file object must be opened in binary mode ('rb') for PDF files.

    Returns:
    str: The content of the file as a string. For PDF files, the content is obtained using the read_pdf function
    from RAG_util module. For TXT files, the content is read directly.
    """
    file_extension = file.name.split('.')[-1].lower()
    if file_extension == 'pdf':
        return read_pdf(file)
    elif file_extension == 'txt':
        return file.read().decode("utf-8")
    
def build_resume_jd_eval_prompt(resume, job_description):
    """
    This function generates a prompt for a career guidance expert to evaluate a resume in relation to a job description.
    The prompt includes a system message, context, action approach, resume and job description, and instructions.

    Parameters:
    resume (str): The content of the resume as a string. Default value is an empty string.
    job_description (str): The content of the job description as a string. Default value is an empty string.

    Returns:
    str: The generated prompt as a string.
    """
    
    resume_jd_eval_prompt = f'''Act as a world-class career guidance expert specializing in resume evaluation. Given the following context, criteria, and instructions, perform a detailed analysis of a resume in relation to a job description.
    ## Context
    A resume and a job description will be provided, containing detailed information regarding the candidate's skills, educational background, and work experience, as well as the requirements and qualifications sought for the job position.
    
    \n Resume: {resume} \n 
    \n Job description: {job_description} \n
    
    ## Approach
    1. Extract the skills, education background, and work experience sections from the provided resume.
    2. Extract the skills, education background, and work experience sections from the provided job description.
    3. Analyze and compare the extracted results from both the resume and job description, with a focus on work experience and skills. Assess the compatibility of the candidate’s qualifications with the job requirements.
    4. Determine the match level based on the comparison results, categorizing the match as "Excellent Match", "Potential Match", or "Not a Match".
    5. Provide a brief explanation for the conclusion, highlighting the reasons behind the match decision based on the analysis.

    ## Response Format
    The response should be structured as follows:
    1. Summary of the extracted skills, education background, and work experience from both the resume and job description.
    2. Comparison analysis emphasizing work experience and skills alignment.
    3. Match level determination (Excellent Match, Potential Match, Not a Match).
    4. Brief explanation for the matching conclusion.

    ## Instructions
    Please ensure to:
    - Maintain objectivity and clarity in the analysis.
    - Highlight specific examples or sections from both the resume and job description during the comparison.
    - Conclude with a rational explanation that supports the match determination, ensuring it is succinct yet informative.'''
    
    return resume_jd_eval_prompt


def build_cover_letter_generator_promt(resume, job_description, cover_letter=""):
    
    cover_letter_generator_promt = f'''Act as a world-class professional career advisor specializing in resume and cover letter writing. Given the following context, criteria, and instructions, create a tailored cover letter for a job application.

    ## Context
    A job description will be provided detailing specific skills, qualifications, and experiences desired by the employer. Additionally, a current resume will be shared, which includes relevant work experiences, skills, and accomplishments that align with the job description.

    \n Resume: {resume} \n 
    \n Job description: {job_description} \n
    \n Cover Letter: {cover_letter} \n

    ## Approach
    Analyze the job description to identify key qualifications, required skills, and preferred experiences. Review the resume to extract relevant information that demonstrates how the applicant’s skills and experiences match the job requirements. Construct a concise and persuasive cover letter that emphasizes relevant experiences and uses appropriate keywords from the job description without overusing hype words or jargon.

    ## Response Format
    The cover letter should include the following sections: 
    1. A professional greeting
    2. An introduction that states the position being applied for and a brief overview of the applicant's interest in the role
    3. A body section that connects the applicant's experiences from the resume with the responsibilities and qualifications in the job description
    4. A closing paragraph that reiterates interest in the position and includes a call to action for further discussion
    5. A professional closing statement

    ## Instructions
    1. Use clear and professional language throughout the letter.
    2. Ensure the cover letter is focused on the job applied for and omits irrelevant information.
    3. Include specific examples from the resume that align with the job description.
    4. Maintain a formal tone and structure suitable for a job application.
    5. Extract contact information from the resume and include it in the cover letter
    6. Dont enclude any indtroductory or trailing text in your response such as "Here is a tailored cover letter" '''
    
    return cover_letter_generator_promt

def build_resume_evaluation_promt(resume):
    resume_evaluation_promt= f'''Act as a world-class resume expert specializing in resume best practices and resume optimization. Given the following context, criteria, and instructions, analyze the provided resume and offer constructive feedback to enhance its effectiveness and improve its score.

    ## Context
    The resume to be analyzed may include various sections such as contact information, objective/summary, work experience, education, skills, and additional sections like certifications or volunteer work. The analysis will focus on clarity, relevance, formatting, keyword optimization, and overall appeal to potential employers.

    \n Resume: {resume} \n 

    ## Approach
    1. Thoroughly review each section of the resume for completeness and clarity.
    2. Identify any areas lacking relevant details or that do not align with industry standards.
    3. Evaluate the use of action verbs and quantify achievements where possible.
    4. Check for keyword optimization in relation to job descriptions relevant to the applicant's field.
    5. Suggest formatting improvements for better readability and professionalism.

    ## Response Format
    Provide a detailed analysis of the resume in a structured format:
    1. Overall Impression: A brief summary of the resume's strengths and weaknesses.
    2. Section-by-Section Breakdown: Feedback on each individual section, highlighting areas for improvement.
    3. Keyword Optimization: Specific keywords to include based on industry standards.
    4. Formatting Suggestions: Recommendations for layout adjustments to enhance visual appeal.
    5. Conclusion: Final thoughts and a recap of the most critical improvement points.

    ## Instructions
    - Maintain a professional tone throughout the analysis.
    - Ensure that all feedback is actionable and specific.
    - Focus on evidence-based best practices in resume crafting.
    - Highlight examples or alternatives where applicable, providing options for improvement.'''
    
    return resume_evaluation_promt


def llm_call(prompt):
    """
    This function makes a call to the Together API to generate a response based on the given prompt.
    The function uses the meta-llama/Llama-Vision-Free model for text generation.

    Parameters:
    prompt (str): The input prompt for the text generation.

    Returns:
    None: The function prints the generated response from the Together API.

    Note:
    This function requires the 'together' and 'python-dotenv' libraries to be installed.
    It also requires a valid API key to be set in the environment variable 'TOGETHER_API_KEY'.
    """
    _ = load_dotenv(find_dotenv())
    client = Together(api_key=os.environ.get('TOGETHER_API_KEY'))

    responses = client.chat.completions.create(
        model="meta-llama/Llama-Vision-Free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=1512,
        temperature=0.7,
        top_p=0.7,
        top_k=50,
        repetition_penalty=1,
        stop=["<|eot_id|>","<|eom_id|>"],
        truncate=130560
    )
    return responses.choices[0].message.content

def read_pdf(pdf):
    """
    This function reads a PDF file and extracts its text content.

    Parameters:
    pdf (str): The path to the PDF file.

    Returns:
    str: The extracted text from the PDF file.
    """
    text = ""
    reader = PdfReader(pdf)
    for page in reader.pages:
        text += page.extract_text()
    return text

def create_cover_letter_pdf(cover_letter_content):
    """
    This function generates a PDF file containing the provided cover letter content.

    Parameters:
    cover_letter_content (str): The text content of the cover letter to be included in the PDF.

    Returns:
    None: The function generates a PDF file named "cover_letter.pdf" containing the cover letter content.

    Note:
    This function uses the reportlab library to create the PDF file. The PDF file is saved in the current working directory.
    """
    c = canvas.Canvas("cover_letter.pdf", pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 100, cover_letter_content)
    c.save()