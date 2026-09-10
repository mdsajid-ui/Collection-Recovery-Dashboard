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
# Global Styling
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600;700&display=swap');

    /* Hide all Streamlit chrome */
    #MainMenu, footer, header, [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
    }

    /* Lock root containers to 100vh - PREVENT OUTER PAGE SCROLL */
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"] {
        background-color: #050505 !important;
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
        overflow: hidden !important;
        height: 100vh !important;
        max-height: 100vh !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .main .block-container, [data-testid="stMainBlockContainer"] {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100vw !important;
        width: 100vw !important;
        height: 100vh !important;
        max-height: 100vh !important;
        overflow: hidden !important;
    }

    /* Iframe and its wrapper match exact viewport */
    [data-testid="stCustomComponentV1"] {
        width: 100vw !important;
        max-width: 100vw !important;
        height: calc(100vh - 38px) !important;
        max-height: calc(100vh - 38px) !important;
        overflow: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    iframe {
        border: none !important;
        width: 100vw !important;
        max-width: 100vw !important;
        height: calc(100vh - 38px) !important;
        max-height: calc(100vh - 38px) !important;
        display: block !important;
    }

    /* --- Luxury Gold Login Form Styling --- */
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 85vh;
    }
    .login-card {
        background: linear-gradient(165deg, #141414, #0A0A0A);
        border: 1px solid rgba(255, 215, 0, 0.28);
        box-shadow: 0 0 35px rgba(255, 215, 0, 0.15), 0 20px 50px rgba(0, 0, 0, 0.8);
        border-radius: 16px;
        padding: 36px 32px 28px;
        max-width: 420px;
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
    .login-title span {
        background: linear-gradient(135deg, #FFF3C4, #FFD700 55%, #E6B566);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .login-sub {
        font-size: 12px;
        color: #BDBDBD;
        margin-bottom: 24px;
        letter-spacing: 0.4px;
    }

    /* Inputs override */
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

    /* Login Submit Button */
    div[data-testid="stForm"] div.stButton > button {
        background: linear-gradient(135deg, #FFD700, #E6B566) !important;
        color: #050505 !important;
        border: none !important;
        font-weight: 700 !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
        border-radius: 8px !important;
        width: 100% !important;
        height: 42px !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.25) !important;
    }

    /* Minimalist Elegant Logout Button in Header */
    div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button {
        background: transparent !important;
        color: #E6B566 !important;
        border: 1px solid rgba(255, 215, 0, 0.3) !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        padding: 2px 14px !important;
        height: 26px !important;
        min-height: 26px !important;
        line-height: 22px !important;
        border-radius: 5px !important;
        margin-top: 5px !important;
        width: auto !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button:hover {
        background: rgba(255, 215, 0, 0.15) !important;
        border-color: #FFD700 !important;
        color: #FFD700 !important;
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
                    st.error("Invalid credentials. Please verify your username and password.")

        st.markdown("""
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# AUTHENTICATED: VIEWPORT-LOCKED FULL-BLEED DASHBOARD
# ---------------------------------------------------------------------------
else:
    # Slim 36px top navigation bar
    top_col, logout_col = st.columns([11, 1])
    with top_col:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:12px;height:36px;padding:0 18px;background:#080808;border-bottom:1px solid rgba(255,215,0,0.18);font-size:11.5px;color:#A0A0A0;">
            <span style="color:#FFD700;font-weight:700;letter-spacing:0.5px;">🛡️ i-PMS</span>
            <span style="color:rgba(255,215,0,0.25);">|</span>
            <span>Collection & Recovery Executive Dashboard</span>
            <span style="background:rgba(51,196,129,0.12);color:#33C481;border:1px solid rgba(51,196,129,0.25);padding:1px 8px;border-radius:10px;font-size:9.5px;font-weight:700;">AUTHENTICATED</span>
            <span style="margin-left:auto;color:#777;font-size:11px;">User: <b style="color:#FFD700;">{st.session_state.get('logged_in_user', valid_username)}</b></span>
        </div>
        """, unsafe_allow_html=True)

    with logout_col:
        if st.button("Logout", key="btn_logout"):
            st.session_state.authenticated = False
            st.rerun()

    # Load and render dashboard (exact viewport height)
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        components.html(html_content, scrolling=False)

    except FileNotFoundError:
        st.error(f"Error: Could not locate dashboard template file at {html_path}")
