import PyPDF2
from docx import Document
import re

def extract_text_from_pdf(uploaded_file):
    """
    Extract text and hyperlinks from PDF.
    Attempts to extract both visible text and embedded hyperlink URLs.
    """
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        urls = []
        
        for page in pdf_reader.pages:
            # Extract visible text
            page_text = page.extract_text()
            text += page_text + "\n"
            
            # Try to extract hyperlinks from annotations
            if '/Annots' in page:
                annotations = page['/Annots']
                for annotation in annotations:
                    try:
                        obj = annotation.get_object()
                        if obj.get('/Subtype') == '/Link':
                            if '/A' in obj and '/URI' in obj['/A']:
                                url = obj['/A']['/URI']
                                urls.append(url)
                    except:
                        pass
        
        # Also try to find URLs in the text itself
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        found_urls = re.findall(url_pattern, text)
        urls.extend(found_urls)
        
        # Add extracted URLs to the text if they're not already there
        if urls:
            unique_urls = list(set(urls))
            text += "\n\nExtracted Links:\n"
            for url in unique_urls:
                # Extract meaningful info from URL
                if 'github.com' in url:
                    text += f"GitHub: {url}\n"
                elif 'linkedin.com' in url:
                    text += f"LinkedIn: {url}\n"
                else:
                    text += f"Link: {url}\n"
        
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_docx(uploaded_file):
    """
    Extract text and hyperlinks from DOCX.
    """
    try:
        doc = Document(uploaded_file)
        text = ""
        urls = []
        
        for para in doc.paragraphs:
            text += para.text + "\n"
            
            # Extract hyperlinks from paragraph
            for run in para.runs:
                if run.element.rPr is not None:
                    for child in run.element.rPr:
                        if 'hyperlink' in child.tag.lower():
                            try:
                                url = child.get('r:id')
                                if url:
                                    urls.append(url)
                            except:
                                pass
        
        # Add extracted URLs if any
        if urls:
            text += "\n\nExtracted Links:\n" + "\n".join(set(urls))
        
        return text
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"