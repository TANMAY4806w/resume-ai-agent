import streamlit as st
import modules.ui as ui
from modules.parser import extract_text_from_pdf, extract_text_from_docx
from modules.enhancer import enhance_resume_content
from modules.converter import convert_resume_data_to_text
# Note: We now import BOTH scoring functions
from modules.scorer import calculate_ats_score, calculate_ai_score
from modules.generator import generate_resume_pdf, generate_resume_docx

# 1. Setup UI
ui.setup_page()
ui.display_header()
selected_template = ui.render_sidebar_settings()

# 2. State Management
if 'resume_data' not in st.session_state: st.session_state.resume_data = None
# Track BEFORE and AFTER ATS scores
if 'score_python_before' not in st.session_state: st.session_state.score_python_before = None
if 'score_python_after' not in st.session_state: st.session_state.score_python_after = None
if 'pdf_path' not in st.session_state: st.session_state.pdf_path = None
if 'docx_path' not in st.session_state: st.session_state.docx_path = None
if 'missing' not in st.session_state: st.session_state.missing = []
if 'keywords_added' not in st.session_state: st.session_state.keywords_added = []
if 'keywords_skipped' not in st.session_state: st.session_state.keywords_skipped = []

# 3. Main Logic Flow
# Step A: Choose Input Method
method = ui.select_input_method()
raw_text = ""

# Step B: Render Forms
if method == "Upload Existing Resume":
    uploaded_file = ui.render_upload_form()
    if uploaded_file:
        if uploaded_file.name.endswith(".pdf"):
            raw_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.name.endswith(".docx"):
            raw_text = extract_text_from_docx(uploaded_file)
else:
    raw_text = ui.render_manual_form()

# Step C: Job Description (Always needed)
job_desc = ui.render_jd_input()

# Step D: The "Analyze" Button (Always Visible)
st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 Analyze & Generate Resume"):
    # Validation
    if not raw_text:
        st.error("⚠️ Please upload a resume or fill in the manual details first.")
    elif not job_desc:
        st.error("⚠️ Please paste the Job Description.")
    else:
        with st.spinner("🔍 Analyzing your resume against the job description..."):
            
            # 1. BEFORE OPTIMIZATION: Score the original resume
            score_python_before, missing_python = calculate_ats_score(raw_text, job_desc)
            
        with st.spinner("✨ Enhancing your resume with AI optimization..."):
            # 2. Enhance Content with Keyword Injection
            # Pass missing keywords to the enhancer for intelligent injection
            ai_data = enhance_resume_content(raw_text, job_desc, missing_keywords=missing_python)
            
            # 3. Check for Errors
            if "error" in ai_data:
                st.error(f"❌ AI Enhancement Error: {ai_data['error']}")
                if 'raw' in ai_data:
                    with st.expander("🔍 Debug Info"):
                        st.text(ai_data['raw'][:1000])
            else:
                # 4. AFTER OPTIMIZATION: Score the enhanced resume
                enhanced_text = convert_resume_data_to_text(ai_data)
                score_python_after, _ = calculate_ats_score(enhanced_text, job_desc)
                
        with st.spinner("📄 Generating professional resume files..."):
            try:
                # 5. Generate Files
                template_map = {
                    "Modern (Blue)": "modern",
                    "Professional (Harvard/Google)": "professional",
                    "Two Column": "twocolumn"
                }
                fname = template_map.get(selected_template, "modern")
                
                pdf_path = generate_resume_pdf(ai_data, template_name=fname)
                docx_path = generate_resume_docx(ai_data)
                
                # 6. Save to Session State
                st.session_state.score_python_before = score_python_before
                st.session_state.score_python_after = score_python_after
                st.session_state.missing = missing_python
                st.session_state.keywords_added = ai_data.get('keywords_added', [])
                st.session_state.keywords_skipped = ai_data.get('keywords_skipped', [])
                st.session_state.pdf_path = pdf_path
                st.session_state.docx_path = docx_path
                st.session_state.resume_data = ai_data
                
                st.success("✅ Resume optimization complete!")
                
            except Exception as e:
                st.error(f"❌ Resume generation failed: {str(e)}")
                st.info("💡 The resume was enhanced successfully, but file generation encountered an error.")

# Step E: Display Results
# We check if 'score_python_before' is not None to know if analysis ran
if st.session_state.score_python_before is not None:
    
    # 1. Show Preview FIRST
    if st.session_state.pdf_path:
        ui.display_pdf_preview(st.session_state.pdf_path)
    
    # 2. Show Optimization Results (Before/After Comparison)
    ui.display_results(
        st.session_state.score_python_before,
        st.session_state.score_python_after,
        st.session_state.missing,
        st.session_state.keywords_added,
        st.session_state.keywords_skipped,
        st.session_state.pdf_path,
        st.session_state.docx_path
    )
    
    with st.expander("👀 Peek at AI Data"):
        st.json(st.session_state.resume_data)