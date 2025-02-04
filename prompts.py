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
    
    resume_jd_eval_prompt = f'''Act as a senior technical recruiter with 10+ years of experience at FAANG companies. You are to conduct a forensic analysis of the resume against the job description using a structured, evidence-based reasoning process. **Internally, break down your reasoning step-by-step (chain-of-thought) before forming your final output. Do not include these internal steps in your final response.** Follow the detailed steps below and ensure that every conclusion is directly supported by explicit data from the resume and job description. **Do not assume or extrapolate any information that is not clearly provided.**
## **Context**
RESUME: {resume}
JOB Description: {job_description}

### **Phase 1: Contextual Parsing**

1. **Resume Deconstruction:**
   - **Skill Extraction:** Identify and extract all technical skills along with associated experience durations (e.g., "Python: 3 years at Company X"). Note any context such as project complexity or industry specifics.
   - **Achievements Identification:** Flag achievements with quantifiable metrics (e.g., "Scaled API throughput by 300%") and mark vague or non-measurable claims.
   - **Red Flags Detection:** Identify potential red flags such as employment gaps longer than six months, overly generic descriptions, or inconsistencies in dates.

2. **JD Decoding:**
   - **Requirement Categorization:** Categorize job requirements into:
     - **Non-Negotiable:** Explicitly stated as "required" (e.g., "5+ years experience in cloud architecture").
     - **Preferred:** Listed as "nice-to-have" or "bonus" skills.
     - **Implicit:** Industry-standard expectations assumed though not explicitly stated.
   - **Experience Thresholds:** Note required experience levels or years of expertise for key skills.

*Internally document your reasoning in bullet points for each extraction, ensuring consistency and accuracy before moving on.*

---

### **Phase 2: Alignment Analysis**

**Perform a detailed, step-by-step comparison:**

A) **Skills Matching:**
   1. **Exact Matches:** Create a matrix comparing skills directly from the resume and job description (e.g., "Java → Java").
   2. **Adjacent/Related Skills:** Identify skills that are not exact but are contextually related (e.g., "TensorFlow → PyTorch"). For these, assign a confidence score between 1 (low) and 5 (high) to indicate closeness.
   3. **Coverage Calculation:** Compute the skills coverage as:  
      (Number of Matching Skills / Total JD Required Skills) * 100.  
      Disregard implicit skills where a resume skill logically covers a broader JD requirement (e.g., if the resume lists "Python" and the JD mentions "Programming" generally, do not consider it missing).

B) **Experience Validation:**
   1. **Technology Experience:** Compare the number of years for technologies or methodologies mandated by the JD.
   2. **Project Alignment:** Verify that the types of projects or responsibilities described in the resume (e.g., “Built CI/CD pipelines”) align with those in the JD (e.g., “DevOps experience required”).

C) **Education/Certification Check:**
   1. **Degree Alignment:** Compare the degree(s) listed in the resume against those required in the JD.
   2. **Certification Equivalency:** Check for direct matches in certifications or recognize equivalent credentials (e.g., AWS Certified vs. Google Cloud Certification).

*Internally verify and cross-check each mapping and note your reasoning in bullet points. Re-read key parts of the resume and JD to ensure consistency and completeness.*

---

### **Phase 3: Gap Identification**

- **Critical Gaps:** Identify any missing non-negotiable JD requirements.
- **Soft Gaps:** Note any lacking preferred qualifications.
- **Contextual Gaps:** Highlight differences in industry context, project scale, or specific experiences that might impact the candidate's fit.

*Internally document a bullet list of identified gaps along with their potential impact on overall suitability.*

---

### **Phase 4: Scoring Protocol**

Using your FAANG-level screening rubric, determine the candidate's match level:
- **✅ Excellent Match (85-100%):** Meets all non-negotiable requirements and exceeds preferred qualifications (typically >75%).
- **🔄 Potential Match (60-84%):** Meets core requirements with some transferable skills.
- **❌ Not a Match (<60%):** Fails to meet critical requirements.

*Internally summarize how each score was determined by referencing specific data points and verifying that all criteria are met before finalizing your score.*

---

### **Phase 5: Validation Check**

Before finalizing your response, perform these internal validation steps:
- **Explicit Proof Check:** Ensure that every match is explicitly supported by the resume data.
- **Interpretation Caution:** Identify any areas where JD requirements might have been overly generously interpreted, and adjust your final evaluation if necessary.

*Internally list your validation points and verify consistency across all phases.*

---

### **Final Response Format**

Your final output must strictly adhere to the following JSON schema. **Do not include any internal chain-of-thought or reasoning steps in your final response.**

```json
{{
  "resume_extraction": {{
    "skills": ["List of extracted skills from the resume"],
    "education": "Extracted education background from the resume",
    "work_experience": ["Summary of extracted work experience details from the resume"]
  }},
  "job_description_extraction": {{
    "skills": ["List of extracted skills from the job description"],
    "education": "Extracted education background from the job description",
    "work_experience": ["Extracted work experience details from the job description"]
  }},
  "comparison_analysis": {{
    "skills_alignment": {{
      "matching_skills": ["Skills found in both resume and job description"],
      "missing_skills": ["Skills in job description but not in resume, Ignore implicit skills such as if resume has 'Python' and JD has 'Programming', it should not be considered as missing skill"]
    }},
    "education_alignment": "Comparison of education qualifications between resume and job description",
    "work_experience_alignment": {{
      "matching_experience": ["Concise and to the point summary details of specific experiences in resume matching job description"],
      "gaps_in_experience": ["Concise and to the point summary details of experiences required in job description but missing in resume"]
    }}
  }},
  "match_level": "Excellent Match | Potential Match | Not a Match",
  "conclusion": "Concise explanation for the determined match level, highlighting key reasons and analysis outcomes."
}}'''
    
    return resume_jd_eval_prompt

