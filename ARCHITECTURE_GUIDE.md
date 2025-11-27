# 🎯 App6.py - Visual Architecture & Workflow Guide

## 🏗️ APPLICATION ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                      STREAMLIT WEB UI                        │
│                 (Browser: localhost:8501)                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   Chat Input    │  │  Image Upload   │  │   Settings  │ │
│  │                 │  │   for OCR       │  │   Sidebar   │ │
│  └────────┬────────┘  └────────┬────────┘  └─────────────┘ │
│           │                    │                             │
│  ┌────────▼────────────────────▼─────────────────────────┐  │
│  │        Message Display & Chat History                │  │
│  │  (User messages, Bot responses, OCR results)         │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
         │                         │
         │ HTTP Request           │ HTTP Request
         │ (JSON Messages)        │ (Image Path)
         ▼                         ▼
    ┌─────────────┐          ┌──────────────┐
    │   OLLAMA    │          │  PADDLEOCR   │
    │   SERVER    │          │    ENGINE    │
    │             │          │              │
    │ phi3:mini   │          │ - Text       │
    │ LLM Model   │          │   Detection  │
    │             │          │ - Recognition│
    │ Running on  │          │ - Scoring    │
    │ localhost:  │          │              │
    │ 11434       │          │ (Local CPU)  │
    │             │          │              │
    └──────┬──────┘          └──────┬───────┘
           │                        │
           │ JSON Response          │ Extracted Text
           │ (AI Answer)            │ + Confidence
           │                        │
    ┌──────▼────────────────────────▼──────┐
    │      Backend Processing Layer        │
    │  - Streaming responses               │
    │  - Chat history management           │
    │  - OCR result formatting             │
    │  - Context building                  │
    └──────┬─────────────────────────────┘
           │
           │ Update UI
           ▼
    Display response in browser
```

---

## 🔄 USER WORKFLOW DIAGRAMS

### Workflow 1: Chat with AI
```
User Types Message
        │
        ▼
Message sent to Ollama
        │
        ▼
Ollama (phi3:mini) processes
        │
        ├─ Uses context (last 8 messages)
        ├─ Applies system prompt
        └─ Generates response token-by-token
        │
        ▼
Response streams to UI
        │
        ├─ Displayed in real-time
        └─ Added to message history
        │
        ▼
Saved to chat_history.json
```

### Workflow 2: Extract Text from Image (OCR)
```
User uploads image
        │
        ▼
Image saved to ./uploaded_files/
        │
        ▼
PaddleOCR processes image
        │
        ├─ Detects text regions
        ├─ Recognizes characters
        ├─ Calculates confidence
        └─ Returns structured data
        │
        ▼
Results formatted and displayed
        │
        ├─ Text regions shown
        ├─ Confidence scores shown
        └─ Added to chat context
        │
        ▼
Saved to ./ocr_outputs/ as JSON
        │
        ▼
User can ask AI about text
```

### Workflow 3: Combined OCR + Chat
```
Upload Image
    │
    ▼
Extract Text (OCR)
    │
    ├─ "Found: Invoice #12345"
    ├─ "Total: $150.00"
    └─ "Confidence: 95%"
    │
    ▼
Ask AI a Question
    │
    ├─ "Summarize this invoice"
    ├─ "Extract vendor name"
    └─ "What's the due date?"
    │
    ▼
AI uses extracted text + context
    │
    ├─ Understands OCR data
    ├─ Analyzes content
    └─ Provides intelligent answer
    │
    ▼
Response displayed + saved
```

---

## 📊 DATA FLOW DIAGRAM

```
┌──────────────────────────────────────────────────────────┐
│                    LOCAL STORAGE                         │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  ./uploaded_files/          ./ocr_outputs/              │
│  ├─ image1.jpg              ├─ image1_ocr.json         │
│  ├─ image2.png              └─ image2_ocr.json         │
│  └─ document.pdf                                        │
│                              chat_history.json          │
│                              ├─ Chat session 1          │
│                              ├─ Chat session 2          │
│                              └─ Chat session 3          │
│                                                           │
└──────────────────────────────────────────────────────────┘
  ▲                                           ▲
  │                                           │
  │ Save image                                │ Load history
  │                                           │
┌─┴──────────────────┐              ┌────────┴──────┐
│  STREAMLIT APP     │              │  SESSION STATE│
│  (app6.py)         │              │  MANAGEMENT   │
│                    │              │               │
│ ┌────────────────┐ │              │ ┌────────────┐│
│ │  File Handler  │ │              │ │ st.session │││
│ │  (Upload/Save) │ │              │ │   .state   │││
│ │                │─┼──────────────┼─│           │││
│ │ OCR Processor  │ │              │ │ messages  │││
│ │ (PaddleOCR)    │ │              │ │ chats     │││
│ │                │─┼──────────────┼─│           │││
│ │ Chat Manager   │ │              │ │ settings  │││
│ │                │─┼──────────────┼─│           │││
│ └────────────────┘ │              │ └────────────┘│
│                    │              │               │
└────────┬───────────┘              └───────────────┘
         │
         │ HTTP/REST
         │
