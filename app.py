# app.py
import streamlit as st

st.set_page_config(
    page_title="Đăng nhập - Quản lý tài liệu",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Document Manager Pro - Quản lý tài liệu chuyên nghiệp"
    }
)

from utils.db import supabase
from utils import auth

# Load custom CSS
def load_css():
    try:
        with open('styles/custom.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass # Fallback if CSS file is not found

load_css()

# Hide sidebar on login page
st.markdown("""<style>
    [data-testid="stSidebar"]
    {
        display: none;
    }
</style>""", unsafe_allow_html=True)

# Initialize session state
if 'user_session' not in st.session_state:
    st.session_state.user_session = None

# --- MODERN LOGIN INTERFACE ---
if not st.session_state.user_session:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; margin-bottom: 2rem;">
        <h1 style="font-size: 3.5rem; margin-bottom: 0.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            📚 Document Manager Pro
        </h1>
        <p style="font-size: 1.2rem; color: var(--text-secondary); font-weight: 300;">
            Hệ thống quản lý tài liệu thông minh và hiện đại
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["🔐 Đăng nhập", "📝 Đăng ký"])
        
        with tab1:
            st.markdown('<div class="main-container animated-card">', unsafe_allow_html=True)
            with st.form("login_form", clear_on_submit=False):
                st.markdown("### Chào mừng trở lại!")
                email = st.text_input("📧 Email", placeholder="your.email@example.com")
                password = st.text_input("🔒 Mật khẩu", type="password", placeholder="Nhập mật khẩu của bạn")
                login_button = st.form_submit_button("🚀 Đăng nhập", use_container_width=True)
                
                if login_button:
                    if email and password:
                        with st.spinner('Đang xác thực...'):
                            try:
                                session = supabase.auth.sign_in_with_password({"email": email, "password": password})
                                st.session_state.user_session = session
                                st.success("Đăng nhập thành công! 🎉")
                                st.balloons()
                                st.cache_resource.clear()
                                st.session_state.user_session = session
                                auth.nav_page("Tài_liệu_của_tôi")
                            except Exception as e:
                                st.error(f"❌ Đăng nhập thất bại: {e}")
                    else:
                        st.warning("⚠️ Vui lòng điền đầy đủ thông tin")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="main-container animated-card">', unsafe_allow_html=True)
            with st.form("signup_form", clear_on_submit=True):
                st.markdown("### Tạo tài khoản mới")
                email = st.text_input("📧 Email", placeholder="your.email@example.com")
                password = st.text_input("🔒 Mật khẩu", type="password", placeholder="Ít nhất 6 ký tự", help="Mật khẩu phải có ít nhất 6 ký tự")
                confirm_password = st.text_input("🔒 Xác nhận mật khẩu", type="password", placeholder="Nhập lại mật khẩu")
                signup_button = st.form_submit_button("✨ Tạo tài khoản", use_container_width=True)
                
                if signup_button:
                    if not all([email, password, confirm_password]):
                        st.warning("⚠️ Vui lòng điền đầy đủ thông tin")
                    elif password != confirm_password:
                        st.error("❌ Mật khẩu xác nhận không khớp")
                    elif len(password) < 6:
                        st.error("❌ Mật khẩu phải có ít nhất 6 ký tự")
                    else:
                        with st.spinner('Đang tạo tài khoản...'):
                            try:
                                session = supabase.auth.sign_up({"email": email, "password": password})
                                st.success("🎉 Đăng ký thành công!")
                                st.info("📧 Vui lòng kiểm tra email để xác thực tài khoản")
                                st.balloons()
                            except Exception as e:
                                st.error(f"❌ Đăng ký thất bại: {e}")
            st.markdown('</div>', unsafe_allow_html=True)
else:
    auth.nav_page("Tài_liệu_của_tôi")