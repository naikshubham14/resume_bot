import re
import unicodedata
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords, wordnet
from io import BytesIO
import google.generativeai as genai
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv, find_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from unidecode import unidecode
import fitz

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
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    # Create the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    )

    chat_session = model.start_chat(
    history=[
    ]
    )

    response = chat_session.send_message(prompt)
    return response.text

def read_pdf(pdf):
    """
    This function reads a PDF file and extracts its text content.

    Parameters:
    pdf (str): The path to the PDF file.

    Returns:
    str: The extracted text from the PDF file.
    """

    text = ""
    # Open the PDF from the byte stream
    with fitz.open(stream=pdf.read(), filetype="pdf") as doc:
        output = []
        for page in doc:
            output += page.get_text("blocks")  # Extract blocks of text
        previous_block_id = 0  # Set a variable to mark the block id
        for block in output:
            if block[6] == 0:  # We only take the text blocks
                if previous_block_id != block[5]:  # Compare the block number
                    plain_text = unidecode(block[4])  # Clean the text
                    text += plain_text
                    text += '\n'
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

def ensure_nltk_resources_download():
    """
    This function checks if required NLTK resources are available and downloads them if necessary.
    """
    # List of NLTK resources to check and download
    resources = ['wordnet', 'stopwords', 'punkt', 'averaged_perceptron_tagger', 'omw']
    
    for resource in resources:
        try:
            # Try accessing a sample of the resource
            if resource == 'stopwords':
                stopwords.words('english')  # Check stopwords
            elif resource == 'wordnet':
                wordnet.synsets('example')  # Check wordnet
            else:
                # For other resources, we can just use nltk.data.find() to check
                nltk.data.find(f"corpora/{resource}")
        except LookupError:
            # If the resource is not found, download it
            print(f"{resource} data not found. Downloading...")
            nltk.download(resource)
        else:
            print(f"{resource} data is already available.")
