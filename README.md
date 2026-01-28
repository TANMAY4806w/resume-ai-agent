# 🚀 AI Resume Architect

> Transform your resume into an ATS-optimized masterpiece with the power of Gemini AI

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Google AI](https://img.shields.io/badge/Google%20AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)

## ✨ Features

### 🎯 Intelligent ATS Optimization
- **Smart Keyword Injection** - Automatically identifies and incorporates missing keywords from job descriptions
- **Before/After Analysis** - Quantifiable ATS score improvement metrics
- **Keyword Tracking** - See exactly which keywords were added and which were skipped (with reasons)

### 🤖 AI-Powered Enhancement
- **Gemini 2.0 Integration** - Leverages Google's latest AI for intelligent resume optimization
- **Natural Language Processing** - Ensures keyword injection feels organic and truthful
- **Context-Aware** - Understands your experience and only adds relevant keywords

### 📄 Professional Resume Generation
- **3 Beautiful Templates**
  - Modern (Blue) - Clean, contemporary design
  - Professional (Harvard/Google) - Traditional corporate style
  - Two Column - Space-efficient layout
- **Dual Format Export** - PDF and DOCX downloads
- **LaTeX Quality** - Professional typesetting for stunning results

### 🎨 Modern UI/UX
- **Adaptive Color Schemes** - Automatically adjusts to dark/light mode
- **Smooth Animations** - Delightful micro-interactions
- **Responsive Design** - Works beautifully on all screen sizes
- **Real-time Preview** - See your optimized resume instantly

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- LaTeX distribution (MiKTeX, TeX Live, or MacTeX)
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/resume-ai-agent.git
   cd resume-ai-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```
   
   Get your free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

4. **Install LaTeX** (if not already installed)
   
   - **Windows**: [MiKTeX](https://miktex.org/download)
   - **macOS**: [MacTeX](https://www.tug.org/mactex/)
   - **Linux**: 
     ```bash
     sudo apt-get install texlive-full
     ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   
   Navigate to `http://localhost:8501`

## 📖 Usage Guide

### Step 1: Choose Your Input Method

**Option A: Upload Existing Resume**
- Supports PDF and DOCX formats
- Automatically extracts text and hyperlinks

**Option B: Create from Scratch**
- Fill in your details manually
- Perfect for first-time resume creation

### Step 2: Paste Job Description

Copy the job description from the posting you're targeting and paste it into the text area.

### Step 3: Analyze & Generate

Click the "🚀 Analyze & Generate Resume" button and watch the magic happen:

1. **ATS Analysis** - Calculates your original ATS score
2. **AI Enhancement** - Optimizes content and injects relevant keywords
3. **Re-scoring** - Measures improvement
4. **File Generation** - Creates professional PDF and DOCX files

### Step 4: Review Results

- **Before/After Scores** - See your ATS improvement percentage
- **Keywords Added** - Review successfully incorporated keywords
- **Keywords Skipped** - Understand why certain keywords weren't added
- **Download Files** - Get your optimized resume in PDF and DOCX

## 🏗️ Project Structure

```
resume-ai-agent/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env                        # API keys (create this)
├── README.md                   # This file
├── modules/
│   ├── ui.py                   # UI components and styling
│   ├── parser.py               # Resume text extraction
│   ├── enhancer.py             # AI-powered enhancement
│   ├── scorer.py               # ATS scoring logic
│   ├── generator.py            # PDF/DOCX generation
│   └── converter.py            # Data format conversion
├── assets/
│   └── templates/
│       ├── modern.tex          # Modern template
│       ├── professional.tex    # Professional template
│       └── twocolumn.tex       # Two-column template
└── output/                     # Generated resume files
```

## 🛠️ Technologies Used

- **[Streamlit](https://streamlit.io/)** - Web framework for the UI
- **[Google Gemini AI](https://ai.google.dev/)** - AI-powered content enhancement
- **[Jinja2](https://jinja.palletsprojects.com/)** - LaTeX template rendering
- **[PyPDF2](https://pypdf2.readthedocs.io/)** - PDF text extraction
- **[python-docx](https://python-docx.readthedocs.io/)** - DOCX handling
- **LaTeX** - Professional document typesetting

## 🎨 UI Features

### Adaptive Design
The UI automatically adapts to your browser's color scheme preference:
- **Dark Mode** - Deep blues with vibrant purple gradients
- **Light Mode** - Clean whites with sky blue accents

### Animations
- Fade-in effects on page load
- Smooth hover transitions
- Bouncing rocket emoji
- Shimmer effects on buttons
- Slide-in notifications

## 📊 How It Works

### ATS Scoring Algorithm

1. **Keyword Extraction** - Identifies important keywords from job description
2. **Resume Analysis** - Extracts keywords from your resume
3. **Gap Analysis** - Finds missing keywords
4. **Score Calculation** - `(Matched Keywords / Total Keywords) × 100`

### AI Enhancement Process

1. **Context Analysis** - AI understands your experience and the job requirements
2. **Keyword Filtering** - Removes generic stopwords and irrelevant terms
3. **Natural Injection** - Incorporates keywords organically into your content
4. **Truthfulness Check** - Only adds keywords that align with your actual experience
5. **Tracking** - Reports which keywords were added and which were skipped

## 🔒 Privacy & Security

- **Local Processing** - Your resume data is processed locally
- **No Storage** - Resume content is not stored on any server
- **API Security** - Gemini API calls are made securely with your private key
- **Session-Based** - All data is cleared when you close the browser

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for powerful language processing
- Streamlit for the amazing web framework
- The open-source community for inspiration and tools

## 📧 Contact

For questions, suggestions, or feedback, please open an issue on GitHub.

---

<div align="center">
  <strong>Made with ❤️ and AI</strong>
  <br>
  <sub>Transform your career, one resume at a time</sub>
</div>