┌────────┴────────────────────────────────────────────┐
│         EXTERNAL SERVICES                          │
├────────────────────────────────────────────────────┤
│                                                     │
│  OLLAMA Server (localhost:11434)                  │
│  ├─ phi3:mini LLM                                 │
│  └─ Chat API endpoint                             │
│                                                     │
│  PaddleOCR (Local)                                │
│  ├─ Text detection model                          │
│  ├─ Text recognition model                        │
│  └─ Classification model                          │
│                                                     │
│  (NO EXTERNAL CLOUD SERVICES - EVERYTHING LOCAL) │
│                                                     │
└────────────────────────────────────────────────────┘
```

---

## 🎨 UI COMPONENT LAYOUT

```
┌────────────────────────────────────────────────────────────────┐
│                    STREAMLIT APP                               │
│                                                                 │
├───────────────────────────────────────┬────────────────────────┤
│                                       │                         │
│                                       │    SIDEBAR (200px)      │
│                                       │ ┌─────────────────────┐ │
│           MAIN AREA (80%)             │ │  Chat History       │ │
│                                       │ │ ┌─────────────────┐ │ │
│ ┌─────────────────────────────────┐  │ │ │ Previous Chats  │ │ │
│ │ Title:                          │  │ │ │ - Chat 1        │ │ │
│ │ "Ollama Chat + OCR Pro"         │  │ │ │ - Chat 2        │ │ │
│ │ Status: phi3:mini | OCR Active  │  │ │ │ - Chat 3        │ │ │
│ ├─────────────────────────────────┤  │ │ └─────────────────┘ │ │
│ │                                  │  │ │                     │ │
│ │ [📸 Upload Image Expander]      │  │ │ [Settings]          │ │
│ │ ├─ Image preview                │  │ │ - Streaming on/off  │ │
│ │ ├─ 🔍 Extract Text button       │  │ │ - OCR Language      │ │
│ │ └─ Results shown here           │  │ │                     │ │
│ │                                  │  │ │ [🆕 New Chat]       │ │
│ ├─────────────────────────────────┤  │ │                     │ │
│ │ Message Display Area             │  │ │ [🔌 Ollama Status]  │ │
│ │ ┌───────────────────────────────┤  │ │ ┌─────────────────┐ │ │
│ │ │ 👤 User: "Hi there"           │  │ │ │ ✅ Ollama OK    │ │ │
│ │ │ 🤖 Bot: "Hello! I'm phi3:mini.│  │ │ │ 📦 phi3:mini    │ │ │
│ │ │ I can help you with..."       │  │ │ └─────────────────┘ │ │
│ │ │                                │  │ │                     │ │
│ │ │ 📸 OCR: "Invoice extracted..."│  │ │ [🔁 Test API]       │ │
│ │ │ 👤 User: "Summarize this"     │  │ │                     │ │
│ │ │ 🤖 Bot: "Based on the OCR..."│  │ │                     │ │
│ │ └───────────────────────────────┤  │ └─────────────────────┘ │
│ │                                  │  │                         │
│ ├─────────────────────────────────┤  │                         │
│ │ Input Area (Fixed at bottom):   │  │                         │
│ │ ┌───────────────────────────────┐  │                         │
│ │ │ 💬 Type message... [  Send  ] │  │                         │
│ │ └───────────────────────────────┘  │                         │
│ │                                     │                         │
│ │ Footer:                             │                         │
│ │ 💡 Upload images... | 🚀 Ask Q...│  │                         │
│ │                                     │                         │
│ └─────────────────────────────────┘  │                         │
│                                       │                         │
└───────────────────────────────────────┴────────────────────────┘
```

---

## 🔌 API ENDPOINTS USED

### Ollama Chat API
```
Endpoint: http://localhost:11434/api/chat
Method: POST
Request:
{
  "model": "phi3:mini",
  "messages": [
    {"role": "system", "content": "You are..."},
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi!"}
  ],
  "stream": true,
  "options": {
    "temperature": 0.8,
    "top_p": 0.95,
    "num_ctx": 8192
  }
}

