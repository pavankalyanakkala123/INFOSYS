# 🚀 STEP-BY-STEP TERMINAL COMMANDS - Run OCR + Ollama

## ✅ STATUS CHECK

**PaddleOCR**: ✅ WORKING  
**Ollama Server**: ✅ WORKING  
**All dependencies**: ✅ INSTALLED  

Everything is ready to run!

---

## 📋 TERMINAL COMMANDS (Copy & Paste)

### 🔴 TERMINAL 1: Start Ollama Server

**Copy this entire block and paste into PowerShell:**

```powershell
ollama serve
```

**What you should see:**
```
time=2025-11-24T14:10:00.000000Z level=INFO msg="Listening on" addr=127.0.0.1:11434
(stays running, listening for requests)
```

✅ **Keep this terminal OPEN at all times**

---

### 🟢 TERMINAL 2: Activate Virtual Environment + Run Streamlit

**Copy this entire block and paste into a NEW PowerShell:**

```powershell
cd C:\Users\prave\Desktop\INFOSYSPROJECT
.\.venv\Scripts\Activate.ps1
```

**Expected output:**
```
(.venv) PS C:\Users\prave\Desktop\INFOSYSPROJECT>
```

Notice the `(.venv)` prefix - this means virtual environment is ACTIVE ✅

Now run Streamlit:

```powershell
cd milestone1
streamlit run app6.py
```

**Expected output:**
```
Local URL: http://localhost:8501
Network URL: http://192.168.0.XXX:8501

You can now view your Streamlit app in your browser.
```

✅ **Keep this terminal OPEN while using the app**

---

### 🔵 TERMINAL 3 (Optional): Test OCR Manually

**Copy this entire block and paste into a THIRD PowerShell:**

```powershell
cd C:\Users\prave\Desktop\INFOSYSPROJECT
.\.venv\Scripts\Activate.ps1
cd milestone1
python test_paddleocr_working.py
```

**Expected output:**
```
✅ RESULT: PaddleOCR IS WORKING CORRECTLY!
```

This proves OCR is functional ✅

---

## 🌐 BROWSER: Access the App

**Open your browser and go to:**
```
http://localhost:8501
```

**What you'll see:**
- Title: "💬 Ollama Chat + OCR Pro"
- Sidebar: ✅ Ollama is running
- Main area: Chat box ready
- Expander: 📸 Upload Image for OCR Analysis

---

## 📸 HOW TO TEST OCR IN THE APP

**Step 1: Prepare an image with text**
- Find any image with readable text (receipt, document, photo with text)
- Can be JPG, PNG, BMP, TIFF format

**Step 2: Upload image**
- Click: 📸 Upload Image for OCR Analysis (expander)
- Click: Choose file
- Select your image with text

**Step 3: Extract text**
- Click: 🔍 Extract Text with OCR button
- Wait 3-5 seconds...

**Step 4: See results**
```
📸 OCR Results from image.jpg:

Extracted Text:
[Your text here]

Detailed Results:
- Text line 1 (confidence: 95%)
- Text line 2 (confidence: 92%)
```

**Step 5: Ask AI about text**
- Type in chat: "Summarize this text"
- Type: "Extract important information"
- Type: "What is the total amount?"

---

## 🎯 QUICK REFERENCE - TERMINAL COMMANDS

| Action | Command | Terminal |
|--------|---------|----------|
| Start Ollama | `ollama serve` | 1 |
| Activate venv | `.\.venv\Scripts\Activate.ps1` | 2 |
| Navigate to app | `cd C:\Users\prave\Desktop\INFOSYSPROJECT\milestone1` | 2 |
| Run Streamlit | `streamlit run app6.py` | 2 |
| Test OCR | `python test_paddleocr_working.py` | 3 |
| Check Ollama | `ollama list` | 3 |
| Verify models | `Invoke-RestMethod -Uri http://localhost:11434/api/tags` | 3 |

---

## ⚡ FASTEST STARTUP (Copy-Paste Ready)

### Setup 1: Terminal 1 (Just copy and paste)
```powershell
ollama serve
```

### Setup 2: Terminal 2 (Just copy and paste)
```powershell
cd C:\Users\prave\Desktop\INFOSYSPROJECT; .\.venv\Scripts\Activate.ps1; cd milestone1; streamlit run app6.py
```

### Setup 3: Browser
```
http://localhost:8501
```

---

## ✅ VERIFICATION CHECKLIST

Before you start, verify each step:

### ✅ Check 1: Ollama Installed
```powershell
ollama --version
```
Should show version like: `ollama version 0.1.XX`

### ✅ Check 2: Virtual Environment Ready
```powershell
cd C:\Users\prave\Desktop\INFOSYSPROJECT
.\.venv\Scripts\Activate.ps1
```
Prompt should show `(.venv)` prefix

