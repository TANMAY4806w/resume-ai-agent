"""
Converter Module
Converts enhanced resume JSON data back to plain text for re-scoring.
This enables before/after ATS score comparison.
"""

def convert_resume_data_to_text(data):
    """
    Converts the enhanced resume JSON structure back to plain text.
    This text can be used for ATS scoring to measure improvement.
    
    Args:
        data (dict): Enhanced resume data from AI
        
    Returns:
        str: Plain text representation of the resume
    """
    if not data or isinstance(data, str):
        return ""
    
    text_parts = []
    
    # Personal Information
    if data.get('name'):
        text_parts.append(f"Name: {data['name']}")
    if data.get('email'):
        text_parts.append(f"Email: {data['email']}")
    if data.get('phone'):
        text_parts.append(f"Phone: {data['phone']}")
    if data.get('linkedin'):
        text_parts.append(f"LinkedIn: {data['linkedin']}")
    if data.get('github'):
        text_parts.append(f"GitHub: {data['github']}")
    if data.get('website'):
        text_parts.append(f"Website: {data['website']}")
    
    text_parts.append("")  # Blank line
    
    # Summary
    if data.get('summary'):
        text_parts.append("PROFESSIONAL SUMMARY")
        text_parts.append(data['summary'])
        text_parts.append("")
    
    # Experience
    if data.get('experience'):
        text_parts.append("WORK EXPERIENCE")
        for job in data['experience']:
            title = job.get('title', '')
            company = job.get('company', '')
            dates = job.get('dates', '')
            
            if company:
                text_parts.append(f"{title} at {company} ({dates})")
            else:
                text_parts.append(f"{title} ({dates})")
            
            if job.get('bullets'):
                for bullet in job['bullets']:
                    text_parts.append(f"- {bullet}")
            text_parts.append("")
    
    # Projects
    if data.get('projects'):
        text_parts.append("PROJECTS")
        for proj in data['projects']:
            name = proj.get('name', '')
            link = proj.get('link', '')
            desc = proj.get('description', '')
            
            text_parts.append(f"{name}")
            if link:
                text_parts.append(f"Link: {link}")
            if desc:
                text_parts.append(desc)
            text_parts.append("")
    
    # Education
    if data.get('education'):
        text_parts.append("EDUCATION")
        for edu in data['education']:
            school = edu.get('school', '')
            degree = edu.get('degree', '')
            year = edu.get('year', '')
            gpa = edu.get('gpa', '')
            
            text_parts.append(f"{degree} at {school} ({year})")
            if gpa:
                text_parts.append(f"GPA: {gpa}")
            text_parts.append("")
    
    # Skills
    if data.get('skills'):
        text_parts.append("SKILLS")
        for skill in data['skills']:
            category = skill.get('category', '')
            items = skill.get('items', '')
            text_parts.append(f"{category}: {items}")
        text_parts.append("")
    
    return "\n".join(text_parts)
