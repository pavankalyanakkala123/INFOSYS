import streamlit as st
import json
import os
import requests
from datetime import datetime
import time
from typing import Generator, Optional
from PIL import Image
import io

# PaddleOCR imports
try:
    from paddleocr import PaddleOCR
    PADDLEOCR_AVAILABLE = True
except ImportError:
    PADDLEOCR_AVAILABLE = False
    st.warning("⚠️ PaddleOCR not installed. Run: pip install paddleocr")

# Configure the page
st.set_page_config(page_title="Ollama Chatbot Pro + OCR", page_icon="💬", layout="wide")

# Constants
UPLOAD_DIR = "uploaded_files"
OCR_OUTPUT_DIR = "ocr_outputs"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "phi3:mini"

# Create directories
for directory in [UPLOAD_DIR, OCR_OUTPUT_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Initialize PaddleOCR (runs only once)
@st.cache_resource
def load_paddleocr():
    """Initialize PaddleOCR model with CPU optimization"""
    if not PADDLEOCR_AVAILABLE:
        return None
    try:
        # Use only supported parameters for current version
        # PaddleOCR 3.3.2 only accepts: lang, ocr_version, drop_score, use_dilation, det_db_thresh, etc.
        ocr = PaddleOCR(lang='en')  # Minimal, working configuration
        return ocr
    except Exception as e:
        st.error(f"Error loading PaddleOCR: {e}")
        return None

# OCR Processing Function
def process_image_with_ocr(image_path: str, ocr_instance) -> dict:
    """
    Process image with PaddleOCR and return structured results
    
    Returns:
        dict with keys: 'text', 'boxes', 'scores', 'formatted_output'
    """
    if ocr_instance is None:
        return {"error": "OCR not available"}
    
    try:
        # Run OCR using predict() - returns OCRResult object (list of dicts)
        result = ocr_instance.predict(image_path)
        
        if not result or len(result) == 0:
            return {"error": "No text detected in image"}
        
        # Extract text, boxes, and confidence scores
        extracted_data = {
            'text': [],
            'boxes': [],
            'scores': [],
            'formatted_output': ""
        }
        
        full_text_lines = []
        
        # result is a list of OCRResult objects (usually one per page)
        ocr_result = result[0]
        
        # Access the recognized texts and scores from the result
        # The OCRResult object is dict-like with keys: 'rec_texts', 'rec_scores', 'rec_polys', etc.
        rec_texts = ocr_result.get('rec_texts', [])
        rec_scores = ocr_result.get('rec_scores', [])
        rec_polys = ocr_result.get('rec_polys', [])
        
        if not rec_texts:
            return {"error": "No readable text detected in image"}
        
        # Process each recognized text
        for i, text in enumerate(rec_texts):
            try:
                text = str(text).strip()
                
                if not text:
                    continue
                
                # Get confidence score
                confidence = float(rec_scores[i]) if i < len(rec_scores) else 0.0
                
                # Get box coordinates if available
                box = rec_polys[i] if i < len(rec_polys) else None
                
                extracted_data['text'].append(text)
                if box is not None:
                    extracted_data['boxes'].append(box.tolist() if hasattr(box, 'tolist') else box)
                extracted_data['scores'].append(confidence)
                
                full_text_lines.append(f"{text} (confidence: {confidence:.2%})")
                
            except (IndexError, TypeError, ValueError) as e:
                continue
        
        if not extracted_data['text']:
            return {"error": "No readable text detected in image"}
        
        # Create formatted output
        extracted_data['formatted_output'] = "\n".join(full_text_lines)
        extracted_data['full_text'] = " ".join(extracted_data['text'])
        
        return extracted_data
        
    except Exception as e:
        return {"error": f"OCR processing failed: {str(e)}"}

# System prompt with OCR awareness
SYSTEM_PROMPT = """You are a highly knowledgeable and helpful AI assistant with OCR capabilities. When answering questions:
- Provide comprehensive, detailed explanations
- If OCR text is provided, analyze it thoroughly and answer questions about the content
- Include relevant examples and context
- Break down complex topics into understandable parts
- Use clear structure with logical flow
- Be thorough but concise - elaborate without unnecessary repetition
- If appropriate, provide step-by-step guidance
- Consider multiple perspectives when relevant"""

# [Keep all your existing helper functions: load_chat_history, save_chat_history, get_chat_title, etc.]
def load_chat_history():
    """Load chat history from JSON file"""
    if os.path.exists("chat_history.json"):
        try:
            with open("chat_history.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_chat_history(history):
    """Save chat history to JSON file"""
    with open("chat_history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

def get_chat_title(messages):
    """Generate a title from the first user message"""
    for msg in messages:
        if msg["role"] == "user" and msg.get("type") not in ["file", "ocr"]:
            title = msg["content"][:30]
            return title + "..." if len(title) == 30 else title
    return "New Chat"

def build_context_messages(context_messages, current_prompt):
    """Build optimized message context with system prompt"""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    if context_messages:
        recent_messages = context_messages[-8:]
        for msg in recent_messages:
            if msg["role"] == "user" and msg.get("type") not in ["file", "ocr"]:
                messages.append({"role": "user", "content": msg["content"]})
            elif msg["role"] == "assistant":
                messages.append({"role": "assistant", "content": msg["content"]})
    
    enhanced_prompt = f"{current_prompt}\n\n[Provide a detailed, comprehensive response]"
    messages.append({"role": "user", "content": enhanced_prompt})
    
    return messages

def stream_ollama_response(prompt: str, context_messages=None) -> Generator[str, None, None]:
    """Stream response from Ollama API for real-time display"""
    try:
        messages = build_context_messages(context_messages, prompt)
        
        data = {
            "model": OLLAMA_MODEL,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": 0.8,
                "top_p": 0.95,
                "top_k": 50,
                "num_ctx": 2048,
                "num_predict": 512,
                "repeat_penalty": 1.1
            }
        }
        
        response = requests.post(OLLAMA_CHAT_URL, json=data, stream=True, timeout=300)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line)
                    if "message" in chunk:
                        content = chunk["message"].get("content", "")
                        if content:
                            yield content
                    if chunk.get("done", False):
                        break
                except json.JSONDecodeError:
                    continue
    
    except requests.exceptions.ConnectionError:
        yield "⚠️ **Error**: Cannot connect to Ollama.\n\n**Solutions:**\n1. Make sure Ollama is running: `ollama serve`\n2. Check if the model is installed: `ollama list`\n3. Pull the model if needed: `ollama pull phi3:mini`"
    except requests.exceptions.Timeout:
        yield "⚠️ **Error**: Ollama request timed out. The model may be overloaded. Please wait a moment and try again."
    except requests.exceptions.HTTPError as e:
        yield f"⚠️ **Error**: Ollama server error ({e.response.status_code}). Try restarting Ollama: `ollama serve`"
    except Exception as e:
        yield f"⚠️ **Error**: {str(e)}"

# Enhanced styling with OCR elements
st.markdown("""
<style>
.chat-message {
    padding: 1rem;
    border-radius: 15px;
    margin-bottom: 1rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    animation: fadeIn 0.3s ease;
}

.user-msg {
    background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
    color: white;
    margin-left: 20%;
}

.bot-msg {
    background: white;
    border: 1px solid #E5E7EB;
    margin-right: 20%;
    color: #1F2937;
}

.ocr-result {
    background: linear-gradient(135deg, #10B981 0%, #059669 100%);
    color: white;
    padding: 1rem;
    border-radius: 15px;
    margin-left: 20%;
    font-family: monospace;
    max-height: 400px;
    overflow-y: auto;
}

.file-upload {
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
    color: white;
    padding: 0.8rem;
    border-radius: 15px;
    margin-left: 20%;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.stButton > button {
    background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
    color: white;
    padding: 0.5rem 2rem;
    border-radius: 25px;
    border: none;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(99, 102, 241, 0.2);
}

.streaming-indicator {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #6366F1;
    border-radius: 50%;
    animation: pulse 1.5s ease-in-out infinite;
    margin-left: 5px;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

.performance-badge {
    display: inline-block;
    padding: 4px 12px;
    background: linear-gradient(135deg, #10B981 0%, #059669 100%);
    color: white;
    border-radius: 12px;
    font-size: 0.85em;
    margin-left: 10px;
}

.ocr-badge {
    display: inline-block;
    padding: 4px 12px;
    background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
    color: white;
    border-radius: 12px;
    font-size: 0.85em;
    margin-left: 10px;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_chat_history()
if "streaming_enabled" not in st.session_state:
    st.session_state.streaming_enabled = True
if "ocr_instance" not in st.session_state:
    st.session_state.ocr_instance = load_paddleocr()

# Sidebar
with st.sidebar:
    st.title("💬 Chat History")
    
    # OCR Status
    if PADDLEOCR_AVAILABLE and st.session_state.ocr_instance:
        st.success("✅ PaddleOCR Ready")
    else:
        st.error("❌ PaddleOCR Not Available")
        st.caption("Install: `pip install paddleocr`")
    
    st.markdown("---")
    
    # Settings
    st.markdown("### ⚙️ Settings")
    st.session_state.streaming_enabled = st.checkbox(
        "Enable Streaming", 
        value=st.session_state.streaming_enabled,
        help="Show responses in real-time"
    )
    
    # OCR Language Selection
    if PADDLEOCR_AVAILABLE:
        ocr_lang = st.selectbox(
            "OCR Language",
            ["en", "hi", "multilingual"],
            help="Select OCR language model"
        )
    
    st.markdown("---")
    
    # New chat button
    if st.button("🆕 New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.current_chat = None
        st.rerun()
    
    # Display chat history
    st.markdown("### Previous Chats")
    
    if st.session_state.chat_history:
        for chat_id, chat_data in sorted(st.session_state.chat_history.items(), reverse=True):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                chat_title = get_chat_title(chat_data)
                is_current = chat_id == st.session_state.current_chat
                button_label = f"{'📍 ' if is_current else ''}{chat_title}"
                
                if st.button(button_label, key=f"chat_{chat_id}", use_container_width=True):
                    st.session_state.messages = chat_data
                    st.session_state.current_chat = chat_id
                    st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"delete_{chat_id}"):
                    del st.session_state.chat_history[chat_id]
                    save_chat_history(st.session_state.chat_history)
                    if chat_id == st.session_state.current_chat:
                        st.session_state.messages = []
                        st.session_state.current_chat = None
                    st.rerun()
    else:
        st.caption("No previous chats yet")

# Main chat interface
st.title("💬 Ollama Chat + OCR Pro")
st.caption(f"Chatting with **{OLLAMA_MODEL}** | OCR: **{'✓ Enabled' if PADDLEOCR_AVAILABLE else '✗ Disabled'}**")

if st.session_state.streaming_enabled:
    st.markdown('<span class="performance-badge">⚡ Streaming Enabled</span>', unsafe_allow_html=True)

if PADDLEOCR_AVAILABLE:
    st.markdown('<span class="ocr-badge">🔍 OCR Active</span>', unsafe_allow_html=True)

# Image upload section with OCR
with st.expander("📸 Upload Image for OCR Analysis"):
    uploaded_image = st.file_uploader(
        "Upload an image to extract text",
        type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'],
        key="ocr_uploader"
    )
    
    if uploaded_image:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
        
        with col2:
            if st.button("🔍 Extract Text with OCR", use_container_width=True):
                if not PADDLEOCR_AVAILABLE or st.session_state.ocr_instance is None:
                    st.error("PaddleOCR not available. Please install: `pip install paddleocr`")
                else:
                    # Save uploaded image
                    image_path = os.path.join(UPLOAD_DIR, uploaded_image.name)
                    with open(image_path, "wb") as f:
                        f.write(uploaded_image.getvalue())
                    
                    # Process with OCR
                    with st.spinner("🔍 Processing image with OCR..."):
                        ocr_result = process_image_with_ocr(image_path, st.session_state.ocr_instance)
                    
                    if "error" in ocr_result:
                        st.error(ocr_result["error"])
                    else:
                        # Add OCR result to chat
                        ocr_message = f"📸 **OCR Results from {uploaded_image.name}:**\n\n"
                        ocr_message += f"**Extracted Text:**\n{ocr_result['full_text']}\n\n"
                        ocr_message += f"**Detailed Results:**\n{ocr_result['formatted_output']}"
                        
                        st.session_state.messages.append({
                            "role": "user",
                            "type": "ocr",
                            "content": ocr_message,
                            "ocr_data": ocr_result,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        
                        # Save OCR results to file
                        ocr_file_path = os.path.join(OCR_OUTPUT_DIR, f"{uploaded_image.name}_ocr.json")
                        with open(ocr_file_path, "w", encoding="utf-8") as f:
                            json.dump(ocr_result, f, indent=4, ensure_ascii=False)
                        
                        st.success(f"✅ Text extracted! {len(ocr_result['text'])} lines detected")
                        st.rerun()

# Display messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        if msg.get("type") == "ocr":
            st.markdown(f'<div class="ocr-result">🔍 OCR ANALYSIS\n\n{msg["content"]}</div>', 
                       unsafe_allow_html=True)
        elif msg.get("type") == "file":
            st.markdown(f"""
                <div class="file-upload">
                    <span>📎</span>
                    <span>{msg["content"]}</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message user-msg">{msg["content"]}</div>', 
                       unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message bot-msg">{msg["content"]}</div>', 
                   unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Type your message or ask about OCR results...")

if user_input:
    # Check if there's recent OCR data to include in context
    ocr_context = ""
    for msg in reversed(st.session_state.messages[-3:]):  # Check last 3 messages
        if msg.get("type") == "ocr" and "ocr_data" in msg:
            ocr_context = f"\n\n[Context: Recent OCR extracted text: {msg['ocr_data'].get('full_text', '')}]"
            break
    
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    # Display user message
    st.markdown(f'<div class="chat-message user-msg">{user_input}</div>', 
               unsafe_allow_html=True)
    
    # Enhance prompt with OCR context if available
    enhanced_input = user_input + ocr_context
    
    # Get bot response
    if st.session_state.streaming_enabled:
        response_placeholder = st.empty()
        full_response = ""
        start_time = time.time()
        
        for chunk in stream_ollama_response(enhanced_input, st.session_state.messages):
            full_response += chunk
            response_placeholder.markdown(
                f'<div class="chat-message bot-msg">{full_response}<span class="streaming-indicator"></span></div>', 
                unsafe_allow_html=True
            )
        
        elapsed_time = time.time() - start_time
        response_placeholder.markdown(
            f'<div class="chat-message bot-msg">{full_response}</div>', 
            unsafe_allow_html=True
        )
        
        bot_reply = full_response
    else:
        with st.spinner("🤔 Generating response..."):
            start_time = time.time()
            bot_reply = ""
            for chunk in stream_ollama_response(enhanced_input, st.session_state.messages):
                bot_reply += chunk
            elapsed_time = time.time() - start_time
        
        st.markdown(f'<div class="chat-message bot-msg">{bot_reply}</div>', 
                   unsafe_allow_html=True)
    
    # Add bot reply
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    # Save chat history
    if not st.session_state.current_chat:
        chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.session_state.current_chat = chat_id
    else:
        chat_id = st.session_state.current_chat
    
    st.session_state.chat_history[chat_id] = st.session_state.messages
    save_chat_history(st.session_state.chat_history)
    
    st.caption(f"⏱️ Response time: {elapsed_time:.2f}s")
    st.rerun()

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("💡 Upload images to extract text with OCR")
with col2:
    st.caption("🚀 Ask questions about extracted text")
with col3:
    st.caption("🔍 Supports 109 languages")