### ✅ Check 3: PaddleOCR Works
```powershell
cd milestone1
python test_paddleocr_working.py
```
Should show: `✅ RESULT: PaddleOCR IS WORKING CORRECTLY!`

### ✅ Check 4: Ollama Responsive
```powershell
Invoke-RestMethod -Uri http://localhost:11434/api/tags
```
Should show JSON with `phi3:mini` model

---

## 🔥 FULL WORKFLOW (From Scratch)

**Time needed: 5-10 minutes**

### Minute 1-2: Start Ollama
```powershell
# Terminal 1
ollama serve
```
Wait for message: `Listening on 127.0.0.1:11434`

### Minute 2-3: Start App
```powershell
# Terminal 2
cd C:\Users\prave\Desktop\INFOSYSPROJECT
.\.venv\Scripts\Activate.ps1
cd milestone1
streamlit run app6.py
```
Wait for: `Local URL: http://localhost:8501`

### Minute 3-4: Open Browser
```
http://localhost:8501
```

### Minute 4-5: Test Chat
- Type: "Hello, how are you?"
- See AI response in real-time

### Minute 5-10: Test OCR
- Click: 📸 Upload Image for OCR Analysis
- Upload image with text
- Click: 🔍 Extract Text with OCR
- See extracted text

---

## 🐛 TROUBLESHOOTING COMMANDS

### Issue: "Cannot connect to Ollama"

**Test connection:**
```powershell
Invoke-RestMethod -Uri http://localhost:11434/api/tags -TimeoutSec 5
```

**If fails**: Ollama not running → Go back to Terminal 1, run `ollama serve`

---

### Issue: "Module not found" or ImportError

**Fix:**
```powershell
# Terminal 2
.\.venv\Scripts\Activate.ps1
pip install --upgrade paddleocr paddlepaddle streamlit
```

---

### Issue: PaddleOCR not responding

**Test:**
```powershell
cd C:\Users\prave\Desktop\INFOSYSPROJECT\milestone1
python test_paddleocr_working.py
```

**If works**: OCR is fine, app might need restart
**If fails**: Run pip install above

---

### Issue: "Port 8501 already in use"

**Option 1: Use different port**
```powershell
streamlit run app6.py --server.port 8502
```

**Option 2: Kill process on port**
```powershell
$proc = Get-Process | Where-Object {$_.ProcessName -eq "streamlit"}
$proc | Stop-Process -Force
```

---

### Issue: "Port 11434 already in use"

**Kill Ollama and restart:**
```powershell
Stop-Process -Name "ollama*" -Force
Start-Sleep -Seconds 2
ollama serve
```

---

## 📊 WHAT EACH COMPONENT DOES

| Component | Command | Port | Purpose |
|-----------|---------|------|---------|
| Ollama | `ollama serve` | 11434 | AI backend (phi3:mini) |
| Streamlit | `streamlit run app6.py` | 8501 | Web UI & OCR |
| PaddleOCR | Built into app | - | Text extraction |
| Browser | http://localhost:8501 | - | Interface |

---

## 🎓 UNDERSTANDING THE FLOW

```
You type message in browser (http://localhost:8501)
        ↓
Streamlit app receives message (Terminal 2)
        ↓
App sends to Ollama server (Terminal 1) on localhost:11434
        ↓
Ollama uses phi3:mini to generate response
        ↓
Response sent back to app
        ↓
Streamlit streams response to your browser
        ↓
You see AI response in real-time
```

**For OCR:**
```
You upload image in browser
        ↓
Streamlit app saves image
        ↓
PaddleOCR processes image (Terminal 2)
        ↓
Extracted text returned
        ↓
Text added to chat context
        ↓
You can ask AI about text
```

---

## 🚀 TERMINAL COMMANDS SUMMARY

**Terminal 1** (Keep open):
```powershell
ollama serve
```

**Terminal 2** (Keep open):
```powershell
cd C:\Users\prave\Desktop\INFOSYSPROJECT
.\.venv\Scripts\Activate.ps1
cd milestone1
streamlit run app6.py
```

**Terminal 3** (Optional testing):
```powershell
cd C:\Users\prave\Desktop\INFOSYSPROJECT\milestone1
python test_paddleocr_working.py
```

**Browser**:
```
http://localhost:8501
```

---

## ✨ YOU'RE READY!

Everything is:
- ✅ Installed
- ✅ Configured
- ✅ Tested
- ✅ Working

**Next step**: Copy Terminal 1 and Terminal 2 commands above and paste them into PowerShell!

**Then open**: http://localhost:8501

**Enjoy**! 🎉

---

**Created**: November 24, 2025
**Status**: ✅ All systems GO
**PaddleOCR**: ✅ VERIFIED WORKING
**Ollama**: ✅ VERIFIED WORKING
