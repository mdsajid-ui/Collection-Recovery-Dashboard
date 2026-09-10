import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(
    page_title="i-PMS | Collection & Recovery Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------------------------
# Credentials (From Streamlit Secrets or Environment Variables)
# ---------------------------------------------------------------------------
DEFAULT_USER = "admin"
DEFAULT_PASS = "admin123"

valid_username = st.secrets.get("APP_USERNAME", os.environ.get("APP_USERNAME", DEFAULT_USER))
valid_password = st.secrets.get("APP_PASSWORD", os.environ.get("APP_PASSWORD", DEFAULT_PASS))

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ---------------------------------------------------------------------------
# Global Styling (Zero-margin, Full-bleed, Dark Theme)
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600;700&display=swap');

    /* Hide Streamlit Header, Footer, and Toolbar */
    #MainMenu, footer, header, [data-testid="stHeader"], [data-testid="stToolbar"] {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
    }

    /* Force Full Bleed Deep Black Background */
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"] {
        background-color: #050505 !important;
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Remove Streamlit default container padding */
    .main .block-container, [data-testid="stMainBlockContainer"] {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100vw !important;
        width: 100vw !important;
    }

    /* Remove iframe borders and margins */
    iframe {
        border: none !important;
        width: 100vw !important;
        height: 100vh !important;
        display: block !important;
    }

    /* --- Luxury Gold Login Form Styling --- */
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding-top: 8vh;
    }
    .login-card {
        background: linear-gradient(165deg, #141414, #0A0A0A);
        border: 1px solid rgba(255, 215, 0, 0.28);
        box-shadow: 0 0 35px rgba(255, 215, 0, 0.15), 0 20px 50px rgba(0, 0, 0, 0.8);
        border-radius: 16px;
        padding: 36px 32px 28px;
        max-width: 440px;
        width: 100%;
        text-align: center;
    }
    .login-badge {
        display: inline-block;
        background: linear-gradient(135deg, #FFD700, #E6B566);
        color: #0A0A0A;
        font-weight: 800;
        font-size: 11px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        padding: 5px 14px;
        border-radius: 20px;
        margin-bottom: 14px;
    }
    .login-title {
        font-family: 'Playfair Display', serif;
        font-size: 26px;
        font-weight: 700;
        color: #FFFFFF;
        margin: 0 0 6px 0;
        letter-spacing: 0.5px;
    }
    .login-sub {
        font-size: 12px;
        color: #BDBDBD;
        margin-bottom: 24px;
        letter-spacing: 0.4px;
    }

    /* Streamlit input dark override */
    div[data-baseweb="input"] {
        background-color: #0E0E0E !important;
        border: 1px solid rgba(255, 215, 0, 0.25) !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: #FFD700 !important;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.35) !important;
    }
    div[data-baseweb="input"] input {
        color: #FFFFFF !important;
        background-color: transparent !important;
    }
    label[data-testid="stWidgetLabel"] p {
        color: #D4AF37 !important;
        font-size: 11.5px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
    }

    /* Submit Button styling */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #FFD700, #E6B566) !important;
        color: #050505 !important;
        border: none !important;
        font-weight: 700 !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
        padding: 10px 24px !important;
        border-radius: 8px !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.25) !important;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.45) !important;
    }

    /* Top Navigation bar when authenticated */
    .auth-topbar {
        background: #0A0A0A;
        border-bottom: 1px solid rgba(255, 215, 0, 0.2);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 24px;
    }
    .auth-topbar-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 13px;
        font-weight: 600;
        color: #E6B566;
    }
    .auth-badge {
        background: rgba(51, 196, 129, 0.15);
        color: #33C481;
        border: 1px solid rgba(51, 196, 129, 0.3);
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# LOGIN GATE
# ---------------------------------------------------------------------------
if not st.session_state.authenticated:
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        st.markdown("""
        <div class="login-container">
            <div class="login-card">
                <span class="login-badge">Protected Portal</span>
                <h1 class="login-title">i-PMS <span>Recovery</span></h1>
                <p class="login-sub">Collection & Recovery Management System</p>
        """, unsafe_allow_html=True)

        with st.form("portal_login_form"):
            entered_user = st.text_input("Username", placeholder="Enter username")
            entered_pass = st.text_input("Password", type="password", placeholder="Enter password")
            submitted = st.form_submit_button("Sign In Securely")

            if submitted:
                if entered_user == valid_username and entered_pass == valid_password:
                    st.session_state.authenticated = True
                    st.session_state.logged_in_user = entered_user
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        st.markdown("""
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# AUTHENTICATED: FULL-BLEED DASHBOARD
# ---------------------------------------------------------------------------
else:
    # Sleek header bar with logout option
    col_info, col_btn = st.columns([9, 1])
    with col_info:
        st.markdown(f"""
        <div class="auth-topbar">
            <div class="auth-topbar-brand">
                <span>🛡️ <b>i-PMS</b> &bull; Collection &amp; Recovery Executive Dashboard</span>
                <span class="auth-badge">AUTHENTICATED</span>
            </div>
            <div style="font-size: 12px; color: #888;">
                Logged in as: <b style="color: #FFD700;">{st.session_state.get('logged_in_user', valid_username)}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_btn:
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # Load and render the full interactive dashboard without white frames
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        components.html(html_content, height=1350, scrolling=True)

    except FileNotFoundError:
        st.error(f"Error: Could not locate dashboard template file at {html_path}")