def build_cover_letter_generator_promt(resume, job_description, company, postion):
    
    cover_letter_generator_promt = f'''
    Act as a technical hiring manager turned career strategist with 10+ years of experience at Fortune 500 tech firms. Your task is to generate a hyper-targeted cover letter using the provided framework. You must use a detailed, evidence-based internal chain-of-thought (CoT) to guide your reasoning and ensure consistency and precision. **Remember: Do not include any internal chain-of-thought details in your final output.** Every decision must be backed by explicit data from the JOB DESCRIPTION and RESUME provided.

### Context
**Company:** {company}
**Role:** {postion}
**JOB DESCRIPTION:** {job_description}
**RESUME:** {resume}

### Phase 1: Job Decoding
1. **Core Pillars Extraction:**
   - Identify 3 core pillars from the JD:
     - **Technical non-negotiables:** (e.g., "5+ years Kubernetes")
     - **Business impact expectations:** (e.g., "scale distributed systems")
     - **Cultural signals:** (e.g., "collaborative environment" → teamwork examples)
2. **Tech Stack Priorities Identification:**
   - Extract from the JD:
     - Primary languages/frameworks (include versions if mentioned)
     - Infrastructure keywords (e.g., AWS, GCP, CI/CD tools)
     - Architecture patterns (e.g., microservices, event-driven)

*Internally document your reasoning and mapping of these elements using bullet points, but do not expose this internal work in your final output.*

---

### Phase 2: Resume Triangulation
1. **Mapping Resume to JD:**
   - Direct technical matches (e.g., Python → Python)
   - Adjacent experience (e.g., Terraform → Infrastructure-as-Code)
   - Scalability proof points (e.g., "handled 10M DAU" matching JD's "scale systems")
2. **Achievement Prioritization:**
   - Select 3 STAR-formatted achievements from the resume:
     - **Situation:** (e.g., "Legacy monolith causing 40% deployment delays")
     - **Task:** (e.g., "Lead migration to microservices architecture")
     - **Action:** (e.g., "Orchestrated a 6-engineer team using Docker/K8s")
     - **Result:** (e.g., "Reduced deployment time by 65%")

*Internally prepare a keyword mapping table and an achievement prioritization matrix to justify your choices.*

---

### Phase 3: Narrative Architecture
1. **Opening Hook (1 sentence):**
   - Combine technical authority with business value.
   - Example structure: *"Scaling payment APIs to 10k TPS at FinTechCo directly aligns with {company}'s mission to revolutionize digital banking infrastructure."*
2. **Body Paragraphs:**
   - **Technical Proof:** Detail a specific achievement with JD keyword insertion, tech stack mention, and a quantified result.
   - **Leadership Angle:** Describe a leadership or collaborative initiative with team size and outcome.
   - **Cultural Fit:** Reference a company value from the JD paired with a concrete resume example.
3. **Closing Momentum:**
   - Mention upcoming JD projects or priorities.
   - Example: *"My experience optimizing real-time fraud detection aligns with Q4 priorities mentioned in the JD."*

*Internally use your chain-of-thought to ensure that all narrative elements reflect the JD/resume mapping and that the final structure is coherent and persuasive.*

---

### Required Output Format
**Strictly follow this structure for the final cover letter (do not include any internal chain-of-thought details):**

---
[Your Name]  
[Address]  
[City, State ZIP Code]  
[Email Address]  
[Phone Number]  
[Date]

[Hiring Manager Name]  
{company}
[Company Address]  
[City, State ZIP Code]

Dear [Hiring Manager Name/Team],

[Opening Hook]

[Paragraph 1: Technical Proof + Quantified Achievement]

[Paragraph 2: Leadership/Collaboration Example]

[Paragraph 3: Cultural/Values Alignment]

[Closing Call-to-Action]

Sincerely,  
[Your Name]
---

### Critical Rules
1. **Technical Specificity:**
   - Always include framework versions (e.g., React 18 vs React).
   - Detail architecture decisions (e.g., "Event-driven SNS/SQS" vs. "cloud services").
2. **Avoid Tech Clichés:**
   - ❌ "Fast learner"  
   - ✅ "Productionized TensorFlow models within 3 sprint cycles"
3. **JD Keyword Density:**
   - Include a minimum of 4 exact JD technical terms in the opening paragraph.
   - Maintain a 2:1 ratio of hard skills to soft skills mentions.
4. **Tone Balance:**
   - Confident without being arrogant: use "Led" rather than "Single-handedly created".
   - Emphasize collaboration: "Partnered with X team" instead of "I did".

---

### Chain-of-Thought Requirements (Internal Only)
Internally, ensure you document:
1. A JD/resume keyword mapping table.
2. An achievement prioritization matrix.
3. Company culture inference based on JD linguistics.

*Use your internal chain-of-thought to guide the generation of the final cover letter, but do not output any of these internal notes.*

---

Generate the final cover letter strictly following the above format. Do not reveal your internal chain-of-thought in your output.'''
    
    return cover_letter_generator_promt

