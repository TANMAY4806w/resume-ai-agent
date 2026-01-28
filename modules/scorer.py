import re
import os
import json
import google.generativeai as genai
from collections import Counter
from dotenv import load_dotenv  # Import the loader

# --- 1. LOAD ENVIRONMENT VARIABLES ---
load_dotenv()  # <--- THIS IS THE FIX. It forces Python to read .env

# Get the key using the exact name from your .env file
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    print("⚠️ Error: GEMINI_API_KEY not found. Check your .env file.")

# --- STOPWORDS LIST ---
STOPWORDS = set([
    "about", "above", "across", "after", "against", "along", "among", "apart", "around", "at", 
    "because", "before", "behind", "being", "below", "beneath", "beside", "between", "beyond", 
    "both", "but", "by", "can", "cannot", "come", "could", "did", "do", "does", "doing", "down", 
    "during", "each", "else", "even", "ever", "every", "for", "from", "get", "got", "had", "has", 
    "have", "he", "her", "here", "hers", "herself", "him", "himself", "his", "how", "if", "in", 
    "into", "is", "it", "its", "itself", "just", "kept", "know", "less", "let", "like", "likely", 
    "make", "many", "may", "me", "might", "more", "most", "much", "must", "my", "myself", "near", 
    "need", "no", "nor", "not", "now", "of", "off", "often", "on", "once", "one", "only", "or", 
    "other", "our", "ours", "ourselves", "out", "over", "own", "said", "same", "say", "see", 
    "shall", "she", "should", "since", "so", "some", "such", "than", "that", "the", "their", 
    "them", "then", "there", "these", "they", "this", "those", "through", "to", "too", "towards", 
    "under", "until", "up", "upon", "us", "use", "used", "uses", "very", "want", "was", "way", 
    "we", "well", "were", "what", "when", "where", "which", "while", "who", "whom", "whose", 
    "why", "will", "with", "within", "without", "would", "yes", "yet", "you", "your", "yours", 
    "yourself", "job", "description", "requirements", "role", "overview", "responsibilities", 
    "qualifications", "looking", "seeking", "must", "have", "ability", "experience", "year", 
    "years", "work", "team", "skills", "using", "strong", "proficient", "knowledge", "creating", 
    "working", "candidate", "ideal", "opportunity"
])

# --- FUNCTION 1: STRICT PYTHON SCORER ---
def extract_keywords(text):
    if not text:
        return []
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    words = text.split()
    keywords = [w for w in words if w not in STOPWORDS and len(w) > 1]
    return sorted(list(set(keywords)))

def calculate_ats_score(resume_text, job_desc_text):
    resume_keywords = set(extract_keywords(resume_text))
    jd_keywords = set(extract_keywords(job_desc_text))
    if not jd_keywords:
        return 0, []
    matches = resume_keywords.intersection(jd_keywords)
    missing = jd_keywords - resume_keywords
    score = (len(matches) / len(jd_keywords)) * 100
    return round(score, 2), list(missing)

# --- FUNCTION 2: GEMINI AI SCORER ---
def calculate_ai_score(resume_text, job_desc):
    """
    Calculate ATS score using Gemini AI for context-aware matching.
    Falls back to 0 if AI fails.
    """
    import time
    
    # Truncate inputs if too long to avoid API limits
    max_length = 3000
    resume_truncated = resume_text[:max_length] if len(resume_text) > max_length else resume_text
    job_truncated = job_desc[:max_length] if len(job_desc) > max_length else job_desc
    
    for attempt in range(2):  # Try twice
        try:
            model = genai.GenerativeModel('gemini-flash')
            
            # Simplified prompt to reduce API load
            prompt = f"""Evaluate resume match to job (0-100 score).

JOB: {job_truncated}

RESUME: {resume_truncated}

Return ONLY this JSON (no markdown):
{{"score": 75, "missing": ["skill1", "skill2"]}}"""
            
            print(f"🔍 Attempt {attempt + 1}: Calling Gemini AI for scoring...")
            
            response = model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.1,
                    'max_output_tokens': 200,
                }
            )
            
            if not response or not response.text:
                print(f"⚠️ Attempt {attempt + 1}: Empty response from Gemini")
                if attempt == 0:
                    time.sleep(1)
                    continue
                return 0, []
            
            text = response.text.strip()
            print(f"✅ Gemini response received: {text[:100]}...")
            
            # Clean potential markdown wrappers
            if "```" in text:
                text = text.replace("```json", "").replace("```", "").strip()
            
            # Try to extract JSON even if there's extra text
            if "{" in text and "}" in text:
                start = text.index("{")
                end = text.rindex("}") + 1
                text = text[start:end]
                    
            data = json.loads(text)
            score = data.get("score", 0)
            missing = data.get("missing", [])
            
            # Validate score is in valid range
            if not isinstance(score, (int, float)) or score < 0 or score > 100:
                print(f"⚠️ Invalid AI score: {score}, defaulting to 0")
                return 0, missing
            
            print(f"✅ AI Score calculated: {score}%")
            return round(score, 2), missing
            
        except json.JSONDecodeError as e:
            print(f"❌ Attempt {attempt + 1} - JSON Parse Error: {e}")
            if 'text' in locals():
                print(f"Raw response: {text[:300]}")
            if attempt == 0:
                time.sleep(1)
                continue
            return 0, []
            
        except Exception as e:
            print(f"❌ Attempt {attempt + 1} - AI Scoring Failed: {type(e).__name__}: {str(e)}")
            if attempt == 0:
                time.sleep(1)
                continue
            return 0, []
    
    print("❌ All attempts failed, returning 0")
    return 0, []