# pages/_Chỉnh_sửa_tài_liệu.py
import streamlit as st
from utils import db, auth
import pandas as pd
import time

# Load custom CSS
def load_css():
    try:
        with open('styles/custom.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except:
        pass

load_css()

# --- KIỂM TRA ĐĂNG NHẬP VÀ SESSION STATE ---
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
    
    if st.button("🚪 Đăng xuất", key="logout_edit", use_container_width=True, type="secondary"):
        st.session_state.user_session = None
        st.rerun()

if "doc_to_edit" not in st.session_state or st.session_state.doc_to_edit is None:
    # Modern no document selected page
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; margin-bottom: 2rem;">
        <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            ✏️ Chỉnh sửa Tài liệu
        </h1>
        <p style="font-size: 1.1rem; color: #6c757d; font-weight: 300;">
            Cập nhật thông tin tài liệu của bạn
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="main-container" style="text-align: center; padding: 3rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">📝</div>
        <h3 style="color: #667eea; margin-bottom: 1rem;">Chưa chọn tài liệu</h3>
        <p style="color: #6c757d; margin-bottom: 2rem;">
            Vui lòng chọn một tài liệu từ thư viện để chỉnh sửa
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("📚 Đến Thư viện Tài liệu", use_container_width=True):
            auth.nav_page("Tài_liệu_của_tôi")
    st.stop()

# --- LẤY DỮ LIỆU ---
doc_id = st.session_state.doc_to_edit

try:
    doc_data = db.get_document_by_id(doc_id)
    subjects_data = db.get_user_subjects(user_id)
except Exception as e:
    st.error(f"❌ Không thể tải dữ liệu tài liệu: {e}")
    st.stop()

# Modern header with document info
file_ext = doc_data['file_name'].split('.')[-1].upper()
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
<div style="text-align: center; padding: 2rem 0; margin-bottom: 2rem;">
    <div style="font-size: 3rem; margin-bottom: 1rem;">{file_icon}</div>
    <h1 style="font-size: 2rem; margin-bottom: 0.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        Chỉnh sửa: {doc_data['file_name'][:40]}{'...' if len(doc_data['file_name']) > 40 else ''}
    </h1>
    <p style="font-size: 1rem; color: #6c757d; font-weight: 300;">
        Cập nhật thông tin phân loại và tags
    </p>
</div>
""", unsafe_allow_html=True)

# Document info card
upload_date = pd.to_datetime(doc_data['created_at']).strftime('%d/%m/%Y %H:%M')
file_size = f"{doc_data.get('file_size', 0) / 1024:.1f} KB" if doc_data.get('file_size') else "N/A"

st.markdown(f"""
<div class="main-container">
    <h3 style="color: #667eea; margin-bottom: 1rem;">📋 Thông tin tài liệu</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
        <div class="glass-card" style="padding: 1rem; text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">📄</div>
            <h4 style="color: #667eea; margin: 0; font-size: 0.9rem;">Tên file</h4>
            <p style="color: #6c757d; margin: 0; font-size: 0.8rem;">{doc_data['file_name']}</p>
        </div>
        
        <div class="glass-card" style="padding: 1rem; text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">📅</div>
            <h4 style="color: #667eea; margin: 0; font-size: 0.9rem;">Ngày upload</h4>
            <p style="color: #6c757d; margin: 0; font-size: 0.8rem;">{upload_date}</p>
        </div>
        
        <div class="glass-card" style="padding: 1rem; text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">💾</div>
            <h4 style="color: #667eea; margin: 0; font-size: 0.9rem;">Kích thước</h4>
            <p style="color: #6c757d; margin: 0; font-size: 0.8rem;">{file_size}</p>
        </div>
        
        <div class="glass-card" style="padding: 1rem; text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">📁</div>
            <h4 style="color: #667eea; margin: 0; font-size: 0.9rem;">Định dạng</h4>
            <p style="color: #6c757d; margin: 0; font-size: 0.8rem;">{file_ext}</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- FORM CHỈNH SỬA ---
subject_map = {s['name']: s['id'] for s in subjects_data}
subject_names = list(subject_map.keys())

# Tìm index của môn học hiện tại
current_subject_name = doc_data.get('subjects', {}).get('name')
current_subject_index = 0
if current_subject_name and current_subject_name in subject_names:
    current_subject_index = subject_names.index(current_subject_name)

st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown("### ✏️ Chỉnh sửa thông tin")

with st.form("edit_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📚 Môn học")
        if not subjects_data:
            st.info("💡 Chưa có môn học nào. Hãy tạo môn học trước!")
            new_subject_name = ""
        else:
            new_subject_name = st.selectbox(
                "Chọn môn học",
                options=[""] + subject_names,
                index=current_subject_index + 1 if current_subject_name else 0,
                help="Chọn môn học để phân loại tài liệu"
            )
            
            # Show current vs new
            if current_subject_name:
                st.caption(f"**Hiện tại:** {current_subject_name}")
    
    with col2:
        st.markdown("#### 🏷️ Tags")
        current_tags = doc_data.get('tags', [])
        new_tags_str = st.text_input(
            "Tags (cách nhau bởi dấu phẩy)",
            value=", ".join(current_tags),
            placeholder="ví dụ: bài giảng, quan trọng, thi cuối kỳ",
            help="Thêm tags để dễ tìm kiếm sau này"
        )
        
        # Tag preview
        if new_tags_str:
            tags_preview = [tag.strip() for tag in new_tags_str.split(',') if tag.strip()]
            if tags_preview:
                tags_html = ""
                for tag in tags_preview[:5]:
                    tags_html += f'<span class="tag" style="font-size: 0.8rem; padding: 0.3rem 0.6rem; margin: 0.2rem;">{tag}</span>'
                st.markdown(f"**Preview:** {tags_html}", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Action buttons
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    
    with col_btn1:
        cancel_btn = st.form_submit_button("❌ Hủy bỏ", use_container_width=True)
    
    with col_btn2:
        submitted = st.form_submit_button("💾 Lưu thay đổi", use_container_width=True)
    
    with col_btn3:
        reset_btn = st.form_submit_button("🔄 Khôi phục", use_container_width=True)
    
    # Handle form submissions
    if cancel_btn:
        del st.session_state.doc_to_edit
        auth.nav_page("Tài_liệu_của_tôi")
    
    if reset_btn:
        st.rerun()
    
    if submitted:
        # Progress animation
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Validate changes
            status_text.text("🔍 Đang kiểm tra thay đổi...")
            progress_bar.progress(25)
            time.sleep(0.3)
            
            new_subject_id = subject_map.get(new_subject_name)
            new_tags_list = [tag.strip() for tag in new_tags_str.split(',') if tag.strip()]
            
            # Check if there are actual changes
            current_subject_id = doc_data.get('subject_id')
            changes_made = (new_subject_id != current_subject_id) or (new_tags_list != current_tags)
            
            if not changes_made:
                progress_bar.progress(0)
                status_text.text("")
                st.info("ℹ️ Không có thay đổi nào để lưu")
            else:
                # Step 2: Prepare updates
                status_text.text("📝 Đang chuẩn bị cập nhật...")
                progress_bar.progress(50)
                time.sleep(0.3)
                
                updates = {
                    "subject_id": new_subject_id,
                    "tags": new_tags_list
                }
                
                # Step 3: Save to database
                status_text.text("💾 Đang lưu vào cơ sở dữ liệu...")
                progress_bar.progress(75)
                
                db.update_document_metadata(doc_id, updates)
                time.sleep(0.3)
                
                # Step 4: Complete
                progress_bar.progress(100)
                status_text.text("✅ Hoàn thành!")
                time.sleep(0.5)
                
                # Success message
                st.success("🎉 Cập nhật thành công!")
                st.balloons()
                
                # Show summary of changes
                st.markdown(f"""
                <div class="glass-card" style="margin-top: 1rem;">
                    <h4 style="color: #28a745; margin-bottom: 1rem;">📋 Tóm tắt thay đổi</h4>
                    <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 0.5rem; font-size: 0.9rem;">
                        <span style="color: #6c757d;">📚 Môn học:</span>
                        <span style="font-weight: 500;">{new_subject_name or 'Chưa phân loại'}</span>
                        
                        <span style="color: #6c757d;">🏷️ Tags:</span>
                        <span style="font-weight: 500;">{', '.join(new_tags_list) if new_tags_list else 'Không có'}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Auto redirect after 3 seconds
                with st.spinner("Sẽ quay về thư viện tài liệu trong 3 giây..."):
                    time.sleep(3)
                
                # Clean up and redirect
                del st.session_state.doc_to_edit
                auth.nav_page("Tài_liệu_của_tôi")
                
        except Exception as e:
            progress_bar.progress(0)
            status_text.text("")
            st.error(f"❌ Lỗi cập nhật: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

# Quick actions
st.markdown("""
<div class="main-container" style="margin-top: 2rem;">
    <h3 style="color: #667eea; margin-bottom: 1rem;">🚀 Hành động nhanh</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
        <div class="glass-card" style="padding: 1rem; text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📚</div>
            <h4 style="color: #667eea; margin-bottom: 0.5rem;">Thư viện</h4>
            <p style="font-size: 0.9rem; color: #6c757d; margin: 0;">Quay về xem tất cả tài liệu</p>
        </div>
        
        <div class="glass-card" style="padding: 1rem; text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📤</div>
            <h4 style="color: #667eea; margin-bottom: 0.5rem;">Upload</h4>
            <p style="font-size: 0.9rem; color: #6c757d; margin: 0;">Thêm tài liệu mới</p>
        </div>
        
        <div class="glass-card" style="padding: 1rem; text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⚙️</div>
            <h4 style="color: #667eea; margin-bottom: 0.5rem;">Môn học</h4>
            <p style="font-size: 0.9rem; color: #6c757d; margin: 0;">Quản lý phân loại</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)