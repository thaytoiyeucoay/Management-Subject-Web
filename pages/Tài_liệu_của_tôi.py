# pages/Tài_liệu_của_tôi.py
import streamlit as st
from utils import db, auth
import pandas as pd

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
    
    if st.button("🚪 Đăng xuất", key="logout_main", use_container_width=True, type="secondary"):
        st.session_state.user_session = None
        st.rerun()

# --- LẤY DỮ LIỆU ---
documents = db.get_user_documents(user_id)

# Modern header
st.markdown("""
<div style="text-align: center; padding: 2rem 0; margin-bottom: 2rem;">
    <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        📚 Thư viện Tài liệu
    </h1>
    <p style="font-size: 1.1rem; color: #6c757d; font-weight: 300;">
        Quản lý và tổ chức tài liệu của bạn một cách thông minh
    </p>
</div>
""", unsafe_allow_html=True)

if not documents:
    st.markdown("""
    <div class="main-container" style="text-align: center; padding: 3rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">📄</div>
        <h3 style="color: #667eea; margin-bottom: 1rem;">Chưa có tài liệu nào</h3>
        <p style="color: #6c757d; margin-bottom: 2rem;">
            Bắt đầu xây dựng thư viện tài liệu của bạn ngay hôm nay!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("📤 Upload tài liệu mới", use_container_width=True, type="primary"):
            auth.nav_page("Upload_Tài_liệu")
    st.stop()

# --- MODERN SEARCH AND FILTER INTERFACE ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    search_term = st.text_input("🔍 Tìm kiếm tài liệu", placeholder="Nhập tên file để tìm kiếm...")

with col2:
    all_tags = sorted(list(set(tag for doc in documents if doc['tags'] for tag in doc['tags'])))
    selected_tags = st.multiselect("🏷️ Lọc theo tags", options=all_tags, placeholder="Chọn tags để lọc")

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    total_docs = len(documents)
    st.metric("📊 Tổng số", total_docs)

st.markdown('</div>', unsafe_allow_html=True)

# Lọc dữ liệu
filtered_data = documents
if search_term:
    filtered_data = [d for d in filtered_data if search_term.lower() in d['file_name'].lower()]
if selected_tags:
    filtered_data = [d for d in filtered_data if d['tags'] and set(selected_tags).issubset(set(d['tags']))]

# Show filtered results count
if len(filtered_data) != len(documents):
    st.info(f"🔍 Hiển thị {len(filtered_data)} / {len(documents)} tài liệu")

# --- MODERN DOCUMENT CARDS ---
if filtered_data:
    # Grid layout for cards
    for i in range(0, len(filtered_data), 2):
        cols = st.columns(2)
        
        for j, col in enumerate(cols):
            if i + j < len(filtered_data):
                doc = filtered_data[i + j]
                
                with col:
                    # Modern card design
                    subject_name = doc.get('subjects', {}).get('name') or "Chưa phân loại"
                    upload_date = pd.to_datetime(doc['created_at']).strftime('%d/%m/%Y')
                    file_size = f"{doc.get('file_size', 0) / 1024:.1f} KB" if doc.get('file_size') else "N/A"
                    
                    # File type icon
                    file_ext = doc['file_name'].split('.')[-1].lower()
                    icon_map = {
                        'pdf': '📕',
                        'docx': '📘',
                        'doc': '📘',
                        'txt': '📄',
                        'xlsx': '📗',
                        'pptx': '📙'
                    }
                    file_icon = icon_map.get(file_ext, '📄')
                    
                    card_html = f"""
                    <div class="glass-card animated-card" style="height: 280px; position: relative; overflow: hidden;">
                        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                            <div style="font-size: 2rem; margin-right: 0.5rem;">{file_icon}</div>
                            <div style="flex: 1;">
                                <h4 style="margin: 0; color: #667eea; font-size: 1.1rem; font-weight: 600; line-height: 1.3;">
                                    {doc['file_name'][:30]}{'...' if len(doc['file_name']) > 30 else ''}
                                </h4>
                            </div>
                        </div>
                        
                        <div style="margin-bottom: 1rem;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                                <span style="color: #6c757d; font-size: 0.85rem;">📚 Môn học:</span>
                                <span style="color: #667eea; font-weight: 500; font-size: 0.85rem;">{subject_name}</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                                <span style="color: #6c757d; font-size: 0.85rem;">📅 Ngày tải:</span>
                                <span style="color: #6c757d; font-size: 0.85rem;">{upload_date}</span>
                            </div>
                            <div style="display: flex; justify-content: space-between;">
                                <span style="color: #6c757d; font-size: 0.85rem;">💾 Kích thước:</span>
                                <span style="color: #6c757d; font-size: 0.85rem;">{file_size}</span>
                            </div>
                        </div>
                    """
                    
                    # Tags
                    if doc['tags']:
                        tags_html = ""
                        for tag in doc['tags'][:3]:  # Limit to 3 tags
                            tags_html += f'<span class="tag" style="font-size: 0.75rem; padding: 0.2rem 0.5rem; margin: 0.1rem;">{tag}</span>'
                        if len(doc['tags']) > 3:
                            tags_html += f'<span style="color: #6c757d; font-size: 0.75rem;">+{len(doc["tags"]) - 3} more</span>'
                        card_html += f'<div style="margin-bottom: 1rem;">{tags_html}</div>'
                    
                    card_html += "</div>"
                    
                    st.markdown(card_html, unsafe_allow_html=True)
                    
                    # Action buttons
                    btn_col1, btn_col2, btn_col3 = st.columns(3)
                    
                    with btn_col1:
                        try:
                            res = db.supabase.storage.from_('document_files').create_signed_url(doc['file_path'], 60)
                            st.link_button("📥", url=res['signedURL'], 
                                         help="Tải xuống", use_container_width=True)
                        except Exception as e:
                            st.button("❌", disabled=True, help="Lỗi link", use_container_width=True)
                    
                    with btn_col2:
                        edit_button = st.button("✏️", key=f"edit_{doc['id']}", 
                                   help="Chỉnh sửa", use_container_width=True)
                        if edit_button:
                            st.session_state.selected_document_id = doc['id']
                            auth.nav_page("_Chỉnh_sửa_tài_liệu")
                    
                    with btn_col3:
                        if st.button("🗑️", key=f"delete_{doc['id']}", 
                                   help="Xóa tài liệu", use_container_width=True, type="primary"):
                            if st.session_state.get(f"confirm_delete_{doc['id']}", False):
                                with st.spinner("Đang xóa..."):
                                    db.delete_document(doc['id'], doc['file_path'])
                                    st.success("Đã xóa tài liệu!")
                                    st.rerun()
                            else:
                                st.session_state[f"confirm_delete_{doc['id']}"] = True
                                st.warning("Nhấn lại để xác nhận xóa")
                                st.rerun()
else:
    st.markdown("""
    <div class="main-container" style="text-align: center; padding: 2rem;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
        <h3 style="color: #667eea;">Không tìm thấy tài liệu</h3>
        <p style="color: #6c757d;">Thử thay đổi từ khóa tìm kiếm hoặc bộ lọc</p>
    </div>
    """, unsafe_allow_html=True)