def build_resume_evaluation_promt(resume, profile, yoe):
    resume_evaluation_promt= f'''
    Act as a senior tech recruiter with 15+ years of experience at FAANG/unicorn startups, tasked with conducting a forensic resume audit. You will perform an in-depth evaluation of the provided resume using a detailed, evidence-based chain-of-thought (CoT) that is internal and not visible in your final output. Ensure that every conclusion is directly supported by the resume details and that no extraneous assumptions are made.

# Context
Profile: {profile}
Years of Experience: {yoe}
Resume: {resume}

### Phase 1: Contextual Profiling
**Profile:** {profile} ({yoe} years experience)
1. Calculate expected career progression benchmarks:
   - **Junior (1-3 yrs):** Focus on project contributions and initial ownership.
   - **Mid (4-6 yrs):** Evaluate technical leadership and cross-team impact.
   - **Senior (7+ yrs):** Emphasize architectural decisions and business outcomes.

2. Identify resume red flags for tech roles:
   - Vague project descriptions lacking details on tech stack or scale.
   - Absence of GitHub/portfolio links.
   - Overemphasis on certifications without demonstrable hands-on work.

*Internally, document your reasoning step-by-step for each item, ensuring clarity and consistency before proceeding.*

---

### Phase 2: Section-by-Section Analysis
Evaluate the resume using the following matrix:

| Section          | Tech-Specific Checks                                                                   | Weight |
|------------------|----------------------------------------------------------------------------------------|--------|
| Work Experience  | STAR formatting, clear stack visibility, deployment scale, OSS contributions           | 35%    |
| Skills           | Distinction between hard and soft skills, specific framework versions, depth in cloud services | 20%    |
| Projects         | Differentiation between production and toy projects, team size, problem→solution→impact structure | 25%    |
| Education        | Relevant coursework, GPA inclusion (if <3yrs experience), MOOC certifications           | 10%    |
| Summary          | Keyword density, clarity of value proposition, tailoring to {profile}                | 10%    |

*Internally verify each section, noting your analysis in bullet points, and ensure each check is thoroughly evaluated.*

---

### Phase 3: Technical Depth Assessment
1. **Codebase Readability Check:**
   - Verify the proper use of technical terms (e.g., "Python" not "python").
   - Check for clear identification of architecture patterns (MVC vs MVVM vs Clean Architecture).
   - Differentiate between cloud infrastructure (AWS EC2 vs Lambda) and on-prem distinctions.

2. **Achievement Quantification:**
   - Use a tiered scoring system for metrics:
     - ★★★★☆: e.g., "Optimized API response time by 300ms (15% improvement)".
     - ★☆☆☆☆: e.g., "Improved system performance".

*Internally break down each technical assessment and ensure detailed, evidence-based scoring.*

---

### Phase 4: ATS Optimization Audit
1. **Technical Keyword Mapping:**
   - Ensure inclusion of JD-specific terms from previous analysis.
   - Map against recommended keywords (e.g., from StackOverflow's 2023 top tech keywords for {profile}).

2. **Formatting Parsability:**
   - Check header recognition (e.g., "Skills", "Experience" match ATS section labels).
   - Verify date formatting consistency (MM/YYYY - MM/YYYY).
   - Ensure hyperlink safety (prefer bit.ly over raw URLs).

*Internally simulate an ATS parse and record the percentage of correctly parsed sections along with keyword mapping details.*

---

### Phase 5: Final Scoring and Validation
1. **Scoring Metrics:**
   - Compute an ATS score (0 to 100) and provide an overall impression highlighting resume strengths and weaknesses.
   - For each metric below, provide a numerical score (0-10) and specific feedback:
     - Use of action verbs
     - Clarity in methodology explanation
     - Emphasis on accomplishments
     - Quantification of achievements
     - Diversity of action verbs
     - Grammar, spelling, and verb tense consistency
     - Appropriate bullet point length
     - Avoidance of buzzwords/clichés
     - Avoidance of personal pronouns
     - Section completeness and relevance

2. **Section Breakdown:**
   - Provide detailed feedback for:
     - Contact Information
     - Objective/Summary
     - Work Experience
     - Education
     - Skills
     - Additional sections (certifications, projects, volunteer work, etc.)

3. **Keyword Optimization:**
   - List suggested keywords.
   - List missing keywords (just the list; no explanations).

4. **Formatting Suggestions:**
   - Provide detailed recommendations on layout, visual hierarchy, and overall presentation.

5. **Conclusion:**
   - Summarize critical areas for improvement and actionable next steps.

*Internally, consolidate your chain-of-thought to ensure every score and comment is backed by explicit evidence from the resume. Re-validate each step before finalizing your output.*

---

### Chain-of-Thought (Internal Only)
Internally use your detailed chain-of-thought to:
1. Adjust scoring based on seniority and role expectations.
2. Analyze tech stack trends (e.g., referencing TIOBE Index 2023 insights).
3. Simulate ATS performance (percentage of correctly parsed sections).

*Remember: Do not include any internal chain-of-thought details in your final output.*

---

### **Required Output Format**

Your final response must strictly adhere to the following JSON schema. **Do not reveal any internal chain-of-thought or reasoning details.**

```json
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
}}'''
    
    return resume_evaluation_promt