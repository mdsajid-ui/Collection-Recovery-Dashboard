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

    /* Hide Streamlit Header, Footer, and Toolbar */
    #MainMenu, footer, header, [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
    }

    /* Force Full Bleed Deep Black Background */
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"] {
        background-color: #050505 !important;
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .main .block-container, [data-testid="stMainBlockContainer"] {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100vw !important;
        width: 100vw !important;
    }

    /* Iframe matches exact viewport below the 36px topbar */
    [data-testid="stCustomComponentV1"] {
        width: 100vw !important;
        max-width: 100vw !important;
        height: calc(100vh - 36px) !important;
        max-height: calc(100vh - 36px) !important;
        overflow: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    iframe {
        border: none !important;
        width: 100vw !important;
        max-width: 100vw !important;
        height: calc(100vh - 36px) !important;
        max-height: calc(100vh - 36px) !important;
        display: block !important;
    }

    /* --- Luxury Gold Login Form Styling --- */
    form[data-testid="stForm"] {
        background: linear-gradient(165deg, #141414, #0A0A0A) !important;
        border: 1px solid rgba(255, 215, 0, 0.32) !important;
        box-shadow: 0 0 35px rgba(255, 215, 0, 0.12), 0 20px 50px rgba(0, 0, 0, 0.8) !important;
        border-radius: 16px !important;
        padding: 28px 24px 22px !important;
        max-width: 380px !important;
        width: 100% !important;
        margin: 4vh auto 0 !important;
    }

    /* Inputs override */
    div[data-baseweb="input"] {
        background-color: #0E0E0E !important;
        border: 1px solid rgba(255, 215, 0, 0.25) !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
        height: 40px !important;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: #FFD700 !important;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.35) !important;
    }
    div[data-baseweb="input"] input {
        color: #FFFFFF !important;
        background-color: transparent !important;
        font-size: 13px !important;
    }
    label[data-testid="stWidgetLabel"] p {
        color: #D4AF37 !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        margin-bottom: 2px !important;
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
        height: 38px !important;
        font-size: 12px !important;
        margin-top: 8px !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.25) !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stForm"] div.stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.4) !important;
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
    _, center_col, _ = st.columns([1, 1.8, 1])
    with center_col:
        with st.form("portal_login_form", clear_on_submit=False):
            st.markdown("""
            <div style="text-align: center; margin-bottom: 16px;">
                <span style="display:inline-block; background:linear-gradient(135deg,#FFD700,#E6B566); color:#0A0A0A; font-weight:800; font-size:10px; letter-spacing:1.5px; text-transform:uppercase; padding:3px 12px; border-radius:20px; margin-bottom:10px;">Protected Portal</span>
                <h1 style="font-family:'Playfair Display',serif; font-size:24px; font-weight:700; color:#FFFFFF; margin:0 0 4px 0; letter-spacing:0.5px;">i-PMS <span style="background:linear-gradient(135deg,#FFF3C4,#FFD700 55%,#E6B566); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">Recovery</span></h1>
                <p style="font-size:11.5px; color:#BDBDBD; margin:0; letter-spacing:0.3px;">Collection & Recovery Management System</p>
            </div>
            """, unsafe_allow_html=True)

            entered_user = st.text_input("Username", placeholder="Enter username")
            entered_pass = st.text_input("Password", type="password", placeholder="Enter password")
            submitted = st.form_submit_button("Sign In Securely", use_container_width=True)

            if submitted:
                if entered_user == valid_username and entered_pass == valid_password:
                    st.session_state.authenticated = True
                    st.session_state.logged_in_user = entered_user
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please verify your username and password.")

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

    # Load and render dashboard
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        components.html(html_content, scrolling=False)

    except FileNotFoundError:
        st.error(f"Error: Could not locate dashboard template file at {html_path}")
