"""
Cyberpunk theme styling for NeuralSprint application
"""

import streamlit as st

def apply_cyber_theme():
    """Apply cyberpunk-themed CSS styling to the Streamlit app"""
    
    st.markdown("""
    <style>
    /* Global cyberpunk theme variables */
    :root {
        --cyber-primary: #00ff88;
        --cyber-secondary: #ff0080;
        --cyber-accent: #00d4ff;
        --cyber-warning: #ffff00;
        --cyber-error: #ff4444;
        --cyber-success: #00ff88;
        --cyber-bg-dark: #0a0a0a;
        --cyber-bg-medium: #1a1a1a;
        --cyber-bg-light: #2a2a2a;
        --cyber-text: #ffffff;
        --cyber-text-dim: #888888;
        --cyber-border: #333333;
        --cyber-glow: 0 0 10px;
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        border-radius: 10px;
        margin: 1rem;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a1a 0%, #0a0a0a 100%);
        border-right: 2px solid var(--cyber-primary);
        box-shadow: 5px 0 15px rgba(0, 255, 136, 0.2);
    }
    
    /* Header and title styling */
    h1, h2, h3 {
        color: var(--cyber-primary) !important;
        text-shadow: var(--cyber-glow) var(--cyber-primary);
        font-family: 'Courier New', monospace;
        font-weight: bold;
        letter-spacing: 1px;
    }
    
    h1 {
        font-size: 2.5rem !important;
        margin-bottom: 1rem;
        text-align: center;
        background: linear-gradient(45deg, #00ff88, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Metric cards styling */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        border: 1px solid var(--cyber-primary);
        border-radius: 8px;
        padding: 1rem;
        box-shadow: var(--cyber-glow) rgba(0, 255, 136, 0.3);
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        border-color: var(--cyber-accent);
        box-shadow: var(--cyber-glow) rgba(0, 212, 255, 0.4);
        transform: translateY(-2px);
    }
    
    [data-testid="metric-container"] > div {
        color: var(--cyber-text) !important;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: var(--cyber-primary) !important;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        font-size: 1.8rem !important;
        text-shadow: var(--cyber-glow) var(--cyber-primary);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #1a1a1a, #2a2a2a);
        border: 2px solid var(--cyber-primary);
        color: var(--cyber-primary) !important;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: var(--cyber-glow) rgba(0, 255, 136, 0.2);
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #2a2a2a, #3a3a3a);
        border-color: var(--cyber-accent);
        color: var(--cyber-accent) !important;
        box-shadow: var(--cyber-glow) rgba(0, 212, 255, 0.4);
        transform: translateY(-1px);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
        box-shadow: var(--cyber-glow) rgba(0, 255, 136, 0.6);
    }
    
    /* Input field styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        background: #1a1a1a !important;
        border: 2px solid #333333 !important;
        color: var(--cyber-text) !important;
        border-radius: 6px !important;
        font-family: 'Courier New', monospace;
        padding: 0.5rem !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--cyber-primary) !important;
        box-shadow: var(--cyber-glow) rgba(0, 255, 136, 0.3) !important;
        outline: none !important;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--cyber-primary), var(--cyber-accent)) !important;
        border-radius: 10px;
        box-shadow: var(--cyber-glow) rgba(0, 255, 136, 0.4);
    }
    
    .stProgress > div > div {
        background: #333333 !important;
        border-radius: 10px;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: #1a1a1a;
        border-radius: 6px;
        padding: 4px;
        border: 1px solid #333333;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: 1px solid transparent;
        color: var(--cyber-text-dim);
        font-family: 'Courier New', monospace;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #2a2a2a, #3a3a3a);
        border-color: var(--cyber-primary);
        color: var(--cyber-primary) !important;
        box-shadow: var(--cyber-glow) rgba(0, 255, 136, 0.3);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #2a2a2a;
        color: var(--cyber-accent) !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(45deg, #1a1a1a, #2a2a2a);
        border: 1px solid #333333;
        border-radius: 6px;
        color: var(--cyber-text) !important;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: var(--cyber-primary);
        box-shadow: var(--cyber-glow) rgba(0, 255, 136, 0.2);
    }
    
    .streamlit-expanderContent {
        background: #1a1a1a;
        border: 1px solid #333333;
        border-top: none;
        border-radius: 0 0 6px 6px;
        padding: 1rem;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background: #1a1a1a;
        border: 1px solid #333333;
        border-radius: 6px;
        overflow: hidden;
    }
    
    .stDataFrame table {
        color: var(--cyber-text) !important;
        font-family: 'Courier New', monospace;
    }
    
    .stDataFrame th {
        background: #2a2a2a !important;
        color: var(--cyber-primary) !important;
        border-bottom: 2px solid var(--cyber-primary) !important;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stDataFrame td {
        border-bottom: 1px solid #333333 !important;
        padding: 0.5rem !important;
    }
    
    .stDataFrame tr:hover {
        background: rgba(0, 255, 136, 0.05) !important;
    }
    
    /* Alert and message styling */
    .stAlert {
        border-radius: 6px;
        border-left: 4px solid;
        font-family: 'Courier New', monospace;
        font-weight: bold;
    }
    
    .stAlert[data-baseweb="notification"] {
        background: rgba(0, 255, 136, 0.1);
        border-left-color: var(--cyber-success);
        color: var(--cyber-success);
    }
    
    .stAlert[data-baseweb="notification"][kind="error"] {
        background: rgba(255, 68, 68, 0.1);
        border-left-color: var(--cyber-error);
        color: var(--cyber-error);
    }
    
    .stAlert[data-baseweb="notification"][kind="warning"] {
        background: rgba(255, 255, 0, 0.1);
        border-left-color: var(--cyber-warning);
        color: var(--cyber-warning);
    }
    
    /* Checkbox and radio styling */
    .stCheckbox > label {
        color: var(--cyber-text) !important;
        font-family: 'Courier New', monospace;
    }
    
    .stRadio > label {
        color: var(--cyber-text) !important;
        font-family: 'Courier New', monospace;
    }
    
    /* Selectbox dropdown styling */
    .stSelectbox [data-baseweb="select"] {
        background: #1a1a1a;
        border: 2px solid #333333;
        border-radius: 6px;
    }
    
    .stSelectbox [data-baseweb="select"]:hover {
        border-color: var(--cyber-primary);
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background: #333333;
    }
    
    .stSlider > div > div > div > div {
        background: var(--cyber-primary);
        box-shadow: var(--cyber-glow) rgba(0, 255, 136, 0.4);
    }
    
    /* File uploader styling */
    .stFileUploader {
        background: #1a1a1a;
        border: 2px dashed #333333;
        border-radius: 6px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: var(--cyber-primary);
        background: rgba(0, 255, 136, 0.05);
    }
    
    /* Code block styling */
    .stCode {
        background: #0a0a0a !important;
        border: 1px solid var(--cyber-primary) !important;
        border-radius: 6px !important;
        color: var(--cyber-primary) !important;
        font-family: 'Courier New', monospace !important;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-top-color: var(--cyber-primary) !important;
        border-right-color: var(--cyber-accent) !important;
    }
    
    /* Custom glow effects */
    .cyber-glow {
        box-shadow: var(--cyber-glow) var(--cyber-primary);
        animation: pulse-glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes pulse-glow {
        from {
            box-shadow: 0 0 5px var(--cyber-primary);
        }
        to {
            box-shadow: 0 0 20px var(--cyber-primary), 0 0 30px var(--cyber-primary);
        }
    }
    
    /* Status indicator styling */
    .status-online {
        color: var(--cyber-success) !important;
        text-shadow: var(--cyber-glow) var(--cyber-success);
    }
    
    .status-offline {
        color: var(--cyber-error) !important;
        text-shadow: var(--cyber-glow) var(--cyber-error);
    }
    
    .status-warning {
        color: var(--cyber-warning) !important;
        text-shadow: var(--cyber-glow) var(--cyber-warning);
    }
    
    /* Custom scroll bar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--cyber-primary);
        border-radius: 4px;
        box-shadow: var(--cyber-glow) rgba(0, 255, 136, 0.3);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--cyber-accent);
        box-shadow: var(--cyber-glow) rgba(0, 212, 255, 0.4);
    }
    
    /* Hide Streamlit footer and menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom classes for specific components */
    .metric-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        border: 1px solid var(--cyber-primary);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: var(--cyber-glow) rgba(0, 255, 136, 0.2);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--cyber-glow) rgba(0, 255, 136, 0.4);
    }
    
    .cyber-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        border: 1px solid #333333;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .cyber-card:hover {
        border-color: var(--cyber-primary);
        box-shadow: var(--cyber-glow) rgba(0, 255, 136, 0.2);
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .status-indicator.online {
        background: var(--cyber-success);
        box-shadow: 0 0 6px var(--cyber-success);
    }
    
    .status-indicator.offline {
        background: var(--cyber-error);
        box-shadow: 0 0 6px var(--cyber-error);
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Terminal-style text */
    .terminal-text {
        font-family: 'Courier New', monospace;
        color: var(--cyber-primary);
        background: #0a0a0a;
        padding: 1rem;
        border-radius: 6px;
        border: 1px solid var(--cyber-primary);
        white-space: pre-wrap;
        overflow-x: auto;
    }
    
    /* Cyber button variants */
    .cyber-button-primary {
        background: linear-gradient(45deg, var(--cyber-primary), var(--cyber-accent));
        border: none;
        color: #000000 !important;
        font-weight: bold;
        text-shadow: none;
    }
    
    .cyber-button-secondary {
        background: transparent;
        border: 2px solid var(--cyber-secondary);
        color: var(--cyber-secondary) !important;
    }
    
    .cyber-button-secondary:hover {
        background: var(--cyber-secondary);
        color: #000000 !important;
    }
    
    /* Matrix-style background animation */
    @keyframes matrix {
        0% { transform: translateY(-100vh); }
        100% { transform: translateY(100vh); }
    }
    
    .matrix-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        opacity: 0.1;
    }
    
    /* Responsive design adjustments */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
            margin: 0.5rem;
        }
        
        h1 {
            font-size: 2rem !important;
        }
        
        .stButton > button {
            font-size: 0.8rem;
            padding: 0.4rem 0.8rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_cyber_metric_card(title: str, value: str, delta: str = None, help_text: str = None):
    """Create a cyberpunk-styled metric card"""
    delta_html = ""
    if delta:
        delta_color = "#00ff88" if delta.startswith("+") else "#ff4444" if delta.startswith("-") else "#ffff00"
        delta_html = f'<div style="color: {delta_color}; font-size: 0.8rem; margin-top: 0.2rem;">{delta}</div>'
    
    help_html = ""
    if help_text:
        help_html = f'<div style="color: #888; font-size: 0.7rem; margin-top: 0.5rem;">{help_text}</div>'
    
    return f"""
    <div class="metric-card">
        <div style="color: #888; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;">
            {title}
        </div>
        <div style="color: #00ff88; font-size: 1.8rem; font-weight: bold; font-family: 'Courier New', monospace; text-shadow: 0 0 10px #00ff88;">
            {value}
        </div>
        {delta_html}
        {help_html}
    </div>
    """

def create_status_indicator(status: str, text: str = ""):
    """Create a status indicator with optional text"""
    status_class = {
        "online": "online",
        "offline": "offline", 
        "warning": "warning",
        "active": "online",
        "inactive": "offline"
    }.get(status.lower(), "offline")
    
    return f"""
    <div style="display: flex; align-items: center; margin: 0.5rem 0;">
        <span class="status-indicator {status_class}"></span>
        <span style="color: #fff; font-family: 'Courier New', monospace;">{text}</span>
    </div>
    """

def create_cyber_card(content: str, title: str = None, border_color: str = "#333333"):
    """Create a cyberpunk-styled content card"""
    title_html = ""
    if title:
        title_html = f"""
        <div style="color: #00ff88; font-weight: bold; font-family: 'Courier New', monospace; 
                    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1rem; 
                    border-bottom: 1px solid {border_color}; padding-bottom: 0.5rem;">
            {title}
        </div>
        """
    
    return f"""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%); 
                border: 1px solid {border_color}; border-radius: 8px; padding: 1.5rem; 
                margin: 1rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);">
        {title_html}
        <div style="color: #fff;">
            {content}
        </div>
    </div>
    """

def create_terminal_output(text: str, prompt: str = "neural@sprint:~$"):
    """Create terminal-style output display"""
    return f"""
    <div class="terminal-text">
{prompt} {text}
    </div>
    """

def apply_custom_button_style(label: str, style: str = "primary", key: str = None):
    """Apply custom styling to Streamlit buttons"""
    style_classes = {
        "primary": "cyber-button-primary",
        "secondary": "cyber-button-secondary"
    }
    
    # This function would be used with st.markdown to create custom styled buttons
    # Since Streamlit doesn't allow direct button styling, this is for reference
    return f'<button class="{style_classes.get(style, "")}">{label}</button>'

def create_progress_bar(value: int, max_value: int = 100, color: str = "#00ff88", height: str = "20px"):
    """Create a custom cyberpunk progress bar"""
    percentage = (value / max_value) * 100
    
    return f"""
    <div style="background: #333; border-radius: 10px; height: {height}; overflow: hidden; 
                border: 1px solid {color}; box-shadow: 0 0 10px {color};">
        <div style="background: linear-gradient(90deg, {color}, #00d4ff); 
                    height: 100%; width: {percentage}%; border-radius: 9px;
                    box-shadow: 0 0 15px {color}; transition: width 0.3s ease;">
        </div>
    </div>
    <div style="color: {color}; font-family: 'Courier New', monospace; 
                font-size: 0.8rem; margin-top: 0.5rem; text-align: center;">
        {value}/{max_value} ({percentage:.1f}%)
    </div>
    """

def create_glow_text(text: str, color: str = "#00ff88"):
    """Create glowing text effect"""
    return f"""
    <span style="color: {color}; text-shadow: 0 0 10px {color}, 0 0 20px {color}; 
                 font-family: 'Courier New', monospace; font-weight: bold;">
        {text}
    </span>
    """
