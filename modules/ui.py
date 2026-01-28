import streamlit as st
from streamlit_option_menu import option_menu
import base64

def setup_page():
    """Configures the page title and CSS with adaptive dark/light mode support."""
    st.set_page_config(page_title="AI Resume Architect", page_icon="🚀", layout="wide")
    st.markdown("""
    <style>
        /* ========== ADAPTIVE COLOR SCHEME ========== */
        /* Automatically adapts to browser's dark/light mode preference */
        
        @media (prefers-color-scheme: dark) {
            :root {
                --bg-primary: #0a0e1a;
                --bg-secondary: #1a1f35;
                --bg-card: #252b42;
                --bg-card-hover: #2d3450;
                --text-primary: #ffffff;
                --text-secondary: #b8c5d6;
                --text-muted: #7a8aa3;
                --accent-primary: #00d4ff;
                --accent-secondary: #0099ff;
                --accent-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                --accent-gradient-alt: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                --border-color: #2d3550;
                --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
                --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
                --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);
                --success-color: #10b981;
                --warning-color: #f59e0b;
                --error-color: #ef4444;
            }
        }
        
        @media (prefers-color-scheme: light) {
            :root {
                --bg-primary: #f8fafc;
                --bg-secondary: #ffffff;
                --bg-card: #ffffff;
                --bg-card-hover: #f1f5f9;
                --text-primary: #1e293b;
                --text-secondary: #475569;
                --text-muted: #94a3b8;
                --accent-primary: #0ea5e9;
                --accent-secondary: #3b82f6;
                --accent-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                --accent-gradient-alt: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                --border-color: #e2e8f0;
                --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.08);
                --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.12);
                --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.16);
                --success-color: #10b981;
                --warning-color: #f59e0b;
                --error-color: #ef4444;
            }
        }
        
        /* ========== GLOBAL STYLES ========== */
        .stApp {
            background: var(--bg-primary);
            transition: background 0.3s ease;
        }
        
        /* ========== ANIMATED HEADER ========== */
        .main-header {
            font-size: 3.5rem;
            font-weight: 800;
            text-align: center;
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0px;
            animation: fadeInDown 0.8s ease-out;
            letter-spacing: -1px;
        }
        
        .sub-header {
            font-size: 1.3rem;
            text-align: center;
            color: var(--text-secondary);
            margin-bottom: 40px;
            animation: fadeInUp 0.8s ease-out 0.2s both;
            font-weight: 400;
        }
        
        /* ========== CARD STYLES ========== */
        .card {
            background: var(--bg-card);
            padding: 30px;
            border-radius: 16px;
            box-shadow: var(--shadow-md);
            border: 1px solid var(--border-color);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            animation: fadeIn 0.6s ease-out;
        }
        
        .card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
            background: var(--bg-card-hover);
        }
        
        /* ========== METRIC BOX ========== */
        .metric-box {
            text-align: center;
            padding: 25px;
            background: var(--bg-card);
            border-radius: 12px;
            border-left: 4px solid var(--accent-primary);
            box-shadow: var(--shadow-sm);
            transition: all 0.3s ease;
            animation: scaleIn 0.5s ease-out;
        }
        
        .metric-box:hover {
            transform: scale(1.02);
            box-shadow: var(--shadow-md);
        }
        
        /* ========== BUTTON STYLES ========== */
        .stButton>button {
            width: 100%;
            border-radius: 12px;
            font-weight: 600;
            background: var(--accent-gradient);
            border: none;
            color: white;
            padding: 14px 28px;
            font-size: 1.05rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: var(--shadow-sm);
            position: relative;
            overflow: hidden;
        }
        
        .stButton>button:before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }
        
        .stButton>button:hover:before {
            left: 100%;
        }
        
        .stButton>button:active {
            transform: translateY(0);
        }
        
        /* ========== RADIO BUTTONS ========== */
        .stRadio > div {
            background: var(--bg-card);
            padding: 15px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
        }
        
        /* ========== FILE UPLOADER ========== */
        .stFileUploader {
            background: var(--bg-card);
            border-radius: 12px;
            padding: 20px;
            border: 2px dashed var(--border-color);
            transition: all 0.3s ease;
        }
        
        .stFileUploader:hover {
            border-color: var(--accent-primary);
            background: var(--bg-card-hover);
        }
        
        /* ========== TEXT INPUTS ========== */
        .stTextInput>div>div>input,
        .stTextArea>div>div>textarea {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: var(--text-primary);
            transition: all 0.3s ease;
        }
        
        .stTextInput>div>div>input:focus,
        .stTextArea>div>div>textarea:focus {
            border-color: var(--accent-primary);
            box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1);
        }
        
        /* ========== EXPANDER ========== */
        .streamlit-expanderHeader {
            background: var(--bg-card);
            border-radius: 8px;
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
        }
        
        .streamlit-expanderHeader:hover {
            background: var(--bg-card-hover);
            border-color: var(--accent-primary);
        }
        
        /* ========== PROGRESS BAR ========== */
        .stProgress > div > div > div {
            background: var(--accent-gradient);
        }
        
        /* ========== ANIMATIONS ========== */
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes scaleIn {
            from {
                opacity: 0;
                transform: scale(0.9);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        
        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        /* ========== SIDEBAR ========== */
        [data-testid="stSidebar"] {
            background: var(--bg-secondary);
            border-right: 1px solid var(--border-color);
        }
        
        [data-testid="stSidebar"] .stRadio > label {
            color: var(--text-primary);
            font-weight: 500;
        }
        
        /* ========== SUCCESS/ERROR MESSAGES ========== */
        .stSuccess {
            background: rgba(16, 185, 129, 0.1);
            border-left: 4px solid var(--success-color);
            border-radius: 8px;
            animation: slideInRight 0.5s ease-out;
        }
        
        .stError {
            background: rgba(239, 68, 68, 0.1);
            border-left: 4px solid var(--error-color);
            border-radius: 8px;
            animation: slideInRight 0.5s ease-out;
        }
        
        .stWarning {
            background: rgba(245, 158, 11, 0.1);
            border-left: 4px solid var(--warning-color);
            border-radius: 8px;
            animation: slideInRight 0.5s ease-out;
        }
        
        .stInfo {
            background: rgba(14, 165, 233, 0.1);
            border-left: 4px solid var(--accent-primary);
            border-radius: 8px;
            animation: slideInRight 0.5s ease-out;
        }
        
        /* ========== SCROLLBAR ========== */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--bg-secondary);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--accent-primary);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent-secondary);
        }
        
        /* ========== LOADING SPINNER ========== */
        .stSpinner > div {
            border-top-color: var(--accent-primary) !important;
        }
    </style>
    """, unsafe_allow_html=True)

