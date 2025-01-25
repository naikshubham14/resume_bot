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
    Adhere to the following JSON schema for your response:
    
    {{
  "resume_extraction": {{
    "skills": ["List of extracted skills from the resume"],
    "education": "Extracted education background from the resume",
    "work_experience": ["Extracted work experience details from the resume"]
  }},
  "job_description_extraction": {{
    "skills": ["List of extracted skills from the job description"],
    "education": "Extracted education background from the job description",
    "work_experience": ["Extracted work experience details from the job description"]
  }},
  "comparison_analysis": {{
    "skills_alignment": {{
      "matching_skills": ["Skills found in both resume and job description"],
      "missing_skills": ["Skills in job description but not in resume"]
    }},
    "education_alignment": "Comparison of education qualifications between resume and job description",
    "work_experience_alignment": {{
      "matching_experience": ["Specific experiences in resume matching job description"],
      "gaps_in_experience": ["Experiences required in job description but missing in resume"]
    }}
  }},
  "match_level": "Excellent Match | Potential Match | Not a Match",
  "conclusion": "Brief explanation for the determined match level, highlighting key reasons and analysis outcomes."
}}

    ## Instructions
    Please ensure to:
    - Maintain objectivity and clarity in the analysis.
    - Highlight specific examples or sections from both the resume and job description during the comparison.
    - Conclude with a rational explanation that supports the match determination, ensuring it is succinct yet informative.'''
    
    return resume_jd_eval_prompt


def build_cover_letter_generator_promt(resume, job_description, company, postion):
    
    cover_letter_generator_promt = f'''Act as a world-class professional career advisor specializing in resume and cover letter writing. Given the following context, criteria, and instructions, create a tailored cover letter for a job application.

    ## Context
    A job description will be provided detailing specific skills, qualifications, and experiences desired by the employer. Additionally, a current resume will be shared, which includes relevant work experiences, skills, and accomplishments that align with the job description.

    \n Resume: {resume} \n 
    \n Job description: {job_description} \n
    \n Company: {company} \n
    \n Position Title: {postion} \n

    ## Approach
    Analyze the job description to identify key qualifications, required skills, and preferred experiences. Review the resume to extract relevant information that demonstrates how the applicant’s skills and experiences match the job requirements. Construct a concise and persuasive cover letter that emphasizes relevant experiences and uses appropriate keywords from the job description without overusing hype words or jargon.

    ## Response Format
    The cover letter should include the following sections: 
    1. A professional greeting
    2. An introduction that states the position being applied for and a brief overview of the applicant's interest in the role
    3. A body section that connects the applicant's experiences from the resume with the responsibilities and qualifications in the job description
    4. A closing paragraph that reiterates interest in the position and includes a call to action for further discussion
    5. A professional closing statement
    6. In your final response do not add any indtroductory or trailing text, you response should include only the content of the cover letter
    
    ## Instructions
    1. Use clear and professional language throughout the letter.
    2. Ensure the cover letter is focused on the job applied for and omits irrelevant information.
    3. Include specific examples from the resume that align with the job description.
    4. Maintain a formal tone and structure suitable for a job application.
    5. Extract contact information from the resume and include it in the cover letter
    6. Dont include any indtroductory or trailing text in your response such as "Here is a tailored cover letter" '''
    
    return cover_letter_generator_promt

def build_resume_evaluation_promt(resume, profile, yoe):
    resume_evaluation_promt= f'''Act as a world-class resume expert specializing in resume best practices and resume optimization. Given the following context, criteria, and instructions, analyze the provided resume and offer constructive feedback to enhance its effectiveness and improve its score.

    ## Context
    This resume belongs to a {profile} with {yoe} years of experience.
    The resume to be analyzed may include various sections such as contact information, objective/summary, work experience, education, skills, and additional sections like certifications or volunteer work. The analysis will focus on clarity, relevance, formatting, keyword optimization, and overall appeal to potential employers.
    Keeping in mind the profile an their years of experience so that the analysis and evaluation is unique and personalized. The
    
    \n Resume: {resume} \n 

    ## Approach
    1. Thoroughly review each section of the resume for completeness and clarity.
    2. Identify any areas lacking relevant details or that do not align with industry standards.
    3. Evaluate the use of action verbs and quantify achievements where possible.
    4. Check for keyword optimization in relation to job descriptions relevant to the applicant's field.
    5. Suggest formatting improvements for better readability and professionalism.

    ## Response Format
    Adhere to the following JSON schema for your response:
    
    {{
  "ats_score": "Numerical score from 0 to 100 indicating ATS compatibility",
  "overall_impression": "Brief summary of resume strengths and weaknesses",
  "metrics_evaluation": {{
    "use_action_verbs": {{
      "score": "Numerical score from 0 to 10 for this metric",
      "comments": "Specific feedback on the use of action verbs in the resume"
    }},
    "methodology_explanation": {{
      "score": "Numerical score from 0 to 10 for this metric",
      "comments": "Feedback on the clarity and relevance of methodology explanations"
    }},
    "emphasize_accomplishment": {{
      "score": "Numerical score from 0 to 10 for this metric",
      "comments": "Feedback on how well accomplishments are highlighted"
    }},
    "quantification_of_achievements": {{
      "score": "Numerical score from 0 to 10 for this metric",
      "comments": "Feedback on the use of numbers or measurable outcomes to quantify achievements"
    }},
    "use_diverse_action_verbs": {{
      "score": "Numerical score from 0 to 10 for this metric",
      "comments": "Feedback on the variety of action verbs used throughout the resume"
    }},
    "spelling_and_verb_tenses": {{
      "score": "Numerical score from 0 to 10 for this metric",
      "comments": "Feedback on grammar, spelling, and consistency in verb tenses"
    }},
    "appropriate_bullet_length": {{
      "score": "Numerical score from 0 to 10 for this metric",
      "comments": "Feedback on the length and readability of bullet points"
    }},
    "avoidance_of_buzzwords_cliches": {{
      "score": "Numerical score from 0 to 10 for this metric",
      "comments": "Feedback on the use of meaningful, specific language instead of generic buzzwords or clichés"
    }},
    "avoid_personal_pronouns": {{
      "score": "Numerical score from 0 to 10 for this metric",
      "comments": "Feedback on the avoidance of personal pronouns for a professional tone"
    }},
    "section_completeness_relevance": {{
      "score": "Numerical score from 0 to 10 for this metric",
      "comments": "Feedback on whether all sections are complete and relevant to the job description"
    }}
  }},
  "section_breakdown": {{
    "contact_information": "Feedback on the accuracy and completeness of contact details",
    "objective_summary": "Feedback on the relevance and clarity of the objective or summary section",
    "work_experience": "Detailed feedback on work experience, highlighting strengths and areas for improvement",
    "education": "Feedback on the education section, including its relevance and presentation",
    "skills": "Evaluation of the skills section, with suggestions for improvement",
    "additional_sections": "Feedback on sections like certifications, projects, or volunteer work"
  }},
  "keyword_optimization": {{
    "suggested_keywords": ["List of recommended keywords"],
    "missing_keywords": ["List of keywords that are relevant but missing from the resume, provide just the list, dont add any explaination or example"]
  }},
  "formatting_suggestions": "Detailed recommendations for layout, visual hierarchy, and overall presentation",
  "conclusion": "Final thoughts summarizing critical areas for improvement and actionable next steps"
}}

    ## Instructions
    - Maintain a professional tone throughout the analysis.
    - Ensure that all feedback is actionable and specific.
    - Focus on evidence-based best practices in resume crafting.
    - Highlight examples or alternatives where applicable, providing options for improvement.'''
    
    return resume_evaluation_promt