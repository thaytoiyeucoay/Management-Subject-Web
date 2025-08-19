# app.py - Document Management System
import streamlit as st
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="📚 Document Manager Pro",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import modules
from core.auth import AuthManager
from core.database import DatabaseManager
from core.ui import UIManager
from core.config import Config

# Initialize managers
@st.cache_resource
def init_managers():
    """Initialize all system managers"""
    config = Config()
    auth_manager = AuthManager(config)
    db_manager = DatabaseManager(config)
    ui_manager = UIManager()
    return auth_manager, db_manager, ui_manager

auth_manager, db_manager, ui_manager = init_managers()

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# Apply theme
ui_manager.apply_theme(st.session_state.theme)

# Load CSS (after theme applied for correct variables)
ui_manager.load_css()

# Main application logic
def main():
    """Main application entry point"""
    
    # Check authentication
    if not st.session_state.authenticated:
        show_login_page()
    else:
        show_main_app()

def show_login_page():
    """Display login/register interface"""
    ui_manager.hide_sidebar()
    
    # Header
    st.markdown("""
    <div class="hero-header">
        <h1>📚 Document Manager Pro</h1>
        <p>Hệ thống quản lý tài liệu thông minh và hiện đại</p>
    </div>
    """, unsafe_allow_html=True)

    # Theme toggle on login screen
    with st.container():
        col_t1, col_t2, col_t3 = st.columns([1,1,1])
        with col_t3:
            selected = ui_manager.render_theme_toggle(st.session_state.theme)
            if selected != st.session_state.theme:
                st.session_state.theme = selected
                ui_manager.apply_theme(selected)
                st.rerun()
    
    # Login/Register tabs
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔐 Đăng nhập", "📝 Đăng ký"])
        
        with tab1:
            handle_login()
        
        with tab2:
            handle_register()

def handle_login():
    """Handle user login"""
    with st.container():
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("### Chào mừng trở lại!")
            
            email = st.text_input(
                "📧 Email", 
                placeholder="your.email@example.com",
                key="login_email"
            )
            
            password = st.text_input(
                "🔒 Mật khẩu", 
                type="password",
                placeholder="Nhập mật khẩu của bạn",
                key="login_password"
            )
            
            login_btn = st.form_submit_button("🚀 Đăng nhập", use_container_width=True)
            
            if login_btn:
                if email and password:
                    with st.spinner('Đang xác thực...'):
                        result = auth_manager.login(email, password)
                        if result['success']:
                            st.session_state.authenticated = True
                            st.session_state.user_data = result['user']
                            st.success("Đăng nhập thành công! 🎉")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(f"❌ {result['message']}")
                else:
                    st.warning("⚠️ Vui lòng điền đầy đủ thông tin")
        
        st.markdown('</div>', unsafe_allow_html=True)