def display_header():
    st.markdown('''
    <div class="main-header">
        <span style="display: inline-block; animation: bounce 2s infinite;">🚀</span>
        AI Resume Architect
    </div>
    <style>
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
    </style>
    ''', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Optimize your resume for ATS in seconds with Gemini 2.0</div>', unsafe_allow_html=True)

def select_input_method():
    """Shows the big toggle to choose between Upload or Manual."""
    return option_menu(
        menu_title=None,
        options=["Upload Existing Resume", "Create from Scratch (Manual)"],
        icons=["cloud-upload", "pencil-square"],
        orientation="horizontal",
        styles={
            "container": {"padding": "5px", "background-color": "#262730"},
            "nav-link": {"font-size": "16px", "text-align": "center", "margin": "5px", "--hover-color": "#444"},
            "nav-link-selected": {"background-color": "#00d4ff"},
        }
    )

def render_upload_form():
    """Renders the file uploader."""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📂 Upload Your Resume")
    uploaded_file = st.file_uploader("Drop your PDF or Docx file here", type=["pdf", "docx"])
    st.markdown('</div>', unsafe_allow_html=True)
    return uploaded_file

def render_manual_form():
    """Renders the detailed manual entry form."""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("✍️ Enter Your Details")
    st.info("💡 Only 'Full Name' is strictly required. Leave others blank if not applicable.")
    
    with st.expander("1. Personal Information", expanded=True):
        col1, col2, col3 = st.columns(3)
        name = col1.text_input("Full Name *", placeholder="e.g. Tanmay Patil")
        email = col2.text_input("Email", placeholder="tanmay@example.com")
        phone = col3.text_input("Phone", placeholder="+91 99999...")
        
        col4, col5 = st.columns(2)
        linkedin = col4.text_input("LinkedIn (Optional)", placeholder="tanmay-patil")
        github = col5.text_input("GitHub (Optional)", placeholder="tanmay-git")

    with st.expander("2. Education & Experience"):
        edu = st.text_area("Education", height=100, placeholder="B.Tech in AI/ML from St. John's (2026), GPA 8.5")
        exp = st.text_area("Work Experience (Optional)", height=150, placeholder="Intern at TechCorp (June 2025): Built Chatbot...")

    with st.expander("3. Skills & Projects"):
        skills = st.text_area("Skills", placeholder="Python, SQL, Gemini API, Streamlit...")
        projects = st.text_area("Projects", height=150, placeholder="Project 1: Fake News Detector\nDescription: ...")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Return formatted text only if Name is provided
    if name:
        return f"""
        Name: {name}
        Email: {email}
        Phone: {phone}
        LinkedIn: {linkedin}
        GitHub: {github}
        EDUCATION: {edu}
        EXPERIENCE: {exp}
        PROJECTS: {projects}
        SKILLS: {skills}
        """
    return None

def render_jd_input():
    """Renders the Job Description box."""
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎯 Target Job Description")
    jd = st.text_area("Paste the job description here...", height=150)
    st.markdown('</div>', unsafe_allow_html=True)
    return jd

def render_sidebar_settings():
    """Renders the sidebar template selector."""
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3048/3048122.png", width=50)
        st.header("Settings")
        template = st.radio(
            "Resume Template:",
            ["Modern (Blue)", "Professional (Harvard/Google)", "Two Column"]
        )
        st.markdown("---")
        if st.button("🗑️ Reset All Data"):
            st.session_state.clear()
            st.rerun()
        return template

def display_pdf_preview(pdf_path):
    """Displays the generated PDF directly in the app using an iframe."""
    st.markdown("### 📄 Resume Live Preview")
    try:
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800px" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Could not display preview: {str(e)}")

