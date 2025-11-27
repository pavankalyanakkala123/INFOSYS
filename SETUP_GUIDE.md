# Ollama Chat + OCR Pro - Complete Setup & Run Guide

## 📋 Project Overview

**App6.py** is a sophisticated Streamlit-based chatbot application that combines:
- **Ollama Integration**: Local LLM (Language Model) using phi3:mini model
- **PaddleOCR Integration**: Extract text from images using AI
- **Chat History**: Persistent conversation storage
- **Streaming Responses**: Real-time AI response generation
- **Multi-format File Support**: Support for images, PDFs, and documents

---

## ✅ Current Environment Status

### ✨ Already Installed & Ready
Your local environment has **ALL** the required packages installed:

**Core Dependencies:**
- ✅ `streamlit` (1.51.0) - Web UI framework
- ✅ `paddleocr` (3.3.2) - OCR text extraction
- ✅ `paddlepaddle` (3.2.0) - ML computation backend
- ✅ `requests` (2.32.5) - HTTP requests for Ollama API
- ✅ `Pillow` (12.0.0) - Image processing
- ✅ `opencv-contrib-python` (4.10.0.84) - Computer vision

**LLM & AI:**
- ✅ `langchain` (0.3.27) - LLM framework
- ✅ `openai` (2.8.1) - AI integration

**Data Processing:**
- ✅ `pandas` (2.3.3) - Data manipulation
- ✅ `numpy` (2.3.4) - Numerical computing
- ✅ `scipy` (1.16.3) - Scientific computing

**Supporting Libraries:**
- ✅ `BeautifulSoup4` (4.14.2) - Web parsing
- ✅ `lxml` (6.0.2) - XML processing
- ✅ `python-docx` (1.2.1) - Word document support
- ✅ `openpyxl` (3.1.5) - Excel support
- ✅ `python-dotenv` (1.2.1) - Environment variables

### 🔧 External Requirements (Not Python packages)

**1. Ollama (Required)**
   - Local LLM server needed for chat functionality
   - Status: Must be running on `http://localhost:11434`

**2. Ollama Models (Required)**
   - Current installed: `phi3:mini` (2.2 GB) ✅
   - Alternative: `llama2`, `mistral`, `neural-chat`

---

## 🚀 Step-by-Step Startup Guide

### Prerequisites Check
Before starting, verify:
```powershell
# Check Python version (should be 3.13.2)
python --version

# Check Ollama is installed
ollama --version

# Check phi3:mini model is available
ollama list
```

### Step 1: Activate Virtual Environment
```powershell
# Navigate to project root
Set-Location C:\Users\prave\Desktop\INFOSYSPROJECT

# Activate virtual environment
.\.venv\Scripts\Activate.ps1
```

After activation, your prompt should show `(.venv)` prefix.

### Step 2: Start Ollama Server (Required)
Open a **NEW PowerShell terminal** and run:
```powershell
ollama serve
```

You should see:
```
...
time=2025-11-24T... level=INFO msg="Listening on" addr=127.0.0.1:11434
```

**Keep this terminal open** - Ollama must stay running for the app to work.

### Step 3: Run the Streamlit Application
In your original PowerShell terminal (with `.venv` activated):
```powershell
# Navigate to milestone1 folder
Set-Location .\milestone1

# Start Streamlit app
streamlit run app6.py
```

Expected output:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://YOUR_IP:8501
```

### Step 4: Open in Browser
- Click the local URL or paste `http://localhost:8501` in your browser
- The app should load with the Ollama Chat + OCR Pro interface

---

## 📊 Application Features & Usage

### 1️⃣ Chat Interface
- **Input Box**: Type any message at the bottom
- **Model**: phi3:mini (2.2B parameters, optimized for CPU)
- **Streaming**: Responses appear in real-time as they're generated
- **Context**: Maintains conversation history for better responses

### 2️⃣ OCR Image Analysis (Star Feature ⭐)
Steps to extract text from images:

1. Click **📸 Upload Image for OCR Analysis** expander
2. Upload an image (jpg, png, bmp, tiff, jpeg)
3. Click **🔍 Extract Text with OCR** button
4. System will:
   - Extract all text from the image
   - Show confidence scores for each text region
   - Save results to `ocr_outputs/` folder
   - Add extracted text to chat context

5. Ask follow-up questions like:
   - "Summarize this text"
   - "Extract key information"
   - "Correct any OCR errors"

### 3️⃣ Chat History
- **New Chat**: Start fresh conversation
- **Previous Chats**: Click to restore past conversations
- **Delete**: Remove old chats with 🗑️ button
- Storage: `chat_history.json`

### 4️⃣ Settings (Sidebar)
- **Streaming Toggle**: Enable/disable real-time response
- **OCR Language**: Change to Hindi or multilingual models
- **Status Indicators**: Shows if OCR and Ollama are ready

---

## 🎯 Example Workflows

### Workflow 1: Analyze Document Image
```
1. Upload a document/form image
2. Extract text with OCR
3. Ask: "What is the main content of this document?"
4. Ask: "Extract all email addresses and phone numbers"
5. Ask: "Summarize the key points"
```