Response: 
(Streaming) Each line is JSON with token-by-token content
```

### Ollama Models API
```
Endpoint: http://localhost:11434/api/tags
Method: GET
Response:
{
  "models": [
    {"name": "phi3:mini", "size": 2.2GB, "modified": "..."}
  ]
}
```

---

## 📦 PACKAGE DEPENDENCIES HIERARCHY

```
app6.py
├─ streamlit (Web UI)
│  ├─ tornado (Web server)
│  ├─ watchdog (File monitoring)
│  └─ pydeck (Visualization)
│
├─ requests (HTTP)
│  ├─ urllib3
│  └─ certifi
│
├─ PIL/Pillow (Images)
│  └─ numpy (numeric)
│
├─ PaddleOCR (Text extraction)
│  ├─ paddlepaddle (ML backend)
│  │  ├─ numpy
│  │  ├─ scipy
│  │  └─ protobuf
│  │
│  ├─ paddlex (Paddle extensions)
│  │  └─ scikit-learn
│  │
│  ├─ opencv-contrib-python
│  │  └─ numpy
│  │
│  ├─ pyclipper (Geometry)
│  └─ python-bidi (Text direction)
│
├─ datetime (Built-in)
├─ json (Built-in)
├─ os (Built-in)
└─ io (Built-in)
```

---

## 🚀 STARTUP SEQUENCE DIAGRAM

```
Step 1: User runs .\start_app.ps1
        │
        ▼
Step 2: Activate virtual environment (.venv)
        │
        ├─ Load Python 3.13.2
        └─ Load 40+ packages
        │
        ▼
Step 3: Check Ollama installation
        │
        ├─ Verify: ollama --version
        └─ Verify: phi3:mini model exists
        │
        ▼
Step 4: Start Ollama server
        │
        ├─ Execute: ollama serve
        ├─ Listen on: localhost:11434
        └─ Load phi3:mini into memory (may take 10-30s)
        │
        ▼
Step 5: Launch Streamlit app
        │
        ├─ Change to: ./milestone1/
        ├─ Execute: streamlit run app6.py
        └─ Web server starts: localhost:8501
        │
        ▼
Step 6: Open browser
        │
        └─ Navigate: http://localhost:8501
        │
        ▼
Step 7: App Ready!
        │
        ├─ Chat input active
        ├─ Image upload ready
        ├─ OCR available
        └─ Chat history loaded
```

---

## 🎯 FEATURE INTERACTION DIAGRAM

```
                          ┌─────────────────┐
                          │   OLLAMA CHAT   │
                          │   (phi3:mini)   │
                          └────────┬────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
          ┌─────────────────┐        ┌─────────────────┐
          │ STREAMING MODE  │        │ NON-STREAM MODE │
          │                 │        │                 │
          │ Real-time token │        │ Wait for full   │
          │ display         │        │ response        │
          └────────┬────────┘        └────────┬────────┘
                   │                          │
                   └──────────────┬───────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │   RESPONSE SAVED TO     │
                    │   - Session state       │
                    │   - chat_history.json   │
                    │   - Displayed in UI     │
                    └────────┬────────────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
      ┌──────────────────┐        ┌──────────────────┐
      │  OCR ON DEMAND   │        │  CHAT CONTEXT    │
      │                  │        │                  │
      │ 1. User uploads  │        │ Used in next     │
      │    image         │        │ Ollama request   │
      │                  │        │                  │
      │ 2. Click Extract │        │ Max: 8 messages  │
      │                  │        │                  │
      │ 3. PaddleOCR     │        │ Improves response│
      │    processes     │        │ quality          │
      │                  │        │                  │
      │ 4. Results shown │        │                  │
      │ 5. Saved to JSON │        │                  │
      │                  │        │                  │
      │ 6. Added to chat │        │                  │
      │    context       │        │                  │
      └──────────────────┘        └──────────────────┘
```

---

## 📊 PERFORMANCE CHARACTERISTICS

```
Response Time vs Load:

First Response:
  |
  | ████░░░░░░░░░░░ (3-5 seconds)
  |
Typical Response:
  | ██░░░░░░░░░░░░░ (1-3 seconds)
  |
OCR Processing:
  | ████████░░░░░░░ (2-10 seconds, depends on image)
  |
Saving to File:
  | █░░░░░░░░░░░░░░ (<1 second)
  |
  └─────────────────────────────

Memory Usage Over Time:

Start:     ███░░░░░ (500MB - Streamlit)
After OCR: ██████░░ (2.5GB - After loading models)
Max:       ████████ (3-4GB - During processing)
Idle:      ██░░░░░░ (1-2GB - After processing complete)
```

---

## 🎓 LEARNING PATH

```
Step 1: Understand App Flow
        └─ Read: COMPLETE_REPORT.md

Step 2: Understand Code
        └─ Read: APP6_ANALYSIS.md
           └─ Focus on: Components section

Step 3: Understand Dependencies
        └─ Read: requirements.txt
           └─ Focus on: Why each package?

Step 4: Try Basic Chat
        └─ Start app
        └─ Type simple message
        └─ Observe streaming

Step 5: Try OCR Feature
        └─ Upload test image
        └─ Extract text
        └─ Ask AI about content

Step 6: Explore Features
        └─ Try different image types
        └─ Use chat history
        └─ Adjust settings

Step 7: Customize (Optional)
        └─ Modify app6.py
        └─ Change models
        └─ Add new features
```

---

**Created**: November 24, 2025
**Status**: ✅ Ready for visualization
**All diagrams are text-based for easy reference**