def display_results(score_python_before, score_python_after,
                    missing, keywords_added, keywords_skipped, pdf_path, docx_path):
    """
    Displays the ATS optimization results with before/after comparison.
    """
    st.markdown("---")
    st.subheader("📊 ATS Optimization Results")
    
    # Calculate improvement
    python_improvement = score_python_after - score_python_before
    
    # Before/After Comparison
    st.markdown("### 🔄 ATS Score: Before vs After Optimization")
    
    col1, col2 = st.columns(2)
    
    # BEFORE score
    with col1:
        st.markdown("#### Before Optimization")
        st.markdown(f"""
        <div class="metric-box" style="border-left: 5px solid #ff4b4b;">
            <p style="color: #aaa; margin:0;">ATS Score</p>
            <h1 style="font-size: 3rem; margin:0; color: #ff4b4b;">{score_python_before}%</h1>
            <p style="font-size: 0.8rem; color: #888;">Original resume</p>
        </div>
        """, unsafe_allow_html=True)
    
    # AFTER score with improvement
    with col2:
        st.markdown("#### After Optimization")
        
        python_color = "#00ff00" if python_improvement > 0 else ("#ff4b4b" if python_improvement < 0 else "#00d4ff")
        python_arrow = "↑" if python_improvement > 0 else ("↓" if python_improvement < 0 else "→")
        
        st.markdown(f"""
        <div class="metric-box" style="border-left: 5px solid {python_color};">
            <p style="color: #aaa; margin:0;">ATS Score</p>
            <h1 style="font-size: 3rem; margin:0; color: {python_color};">{score_python_after}%</h1>
            <p style="font-size: 1rem; color: {python_color}; font-weight: bold;">{python_arrow} {abs(python_improvement):.1f}% improvement</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Optimization Insights
    if python_improvement > 10:
        st.success(f"🎉 **Excellent!** Your ATS score improved by **{python_improvement:.1f}%**! The AI successfully optimized your resume with relevant keywords.")
    elif python_improvement > 5:
        st.success(f"✅ **Great!** Your ATS score improved by **{python_improvement:.1f}%**. Your resume is now more ATS-friendly.")
    elif python_improvement > 0:
        st.info(f"✅ **Good!** Your ATS score improved by **{python_improvement:.1f}%**. Small improvements can make a difference!")
    else:
        st.warning("⚠️ Your resume was already well-optimized for ATS. The AI focused on improving content quality.")
    
    # Keywords Added Section
    if keywords_added and len(keywords_added) > 0:
        st.markdown("### ✅ Keywords Successfully Added")
        st.markdown(f"""
        <div class="card">
            <p>The AI naturally incorporated these missing keywords into your resume:</p>
            <p style="font-size: 1.1rem; color: #00d4ff; font-weight: bold;">
                {', '.join(keywords_added)}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Keywords Skipped Section
    if keywords_skipped and len(keywords_skipped) > 0:
        with st.expander("⚠️ Keywords Skipped (Click to see why)"):
            st.markdown("The AI skipped these keywords because they didn't fit your experience:")
            for item in keywords_skipped:
                if isinstance(item, dict):
                    keyword = item.get('keyword', 'Unknown')
                    reason = item.get('reason', 'No reason provided')
                    st.markdown(f"- **{keyword}**: {reason}")
                else:
                    st.markdown(f"- {item}")
    
    # Missing Keywords (Still not added)
    remaining_missing = [kw for kw in missing if kw not in keywords_added]
    if remaining_missing and len(remaining_missing) > 0:
        with st.expander("🔍 Still Missing Keywords"):
            st.markdown("These keywords from the job description are still not in your resume:")
            st.markdown(f"**{', '.join(remaining_missing[:10])}**")
            st.info("💡 Consider adding these manually if they match your actual experience.")
    
    st.markdown("---")
    
    # Download Section
    st.subheader("📥 Download Your Optimized Resume")
    
    c1, c2 = st.columns(2)
    with c1:
        if pdf_path:
            with open(pdf_path, "rb") as f:
                st.download_button("📄 Download PDF", f, "Optimized_Resume.pdf", "application/pdf", use_container_width=True)
    with c2:
        if docx_path:
            with open(docx_path, "rb") as f:
                st.download_button("📝 Download Word", f, "Optimized_Resume.docx", 
                                 "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                 use_container_width=True)
