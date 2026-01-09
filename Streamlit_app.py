import streamlit as st
import time
import threading
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import json
from datetime import datetime

# 🎨 Custom CSS
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .dashboard-header {
        background: rgba(0, 0, 0, 0.7);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 2px solid #00ffff;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.3);
        text-align: center;
    }
    
    .dashboard-title {
        background: linear-gradient(45deg, #00ffff, #00ffaa, #ff00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
    }
    
    .input-section {
        background: rgba(0, 0, 0, 0.6);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        border: 1px solid #00ffff;
    }
    
    .input-label {
        color: #00ffff;
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: block;
        font-size: 1.1rem;
    }
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background: rgba(0, 20, 40, 0.8) !important;
        color: white !important;
        border: 2px solid #00ffff !important;
        border-radius: 10px;
        padding: 0.8rem;
        transition: all 0.3s;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #ff00ff !important;
        box-shadow: 0 0 20px rgba(255, 0, 255, 0.5) !important;
    }
    
    .control-buttons {
        display: flex;
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .stButton>button {
        flex: 1;
        background: linear-gradient(45deg, #00ffff, #0080ff);
        color: black !important;
        border: none;
        border-radius: 10px;
        padding: 1rem;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s;
        box-shadow: 0 5px 15px rgba(0, 255, 255, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 255, 255, 0.6);
        background: linear-gradient(45deg, #00ffaa, #00ffff);
    }
    
    .stop-button {
        background: linear-gradient(45deg, #ff0000, #ff5500) !important;
    }
    
    .stop-button:hover {
        background: linear-gradient(45deg, #ff5500, #ff0000) !important;
    }
    
    .stats-container {
        background: rgba(0, 0, 0, 0.6);
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid #00ffaa;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
    }
    
    .stat-box {
        background: rgba(0, 40, 80, 0.6);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #0080ff;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(45deg, #00ffff, #ff00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        color: #00ffaa;
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    .log-container {
        background: rgba(0, 0, 0, 0.8);
        color: #00ffff;
        padding: 1rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        height: 400px;
        overflow-y: auto;
        border: 1px solid #00ffff;
        margin-top: 1.5rem;
    }
    
    .log-entry {
        padding: 0.3rem 0;
        border-bottom: 1px solid rgba(0, 255, 255, 0.2);
        animation: fadeIn 0.5s;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateX(-10px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .log-time {
        color: #00ffaa;
        margin-right: 10px;
    }
    
    .log-message {
        color: white;
    }
    
    .success-log {
        color: #00ffaa !important;
    }
    
    .error-log {
        color: #ff5555 !important;
    }
    
    .warning-log {
        color: #ffff00 !important;
    }
    
    .file-uploader {
        border: 2px dashed #00ffff;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        background: rgba(0, 20, 40, 0.6);
    }
    
    .running-animation {
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(0, 255, 255, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(0, 255, 255, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 255, 255, 0); }
    }
    
    .session-info {
        background: rgba(0, 0, 0, 0.6);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #ff00ff;
    }
    
    .watermark {
        text-align: center;
        color: rgba(0, 255, 255, 0.3);
        font-size: 0.9rem;
        margin-top: 2rem;
        padding: 1rem;
    }
</style>
"""

st.set_page_config(
    page_title="JACKSON AUTO BOT",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(custom_css, unsafe_allow_html=True)

# Initialize session state
if 'automation_running' not in st.session_state:
    st.session_state.automation_running = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0
if 'session_start_time' not in st.session_state:
    st.session_state.session_start_time = datetime.now()
if 'current_task' not in st.session_state:
    st.session_state.current_task = None

class AutomationEngine:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.message_index = 0
        self.driver = None
        self.task_thread = None
        
    def log(self, message, type="info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs.append((timestamp, message, type))
        st.session_state.logs = self.logs[-100:]  # Keep last 100 logs
        
    def setup_browser(self):
        try:
            self.log("🛠️ Setting up Chrome browser...")
            
            chrome_options = Options()
            chrome_options.add_argument('--headless=new')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-setuid-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
            
            # Try to find Chromium/Chrome
            chromium_paths = [
                '/usr/bin/chromium',
                '/usr/bin/chromium-browser',
                '/usr/bin/google-chrome',
                '/usr/bin/chrome'
            ]
            
            for path in chromium_paths:
                if Path(path).exists():
                    chrome_options.binary_location = path
                    self.log(f"✅ Found browser at: {path}")
                    break
            
            # Try to find ChromeDriver
            driver_paths = [
                '/usr/bin/chromedriver',
                '/usr/local/bin/chromedriver'
            ]
            
            driver_path = None
            for path in driver_paths:
                if Path(path).exists():
                    driver_path = path
                    self.log(f"✅ Found driver at: {path}")
                    break
            
            try:
                from selenium.webdriver.chrome.service import Service
                
                if driver_path:
                    service = Service(executable_path=driver_path)
                    self.driver = webdriver.Chrome(service=service, options=chrome_options)
                else:
                    self.driver = webdriver.Chrome(options=chrome_options)
                
                self.driver.set_window_size(1920, 1080)
                self.log("✅ Browser setup completed!")
                return True
                
            except Exception as e:
                self.log(f"❌ Browser setup failed: {str(e)}", "error")
                return False
                
        except Exception as e:
            self.log(f"❌ Setup error: {str(e)}", "error")
            return False
    
    def find_message_input(self):
        """Find message input field on Facebook"""
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Try multiple selectors
            selectors = [
                'div[contenteditable="true"][role="textbox"]',
                'div[contenteditable="true"][data-lexical-editor="true"]',
                'div[aria-label*="message" i][contenteditable="true"]',
                'div[aria-label*="Message" i][contenteditable="true"]',
                'div[contenteditable="true"][spellcheck="true"]',
                'textarea[placeholder*="message" i]',
                '[contenteditable="true"]',
                'textarea',
                'input[type="text"]'
            ]
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        for element in elements:
                            try:
                                element.click()
                                time.sleep(0.5)
                                self.log(f"✅ Found input with selector: {selector[:30]}...")
                                return element
                            except:
                                continue
                except:
                    continue
            
            self.log("❌ Could not find message input", "error")
            return None
            
        except Exception as e:
            self.log(f"❌ Error finding input: {str(e)}", "error")
            return None
    
    def send_single_message(self, element, message):
        """Send a single message"""
        try:
            # Clear and set message
            self.driver.execute_script("""
                const elem = arguments[0];
                const msg = arguments[1];
                
                elem.focus();
                elem.click();
                
                if (elem.tagName === 'DIV') {
                    elem.textContent = msg;
                    elem.innerHTML = msg;
                } else {
                    elem.value = msg;
                }
                
                elem.dispatchEvent(new Event('input', { bubbles: true }));
                elem.dispatchEvent(new Event('change', { bubbles: true }));
            """, element, message)
            
            time.sleep(1)
            
            # Try to send
            sent = self.driver.execute_script("""
                const buttons = document.querySelectorAll('[aria-label*="Send" i], [data-testid="send-button"], button:has(svg[aria-label*="send" i])');
                
                for (let btn of buttons) {
                    if (btn.offsetParent !== null) {
                        btn.click();
                        return true;
                    }
                }
                
                // Try Enter key
                const events = [
                    new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true }),
                    new KeyboardEvent('keypress', { key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true }),
                    new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true })
                ];
                
                events.forEach(event => arguments[0].dispatchEvent(event));
                return true;
            """, element)
            
            return True
            
        except Exception as e:
            self.log(f"❌ Send error: {str(e)}", "error")
            return False
    
    def run_automation(self, config):
        """Main automation loop"""
        try:
            self.log("🚀 Starting automation...", "success")
            
            if not self.setup_browser():
                return False
            
            # Navigate to Facebook
            self.driver.get('https://www.facebook.com/')
            self.log("🌐 Navigating to Facebook...")
            time.sleep(10)
            
            # Add cookies if provided
            if config.get('cookies'):
                try:
                    cookies = config['cookies'].split(';')
                    for cookie in cookies:
                        cookie = cookie.strip()
                        if cookie and '=' in cookie:
                            name, value = cookie.split('=', 1)
                            self.driver.add_cookie({
                                'name': name.strip(),
                                'value': value.strip(),
                                'domain': '.facebook.com',
                                'path': '/'
                            })
                    self.log("🍪 Cookies added successfully")
                except Exception as e:
                    self.log(f"⚠️ Cookie error: {str(e)}", "warning")
            
            # Go to chat
            chat_id = config.get('chat_id', '').strip()
            if chat_id:
                self.driver.get(f'https://www.facebook.com/messages/t/{chat_id}')
                self.log(f"💬 Opening chat: {chat_id}")
            else:
                self.driver.get('https://www.facebook.com/messages')
                self.log("💬 Opening messages page")
            
            time.sleep(15)
            
            # Find message input
            message_input = self.find_message_input()
            if not message_input:
                self.log("❌ Cannot find message input. Stopping.", "error")
                return False
            
            # Load messages
            messages = []
            if config.get('messages_file'):
                messages = config['messages_file'].split('\n')
                messages = [m.strip() for m in messages if m.strip()]
            
            if not messages:
                messages = ["Hello! This is auto message."]
            
            self.log(f"📄 Loaded {len(messages)} messages")
            
            # Get prefix
            prefix = config.get('hatersname_prefix', '')
            delay = int(config.get('delay', 5))
            
            self.log(f"⏱️ Delay: {delay} seconds | Prefix: {prefix}")
            
            # Start sending messages
            message_count = 0
            self.message_index = 0
            
            while self.running:
                # Get next message
                current_message = messages[self.message_index % len(messages)]
                full_message = f"{prefix} {current_message}" if prefix else current_message
                
                # Send message
                self.log(f"📤 Sending: {full_message[:50]}...")
                if self.send_single_message(message_input, full_message):
                    message_count += 1
                    st.session_state.message_count = message_count
                    self.message_count = message_count
                    self.message_index += 1
                    
                    self.log(f"✅ Sent #{message_count}: {full_message[:30]}...", "success")
                    
                    # Check if still running
                    if not self.running:
                        break
                    
                    # Wait for delay
                    for _ in range(delay):
                        if not self.running:
                            break
                        time.sleep(1)
                else:
                    self.log("❌ Failed to send message", "error")
                    break
            
            self.log(f"🛑 Automation stopped. Total sent: {message_count}", "success")
            return True
            
        except Exception as e:
            self.log(f"💥 Fatal error: {str(e)}", "error")
            return False
        finally:
            if self.driver:
                try:
                    self.driver.quit()
                    self.log("🔌 Browser closed")
                except:
                    pass
    
    def start(self, config):
        """Start automation in a thread"""
        if self.running:
            return False
        
        self.running = True
        st.session_state.automation_running = True
        
        def run_task():
            self.run_automation(config)
            self.running = False
            st.session_state.automation_running = False
        
        self.task_thread = threading.Thread(target=run_task, daemon=True)
        self.task_thread.start()
        return True
    
    def stop(self):
        """Stop automation"""
        self.running = False
        st.session_state.automation_running = False
        self.log("⏹️ Stopping automation...", "warning")

# Initialize automation engine
if 'engine' not in st.session_state:
    st.session_state.engine = AutomationEngine()

# Dashboard Header
st.markdown("""
<div class="dashboard-header">
    <h1 class="dashboard-title">JACKSON AUTO BOT</h1>
    <p style="color: #00ffaa; margin-top: 0.5rem;">Unlimited Facebook Message Automation System</p>
</div>
""", unsafe_allow_html=True)

# Main Dashboard Layout
col1, col2 = st.columns([2, 1])

with col1:
    # Configuration Section
    st.markdown("""
    <div class="input-section">
        <div class="input-label">🔧 CONFIGURATION SETUP</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat ID
    chat_id = st.text_input(
        "Facebook Chat ID",
        placeholder="Enter Facebook conversation ID from URL",
        help="Example: 100051508763156 (from m.facebook.com/messages/t/THIS_ID)"
    )
    
    # Hatersname Prefix
    hatersname_prefix = st.text_input(
        "Hatersname Prefix",
        placeholder="Example: [JACKSON XD HERE]",
        help="This will be added before each message"
    )
    
    # Delay
    delay = st.slider(
        "Delay between messages (seconds)",
        min_value=1,
        max_value=60,
        value=5,
        help="Wait time between sending messages"
    )
    
    # Cookies
    cookies = st.text_area(
        "Facebook Cookies (Optional)",
        placeholder="Paste your Facebook cookies here...",
        height=100,
        help="Format: cookie_name=cookie_value; cookie_name2=cookie_value2"
    )
    
    # Messages File
    st.markdown('<div class="input-label">📁 MESSAGES FILE (.txt)</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload text file with messages (one per line)",
        type=['txt'],
        label_visibility="collapsed"
    )
    
    # Load default messages if no file uploaded
    messages_content = ""
    if uploaded_file is not None:
        messages_content = uploaded_file.getvalue().decode("utf-8")
        st.success(f"✅ Loaded {len(messages_content.splitlines())} messages")
    else:
        st.info("📝 Upload a .txt file with messages (one per line)")

with col2:
    # Control Panel
    st.markdown("""
    <div class="input-section">
        <div class="input-label">🎮 CONTROL PANEL</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Session Info
    session_duration = datetime.now() - st.session_state.session_start_time
    hours, remainder = divmod(session_duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    st.markdown(f"""
    <div class="session-info">
        <strong>🕒 Session Duration:</strong><br>
        {hours:02d}:{minutes:02d}:{seconds:02d}<br>
        <strong>📊 Messages Sent:</strong><br>
        {st.session_state.message_count}<br>
        <strong>📈 Status:</strong><br>
        {"🟢 RUNNING" if st.session_state.automation_running else "🔴 STOPPED"}
    </div>
    """, unsafe_allow_html=True)
    
    # Control Buttons
    st.markdown('<div class="control-buttons">', unsafe_allow_html=True)
    
    col_start, col_stop = st.columns(2)
    
    with col_start:
        start_disabled = st.session_state.automation_running or not chat_id
        if st.button(
            "▶️ START BOT",
            use_container_width=True,
            disabled=start_disabled,
            help="Start automation"
        ):
            config = {
                'chat_id': chat_id,
                'hatersname_prefix': hatersname_prefix,
                'delay': delay,
                'cookies': cookies,
                'messages_file': messages_content or "Auto message from WALEED XD BOT"
            }
            
            if st.session_state.engine.start(config):
                st.success("🚀 Automation started!")
                st.rerun()
    
    with col_stop:
        if st.button(
            "⏹️ STOP BOT",
            use_container_width=True,
            disabled=not st.session_state.automation_running,
            type="secondary",
            help="Stop automation"
        ):
            st.session_state.engine.stop()
            st.warning("🛑 Stopping automation...")
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("""
    <div class="input-section">
        <div class="input-label">⚡ QUICK ACTIONS</div>
    </div>
    """, unsafe_allow_html=True)
    
    col_q1, col_q2 = st.columns(2)
    
    with col_q1:
        if st.button("📋 Copy Config", use_container_width=True):
            config_data = {
                'chat_id': chat_id,
                'prefix': hatersname_prefix,
                'delay': delay
            }
            st.code(json.dumps(config_data, indent=2))
            st.success("Config copied to clipboard!")
    
    with col_q2:
        if st.button("🔄 Refresh Logs", use_container_width=True):
            st.rerun()

# Statistics
st.markdown("""
<div class="stats-container">
    <div class="input-label">📊 LIVE STATISTICS</div>
    <div class="stats-grid">
        <div class="stat-box">
            <div class="stat-value">{:,}</div>
            <div class="stat-label">Messages Sent</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{}</div>
            <div class="stat-label">Bot Status</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{}</div>
            <div class="stat-label">Delay (seconds)</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{}</div>
            <div class="stat-label">Active Threads</div>
        </div>
    </div>
</div>
""".format(
    st.session_state.message_count,
    "🟢 RUNNING" if st.session_state.automation_running else "🔴 STOPPED",
    delay,
    "1" if st.session_state.automation_running else "0"
), unsafe_allow_html=True)

# Live Logs
st.markdown("""
<div class="input-section">
    <div class="input-label">📜 LIVE AUTOMATION LOGS</div>
</div>
""", unsafe_allow_html=True)

# Log Container
log_html = '<div class="log-container">'
if st.session_state.logs:
    for timestamp, message, log_type in st.session_state.logs[-50:]:  # Show last 50 logs
        color_class = {
            "success": "success-log",
            "error": "error-log",
            "warning": "warning-log"
        }.get(log_type, "")
        
        log_html += f'''
        <div class="log-entry">
            <span class="log-time">[{timestamp}]</span>
            <span class="log-message {color_class}">{message}</span>
        </div>
        '''
else:
    log_html += '<div style="text-align: center; padding: 50px; color: #666;">No logs yet. Start automation to see logs here.</div>'

log_html += '</div>'
st.markdown(log_html, unsafe_allow_html=True)

# Auto-refresh if running
if st.session_state.automation_running:
    time.sleep(2)
    st.rerun()

# Footer
st.markdown("""
<div class="watermark">
    🤖 JACKSON AUTO BOT v2.0 | Unlimited Message Automation | Made with 💙
</div>
""", unsafe_allow_html=True)

# Instructions
with st.expander("📖 HOW TO USE"):
    st.markdown("""
    ### **📌 Step-by-Step Guide:**
    
    1. **Get Facebook Chat ID:**
       - Open Facebook Messenger in browser
       - Open the chat you want to automate
       - Copy the ID from URL: `m.facebook.com/messages/t/100051508763156`
       - **Chat ID = `100051508763156`**
    
    2. **Prepare Messages File:**
       - Create a `.txt` file
       - Write one message per line
       - Example:
         ```
         Hello, how are you?
         This is automated message
         Testing auto bot
         ```
    
    3. **Optional - Facebook Cookies:**
       - Press F12 in browser
       - Go to Application/Storage > Cookies
       - Copy `c_user` and `xs` cookies
       - Format: `c_user=12345; xs=abcde...`
    
    4. **Start Automation:**
       - Fill all required fields
       - Click **START BOT**
       - Watch logs in real-time
    
    ### **⚠️ Important Notes:**
    - Keep browser tab open (don't close)
    - Internet connection must be stable
    - Start with high delay (10+ seconds) for testing
    - Bot runs in background - you can minimize
    
    ### **🚨 Troubleshooting:**
    - **Bot not starting?** Check Chat ID format
    - **Messages not sending?** Try adding cookies
    - **Errors in logs?** Check internet connection
    - **Slow?** Increase delay between messages
    
    ### **🛡️ Safety Tips:**
    - Don't use on main Facebook account
    - Use separate/test account
    - Start with long delays
    - Monitor bot activity
    """)

# Hidden debug section (Ctrl+Shift+D to show)
with st.sidebar:
    if st.checkbox("🔧 Debug Mode", False):
        st.markdown("### Debug Information")
        st.json({
            "automation_running": st.session_state.automation_running,
            "message_count": st.session_state.message_count,
            "logs_count": len(st.session_state.logs),
            "session_duration": str(session_duration),
            "chat_id_provided": bool(chat_id),
            "messages_loaded": bool(messages_content),
            "cookies_provided": bool(cookies)
        })
        
        if st.button("Clear Logs"):
            st.session_state.logs = []
            st.rerun()
        
        if st.button("Reset Counter"):
            st.session_state.message_count = 0
            st.rerun()