### Workflow 2: Receipt Analysis
```
1. Upload receipt image
2. Extract text with OCR
3. Ask: "Calculate the total amount"
4. Ask: "List all items and prices"
5. Ask: "What's the tax percentage?"
```

### Workflow 3: Form Recognition
```
1. Upload form/survey image
2. Extract text with OCR
3. Ask: "Fill this form with sample data"
4. Ask: "What fields are required?"
```

---

## 🔍 File Structure

```
INFOSYSPROJECT/
├── .venv/                          # Virtual environment
├── milestone1/
│   ├── app6.py                     # ⭐ Main app (Streamlit + Ollama + OCR)
│   ├── test_ocr.py                 # Test script for OCR functionality
│   ├── uploaded_files/             # Temp storage for uploaded images
│   ├── ocr_outputs/                # OCR extraction results (JSON)
│   └── ollama.py                   # Ollama integration utilities
├── chat_history.json               # Persistent chat storage
├── SETUP_GUIDE.md                  # This file
└── requirements.txt                # Python dependencies
```

---

## 🛠️ Troubleshooting

### Issue 1: "Cannot connect to Ollama"
**Solution:**
- Ensure Ollama is running: `ollama serve` in separate terminal
- Check Ollama is on port 11434: `http://localhost:11434/api/tags`
- Restart both Ollama and Streamlit if needed

### Issue 2: "PaddleOCR not installed"
**Solution:**
```powershell
pip install paddleocr paddlepaddle
```

### Issue 3: "Model phi3:mini not found"
**Solution:**
```powershell
ollama pull phi3:mini
ollama list  # Verify it's installed
```

### Issue 4: "Streamlit not found"
**Solution:**
```powershell
# Ensure venv is activated
.\.venv\Scripts\Activate.ps1
pip install streamlit
```

### Issue 5: OCR extraction too slow
**Solution:**
- Reduce image resolution before uploading
- Use `det_limit_side_len=640` in app6.py (line ~48)
- Consider using GPU if available

### Issue 6: Out of memory errors
**Solution:**
- Close other applications
- Restart Ollama and app
- Consider using smaller model: `ollama pull neural-chat` (7B)

---

## 📦 Dependency Details

### Why Each Package?

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.51.0 | Web interface & real-time updates |
| paddleocr | 3.3.2 | Text extraction from images |
| paddlepaddle | 3.2.0 | ML computation backend for OCR |
| requests | 2.32.5 | HTTP communication with Ollama |
| Pillow | 12.0.0 | Image loading & manipulation |
| langchain | 0.3.27 | LLM integration framework |
| opencv-python | 4.10.0.84 | Advanced image processing |
| numpy | 2.3.4 | Numerical array operations |

### All Packages Installed ✅
No additional downloads needed! Your environment is complete.

---

## 🚦 Quick Health Check Script

Run this to verify everything:
```powershell
# Activate venv
.\.venv\Scripts\Activate.ps1

# Test imports
python -c "
import streamlit; print('✅ Streamlit OK')
from paddleocr import PaddleOCR; print('✅ PaddleOCR OK')
import paddlepaddle; print('✅ PaddleOaddle OK')
import requests; print('✅ Requests OK')
import langchain; print('✅ LangChain OK')
print('All imports successful!')
"

# Check Ollama
Invoke-RestMethod -Uri http://localhost:11434/api/tags

# List installed models
ollama list
```

---

## 📈 Performance Optimization

### For Faster Responses:
1. **Reduce streaming overhead**: Toggle off "Enable Streaming" in sidebar
2. **Use CPU optimization**: Already configured (use_gpu=False)
3. **Batch processing**: Process multiple images at once
4. **Cache models**: First run downloads models (~2min), subsequent runs are instant

### For Better OCR:
1. Upload high-resolution images (300+ DPI)
2. Ensure text is clear and straight
3. Use "en" language for English (default)
4. Avoid rotated/skewed images

---

## 🔐 Security Notes

- **Chat History**: Stored locally in `chat_history.json`
- **Uploaded Images**: Stored in `uploaded_files/` (local only)
- **OCR Results**: Saved in `ocr_outputs/` (local only)
- **No Cloud Upload**: Everything runs locally on your machine
- **No API Keys Needed**: Ollama runs on localhost

---

## 📞 Support Checklist

Before reporting issues:
- ✅ Ollama server is running (`ollama serve`)
- ✅ Virtual environment is activated
- ✅ phi3:mini model is installed (`ollama list`)
- ✅ Port 11434 is not blocked
- ✅ Port 8501 is available (Streamlit)
- ✅ At least 4GB RAM available
- ✅ At least 5GB free disk space

---

## 🎓 Next Steps

1. **Test OCR**: Upload a document image and verify text extraction
2. **Ask Questions**: Use the chat interface with OCR results
3. **Customize**: Modify `app6.py` to add new features
4. **Scale**: Use larger models if needed (llama2, mistral)

---

**Created**: November 24, 2025
**Python Version**: 3.13.2
**Status**: ✅ Ready to Run
