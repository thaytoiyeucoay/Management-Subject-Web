# pages/Upload_Tài_liệu.py
import streamlit as st
from utils import db, auth
import time

# Load custom CSS
def load_css():
    try:
        with open('styles/custom.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except:
        pass

load_css()

# --- KIỂM TRA ĐĂNG NHẬP ---
if not st.session_state.get("user_session"):
    st.error("Bạn cần đăng nhập để xem trang này.")
    st.stop()

user_id = auth.get_user_id()
user_email = auth.get_user_email()

# Modern sidebar
with st.sidebar:
    st.markdown(f"""
    <div class="glass-card" style="text-align: center; margin-bottom: 1rem;">
        <h3 style="color: #667eea; margin-bottom: 0.5rem;">👋 Xin chào!</h3>
        <p style="font-size: 0.9rem; color: #6c757d; margin: 0;">{user_email}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚪 Đăng xuất", key="logout_upload", use_container_width=True, type="secondary"):
        st.session_state.user_session = None
        st.rerun()

# Modern header
st.markdown("""
<div style="text-align: center; padding: 2rem 0; margin-bottom: 2rem;">
    <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        📤 Upload Tài liệu
    </h1>
    <p style="font-size: 1.1rem; color: #6c757d; font-weight: 300;">
        Thêm tài liệu mới vào thư viện của bạn
    </p>
</div>
""", unsafe_allow_html=True)

# Lấy danh sách môn học của người dùng
subjects_data = db.get_user_subjects(user_id)
subject_map = {s['name']: s['id'] for s in subjects_data}

# Modern upload form
st.markdown('<div class="main-container">', unsafe_allow_html=True)

with st.form("upload_form", clear_on_submit=True):
    st.markdown("### 📁 Chọn tài liệu")
    
    # Enhanced file uploader with custom styling
    uploaded_file = st.file_uploader(
        "Kéo thả file vào đây hoặc click để chọn",
        type=['pdf', 'docx', 'txt', 'xlsx', 'pptx'],
        help="Hỗ trợ các định dạng: PDF, DOCX, TXT, XLSX, PPTX"
    )
    
    if uploaded_file:
        # File preview
        file_size_mb = uploaded_file.size / (1024 * 1024)
        file_ext = uploaded_file.name.split('.')[-1].upper()
        
        # File type icon
        icon_map = {
            'PDF': '📕',
            'DOCX': '📘',
            'DOC': '📘',
            'TXT': '📄',
            'XLSX': '📗',
            'PPTX': '📙'
        }
        file_icon = icon_map.get(file_ext, '📄')
        
        st.markdown(f"""
        <div class="glass-card" style="margin: 1rem 0; padding: 1rem;">
            <div style="display: flex; align-items: center;">
                <div style="font-size: 2rem; margin-right: 1rem;">{file_icon}</div>
                <div style="flex: 1;">
                    <h4 style="margin: 0; color: #667eea;">{uploaded_file.name}</h4>
                    <p style="margin: 0; color: #6c757d; font-size: 0.9rem;">
                        {file_ext} • {file_size_mb:.2f} MB
                    </p>
                </div>
                <div style="color: #28a745; font-size: 1.5rem;">✅</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Form fields with modern styling
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📚 Phân loại")
        if not subjects_data:
            st.info("💡 Chưa có môn học nào. Hãy tạo môn học trước!")
            selected_subject_name = ""
        else:
            selected_subject_name = st.selectbox(
                "Chọn môn học",
                options=[""] + list(subject_map.keys()),
                help="Chọn môn học để phân loại tài liệu"
            )
    
    with col2:
        st.markdown("### 🏷️ Tags")
        tags_input = st.text_input(
            "Nhập tags",
            placeholder="ví dụ: bài giảng, thi cuối kỳ, quan trọng",
            help="Cách nhau bởi dấu phẩy để dễ tìm kiếm sau này"
        )
        
        # Tag suggestions
        if tags_input:
            tags_preview = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
            if tags_preview:
                tags_html = ""
                for tag in tags_preview[:5]:  # Show max 5 tags
                    tags_html += f'<span class="tag" style="font-size: 0.8rem; padding: 0.3rem 0.6rem; margin: 0.2rem;">{tag}</span>'
                st.markdown(f"**Preview:** {tags_html}", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Submit button with enhanced styling
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        submitted = st.form_submit_button("🚀 Upload Tài liệu", use_container_width=True)
    
    if submitted and uploaded_file is not None:
        # Progress animation
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Validate file
            status_text.text("🔍 Đang kiểm tra file...")
            progress_bar.progress(20)
            time.sleep(0.5)
            
            file_bytes = uploaded_file.getvalue()
            file_name = uploaded_file.name
            file_path = f"{user_id}/{file_name}"
            
            # Step 2: Upload to storage
            status_text.text("☁️ Đang upload lên cloud...")
            progress_bar.progress(50)
            
            db.upload_file_to_storage(file_bytes, file_path)
            time.sleep(0.5)
            
            # Step 3: Save metadata
            status_text.text("💾 Đang lưu thông tin...")
            progress_bar.progress(80)
            
            tags_list = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
            metadata = {
                "user_id": user_id,
                "subject_id": subject_map.get(selected_subject_name),
                "file_name": file_name,
                "file_path": file_path,
                "file_size": uploaded_file.size,
                "file_type": uploaded_file.type,
                "tags": tags_list
            }
            
            db.insert_document(metadata)
            
            # Step 4: Complete
            progress_bar.progress(100)
            status_text.text("✅ Hoàn thành!")
            time.sleep(0.5)
            
            # Success message with animation
            st.success("🎉 Upload tài liệu thành công!")
            st.balloons()
            
            # Show summary
            st.markdown(f"""
            <div class="glass-card" style="margin-top: 1rem;">
                <h4 style="color: #28a745; margin-bottom: 1rem;">📋 Tóm tắt upload</h4>
                <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 0.5rem; font-size: 0.9rem;">
                    <span style="color: #6c757d;">📄 Tên file:</span>
                    <span style="font-weight: 500;">{file_name}</span>
                    
                    <span style="color: #6c757d;">📚 Môn học:</span>
                    <span style="font-weight: 500;">{selected_subject_name or 'Chưa phân loại'}</span>
                    
                    <span style="color: #6c757d;">🏷️ Tags:</span>
                    <span style="font-weight: 500;">{', '.join(tags_list) if tags_list else 'Không có'}</span>
                    
                    <span style="color: #6c757d;">💾 Kích thước:</span>
                    <span style="font-weight: 500;">{file_size_mb:.2f} MB</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Quick actions
            st.markdown("### 🚀 Tiếp theo?")
            col_action1, col_action2, col_action3 = st.columns(3)
            
            with col_action1:
                if st.button("📤 Upload thêm", use_container_width=True):
                    st.rerun()
            
            with col_action2:
                if st.button("📚 Xem tài liệu", use_container_width=True):
                    auth.nav_page("Tài_liệu_của_tôi")
            
            with col_action3:
                if st.button("⚙️ Quản lý môn học", use_container_width=True):
                    auth.nav_page("Quản_lý_Môn_học")
                    
        except Exception as e:
            progress_bar.progress(0)
            status_text.text("")
            st.error(f"❌ Lỗi upload: {str(e)}")
            
    elif submitted and uploaded_file is None:
        st.warning("⚠️ Vui lòng chọn file để upload!")

st.markdown('</div>', unsafe_allow_html=True)

# Upload tips
st.markdown("""
<div class="main-container" style="margin-top: 2rem;">
    <h3 style="color: #667eea; margin-bottom: 1rem;">💡 Mẹo upload hiệu quả</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
        <div class="glass-card" style="padding: 1rem;">
            <h4 style="color: #667eea; margin-bottom: 0.5rem;">📁 Định dạng hỗ trợ</h4>
            <p style="font-size: 0.9rem; color: #6c757d; margin: 0;">
                PDF, DOCX, TXT, XLSX, PPTX - tối đa 200MB mỗi file
            </p>
        </div>
        
        <div class="glass-card" style="padding: 1rem;">
            <h4 style="color: #667eea; margin-bottom: 0.5rem;">🏷️ Sử dụng Tags</h4>
            <p style="font-size: 0.9rem; color: #6c757d; margin: 0;">
                Thêm tags để tìm kiếm nhanh chóng và tổ chức tốt hơn
            </p>
        </div>
        
        <div class="glass-card" style="padding: 1rem;">
            <h4 style="color: #667eea; margin-bottom: 0.5rem;">📚 Phân loại môn học</h4>
            <p style="font-size: 0.9rem; color: #6c757d; margin: 0;">
                Tạo môn học trước để phân loại tài liệu một cách khoa học
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)