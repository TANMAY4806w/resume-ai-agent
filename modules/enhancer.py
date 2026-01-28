import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# 1. FORCE LOAD THE .ENV FILE
# This tells Python to look for the .env file in the current folder
load_dotenv() 

# 2. DEBUGGING: Check if key exists
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    # This will print to your terminal so you can see the error clearly
    print("❌ ERROR: GEMINI_API_KEY is missing from environment variables.")
    print("Please check that you created a file named '.env' (not .env.txt) and it contains your key.")
else:
    print("✅ API Key found.")

# 3. CONFIGURE THE API
genai.configure(api_key=api_key)

def enhance_resume_content(original_text, job_description, missing_keywords=None):
    """
    Enhances resume content using Gemini AI with intelligent keyword injection.
    
    Args:
        original_text (str): Original resume text
        job_description (str): Target job description
        missing_keywords (list): Keywords missing from original resume (from ATS analysis)
        
    Returns:
        dict: Enhanced resume data with keywords_added and keywords_skipped fields
    """
    # Use the Flash model (Fast & Free)
    model = genai.GenerativeModel('gemini-flash-latest')
    
    # Prepare missing keywords section
    keywords_section = ""
    if missing_keywords and len(missing_keywords) > 0:
        # Filter out common stopwords and generic terms
        stopwords = {'are', 'is', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                    'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
                    'key', 'detail', 'details', 'issues', 'issue', 'closely', 'outputs',
                    'efficient', 'userfacing', 'user', 'facing', 'software', 'thirdparty'}
        
        # Filter keywords: only keep meaningful technical terms (length > 3, not in stopwords)
        filtered_keywords = [
            kw for kw in missing_keywords 
            if len(kw) > 3 and kw.lower() not in stopwords
        ]
        
        # Limit to top 10 most important keywords
        top_keywords = filtered_keywords[:10]
        
        if top_keywords:  # Only add section if we have meaningful keywords
            keywords_section = f"""
    🎯 CRITICAL ATS OPTIMIZATION TASK:
    The following TECHNICAL keywords are MISSING from the resume but present in the job description:
    {', '.join(top_keywords)}
    
    Your task is to NATURALLY incorporate these keywords where truthful and relevant.
    Rules for keyword injection:
    1. Only add TECHNICAL keywords that match the candidate's actual experience (e.g., Python, Docker, AWS, React)
    2. DO NOT add generic words like "efficient", "software", "detail", "issues", "key", "are", etc.
    3. Integrate them naturally into existing bullets or summary (NO keyword stuffing)
    4. Prioritize keywords that fit the candidate's background
    5. If a keyword doesn't fit truthfully, skip it
    6. Track which keywords you added vs skipped
    """
    
    prompt = f"""
    You are an expert ATS Resume Optimization Specialist.
    
    {keywords_section}
    
    TASK:
    1. Extract the name, email, phone, linkedin, github, and website from the resume.
    2. Rewrite the experience bullets to be strong, impact-driven, and ATS-optimized.
    3. If missing keywords were provided, naturally incorporate them where truthful.
    4. Return ONLY a valid JSON object with this exact structure (no markdown formatting):
    {{
        "name": "Full Name",
        "email": "email@example.com",
        "phone": "+1234567890",
        "linkedin": "linkedin-username",
        "github": "github-username",
        "website": "https://portfolio.com",
        "summary": "Professional summary that naturally includes relevant keywords...",
        "experience": [
            {{ 
                "title": "Job Title", 
                "company": "Company Name",
                "dates": "Month Year - Month Year", 
                "bullets": [
                    "Improved X by Y% using [relevant keyword]",
                    "Led team of Z to achieve [result] with [technology]"
                ] 
            }}
        ],
        "education": [
            {{ "school": "University Name", "degree": "Degree Name", "year": "Year", "gpa": "GPA" }}
        ],
        "skills": [
            {{ "category": "Programming Languages", "items": "Python, Java, JavaScript" }},
            {{ "category": "Frameworks & Tools", "items": "React, Docker, AWS" }}
        ],
        "projects": [
            {{ "name": "Project Name", "link": "https://github.com/...", "description": "Brief description with relevant keywords" }}
        ],
        "keywords_added": ["keyword1", "keyword2", "keyword3"],
        "keywords_skipped": [
            {{"keyword": "keyword4", "reason": "Not relevant to candidate's experience"}},
            {{"keyword": "keyword5", "reason": "Would be dishonest to add"}}
        ]
    }}
    
    IMPORTANT NOTES:
    - The "company" field in experience is REQUIRED (extract from resume or infer from context)
    - keywords_added: List of keywords you successfully incorporated
    - keywords_skipped: List of objects with keyword and reason for skipping
    - If no missing keywords were provided, return empty arrays for keywords_added and keywords_skipped
    - DO NOT use **bold**, *italic*, or any markdown formatting in the text content
    - Keep all text plain and professional - no asterisks, underscores, or special formatting
    - Write naturally without emphasizing words with formatting
    
    ORIGINAL RESUME:
    {original_text}
    
    JOB DESCRIPTION:
    {job_description}
    """
    
    try:
        response = model.generate_content(prompt)
        # Clean up if the model adds markdown code blocks
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_text)
        
        # Ensure keywords_added and keywords_skipped exist
        if 'keywords_added' not in data:
            data['keywords_added'] = []
        if 'keywords_skipped' not in data:
            data['keywords_skipped'] = []
            
        return data
    except json.JSONDecodeError as e:
        return {
            "error": f"Failed to parse AI response as JSON: {str(e)}", 
            "raw": response.text if 'response' in locals() else "No response"
        }
    except Exception as e:
        return {
            "error": f"Enhancement failed: {str(e)}", 
            "raw": response.text if 'response' in locals() else "No response"
        }