def handle_register():
    """Handle user registration"""
    with st.container():
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        
        with st.form("register_form"):
            st.markdown("### Tạo tài khoản mới")
            
            email = st.text_input(
                "📧 Email", 
                placeholder="your.email@example.com",
                key="register_email"
            )
            
            password = st.text_input(
                "🔒 Mật khẩu", 
                type="password",
                placeholder="Ít nhất 6 ký tự",
                help="Mật khẩu phải có ít nhất 6 ký tự",
                key="register_password"
            )
            
            confirm_password = st.text_input(
                "🔒 Xác nhận mật khẩu", 
                type="password",
                placeholder="Nhập lại mật khẩu",
                key="register_confirm"
            )
            
            register_btn = st.form_submit_button("✨ Tạo tài khoản", use_container_width=True)
            
            if register_btn:
                if not all([email, password, confirm_password]):
                    st.warning("⚠️ Vui lòng điền đầy đủ thông tin")
                elif password != confirm_password:
                    st.error("❌ Mật khẩu xác nhận không khớp")
                elif len(password) < 6:
                    st.error("❌ Mật khẩu phải có ít nhất 6 ký tự")
                else:
                    with st.spinner('Đang tạo tài khoản...'):
                        result = auth_manager.register(email, password)
                        if result['success']:
                            st.success("🎉 Đăng ký thành công!")
                            st.info("📧 Vui lòng kiểm tra email để xác thực tài khoản")
                            st.balloons()
                        else:
                            st.error(f"❌ {result['message']}")
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_main_app():
    """Display main application interface"""
    user_email = st.session_state.user_data.get('email', 'Unknown')
    
    # Sidebar navigation
    with st.sidebar:
        # Theme toggle on sidebar
        selected = ui_manager.render_theme_toggle(st.session_state.theme)
        if selected != st.session_state.theme:
            st.session_state.theme = selected
            ui_manager.apply_theme(selected)
            st.rerun()

        ui_manager.render_user_info(user_email)
        
        if st.button("🚪 Đăng xuất", key="logout", use_container_width=True, type="secondary"):
            auth_manager.logout()
            st.session_state.authenticated = False
            st.session_state.user_data = None
            st.rerun()
        
        st.markdown("---")
        
        # Navigation menu
        pages = {
            "🏠 Trang chủ": "home",
            "📚 Thư viện Tài liệu": "documents", 
            "📤 Upload Tài liệu": "upload",
            "⚙️ Quản lý Môn học": "subjects"
        }
        
        for page_name, page_key in pages.items():
            if st.button(page_name, key=f"nav_{page_key}", use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun()
    
    # Main content area
    current_page = st.session_state.current_page
    
    if current_page == "home":
        show_home_page()
    elif current_page == "documents":
        show_documents_page()
    elif current_page == "upload":
        show_upload_page()
    elif current_page == "subjects":
        show_subjects_page()

def show_home_page():
    """Display home dashboard"""
    ui_manager.render_page_header("🏠 Trang chủ", "Chào mừng đến với hệ thống quản lý tài liệu")
    
    # Statistics cards
    user_id = st.session_state.user_data['id']
    stats = db_manager.get_user_statistics(user_id)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        ui_manager.render_stat_card("📄", "Tài liệu", stats['total_documents'], "#667eea")
    
    with col2:
        ui_manager.render_stat_card("📚", "Môn học", stats['total_subjects'], "#28a745")
    
    with col3:
        ui_manager.render_stat_card("🏷️", "Tags", stats['total_tags'], "#ffc107")
    
    with col4:
        ui_manager.render_stat_card("💾", "Dung lượng", f"{stats['total_size']:.1f} MB", "#dc3545")
    
    # Quick actions
    st.markdown("### 🚀 Hành động nhanh")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📤 Upload tài liệu mới", use_container_width=True, type="primary"):
            st.session_state.current_page = "upload"
            st.rerun()
    
    with col2:
        if st.button("📚 Xem thư viện", use_container_width=True):
            st.session_state.current_page = "documents"
            st.rerun()
    
    with col3:
        if st.button("⚙️ Quản lý môn học", use_container_width=True):
            st.session_state.current_page = "subjects"
            st.rerun()
    
    # Recent documents
    recent_docs = db_manager.get_recent_documents(user_id, limit=5)
    if recent_docs:
        st.markdown("### 📋 Tài liệu gần đây")
        ui_manager.render_document_list(recent_docs, show_actions=False)

def show_documents_page():
    """Display documents management page"""
    ui_manager.render_page_header("📚 Thư viện Tài liệu", "Quản lý và tổ chức tài liệu của bạn")
    
    user_id = st.session_state.user_data['id']
    
    # Search and filters
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        search_term = st.text_input("🔍 Tìm kiếm", placeholder="Nhập tên tài liệu...")
    
    with col2:
        subjects = db_manager.get_user_subjects(user_id)
        subject_options = ["Tất cả"] + [s['name'] for s in subjects]
        selected_subject = st.selectbox("📚 Môn học", subject_options)
    
    with col3:
        sort_options = ["Mới nhất", "Cũ nhất", "Tên A-Z", "Tên Z-A"]
        sort_by = st.selectbox("🔄 Sắp xếp", sort_options)
    
    # Get and filter documents
    documents = db_manager.get_user_documents(user_id)
    
    # Apply filters
    if search_term:
        documents = [d for d in documents if search_term.lower() in d['file_name'].lower()]
    
    if selected_subject != "Tất cả":
        documents = [d for d in documents if d.get('subject_name') == selected_subject]
    
    # Apply sorting
    if sort_by == "Mới nhất":
        documents.sort(key=lambda x: x['created_at'], reverse=True)
    elif sort_by == "Cũ nhất":
        documents.sort(key=lambda x: x['created_at'])
    elif sort_by == "Tên A-Z":
        documents.sort(key=lambda x: x['file_name'])
    elif sort_by == "Tên Z-A":
        documents.sort(key=lambda x: x['file_name'], reverse=True)
    
    # Display results
    if documents:
        st.info(f"📊 Hiển thị {len(documents)} tài liệu")
        ui_manager.render_document_grid(documents, db_manager)
    else:
        ui_manager.render_empty_state("📄", "Không tìm thấy tài liệu", "Thử thay đổi bộ lọc hoặc upload tài liệu mới")

def show_upload_page():
    """Display upload page"""
    ui_manager.render_page_header("📤 Upload Tài liệu", "Thêm tài liệu mới vào thư viện")
    
    user_id = st.session_state.user_data['id']
    
    with st.form("upload_form"):
        # File upload
        uploaded_file = st.file_uploader(
            "Chọn tài liệu",
            type=['pdf', 'docx', 'txt', 'xlsx', 'pptx', 'doc'],
            help="Hỗ trợ: PDF, DOCX, TXT, XLSX, PPTX (tối đa 200MB)"
        )
        
        if uploaded_file:
            ui_manager.render_file_preview(uploaded_file)
        
        # Metadata
        col1, col2 = st.columns(2)
        
        with col1:
            subjects = db_manager.get_user_subjects(user_id)
            subject_options = [""] + [s['name'] for s in subjects]
            selected_subject = st.selectbox("📚 Môn học", subject_options)
        
        with col2:
            tags_input = st.text_input(
                "🏷️ Tags", 
                placeholder="bài giảng, quan trọng, thi cuối kỳ",
                help="Cách nhau bởi dấu phẩy"
            )
        
        # Submit
        submit_btn = st.form_submit_button("🚀 Upload", use_container_width=True, type="primary")
        
        if submit_btn:
            if uploaded_file:
                with st.spinner("Đang upload..."):
                    result = db_manager.upload_document(
                        user_id=user_id,
                        file=uploaded_file,
                        subject_name=selected_subject if selected_subject else None,
                        tags=tags_input
                    )
                    
                    if result['success']:
                        st.success("🎉 Upload thành công!")
                        st.balloons()
                        # Auto redirect to documents
                        st.session_state.current_page = "documents"
                        st.rerun()
                    else:
                        st.error(f"❌ {result['message']}")
            else:
                st.warning("⚠️ Vui lòng chọn file để upload")

def show_subjects_page():
    """Display subjects management page"""
    ui_manager.render_page_header("⚙️ Quản lý Môn học", "Tổ chức tài liệu theo môn học")
    
    user_id = st.session_state.user_data['id']
    
    # Add new subject
    with st.form("add_subject_form"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            subject_name = st.text_input(
                "Tên môn học mới",
                placeholder="Ví dụ: Toán cao cấp, Lập trình Python..."
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            add_btn = st.form_submit_button("➕ Thêm", use_container_width=True)
        
        if add_btn and subject_name:
            result = db_manager.add_subject(user_id, subject_name.strip())
            if result['success']:
                st.success(f"✅ Đã thêm môn học '{subject_name}'")
                st.rerun()
            else:
                st.error(f"❌ {result['message']}")
    
    # Display subjects with CRUD
    subjects = db_manager.get_user_subjects(user_id)
    
    if subjects:
        st.markdown("### Danh sách môn học")
        for s in subjects:
            sid = s.get("id")
            cols = st.columns([4, 1, 1])
            with cols[0]:
                new_name = st.text_input(
                    label=f"Tên môn học (ID {sid})",
                    value=s.get("name", ""),
                    key=f"sub_name_{sid}"
                )
            with cols[1]:
                if st.button("💾 Lưu", key=f"save_sub_{sid}", use_container_width=True):
                    if new_name.strip():
                        res = db_manager.update_subject(int(sid), new_name.strip())
                        if res.get("success"):
                            st.success("Đã cập nhật môn học")
                            st.rerun()
                        else:
                            st.error(f"❌ {res.get('message')}")
                    else:
                        st.warning("Tên môn học không được để trống")
            with cols[2]:
                confirm = st.checkbox("Xác nhận", key=f"confirm_del_{sid}")
                if st.button("🗑️ Xóa", key=f"del_sub_{sid}", use_container_width=True, disabled=not confirm):
                    res = db_manager.delete_subject(int(sid))
                    if res.get("success"):
                        st.success("Đã xóa môn học")
                        st.rerun()
                    else:
                        st.error(f"❌ {res.get('message')}")
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    else:
        ui_manager.render_empty_state("📚", "Chưa có môn học", "Tạo môn học đầu tiên để tổ chức tài liệu")

if __name__ == "__main__":
    main()