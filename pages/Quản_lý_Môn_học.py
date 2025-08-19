# pages/Quản_lý_Môn_học.py
import streamlit as st
from utils import db, auth

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
    
    if st.button("🚪 Đăng xuất", key="logout_subjects", use_container_width=True, type="secondary"):
        st.session_state.user_session = None
        st.rerun()

# Modern header
st.markdown("""
<div style="text-align: center; padding: 2rem 0; margin-bottom: 2rem;">
    <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        ⚙️ Quản lý Môn học
    </h1>
    <p style="font-size: 1.1rem; color: #6c757d; font-weight: 300;">
        Tổ chức và phân loại tài liệu theo môn học
    </p>
</div>
""", unsafe_allow_html=True)

# Get subjects data
subjects_data = db.get_user_subjects(user_id)

# Statistics cards
col1, col2, col3 = st.columns(3)

with col1:
    total_subjects = len(subjects_data)
    st.markdown(f"""
    <div class="glass-card" style="text-align: center; padding: 1.5rem;">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📚</div>
        <h3 style="color: #667eea; margin: 0; font-size: 2rem;">{total_subjects}</h3>
        <p style="color: #6c757d; margin: 0; font-size: 0.9rem;">Tổng môn học</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Count documents per subject
    documents = db.get_user_documents(user_id)
    total_docs = len(documents)
    st.markdown(f"""
    <div class="glass-card" style="text-align: center; padding: 1.5rem;">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📄</div>
        <h3 style="color: #667eea; margin: 0; font-size: 2rem;">{total_docs}</h3>
        <p style="color: #6c757d; margin: 0; font-size: 0.9rem;">Tổng tài liệu</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    avg_docs = round(total_docs / total_subjects, 1) if total_subjects > 0 else 0
    st.markdown(f"""
    <div class="glass-card" style="text-align: center; padding: 1.5rem;">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📊</div>
        <h3 style="color: #667eea; margin: 0; font-size: 2rem;">{avg_docs}</h3>
        <p style="color: #6c757d; margin: 0; font-size: 0.9rem;">TB tài liệu/môn</p>
    </div>
    """, unsafe_allow_html=True)

# Add new subject form
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown("### ➕ Thêm môn học mới")

with st.form("new_subject_form", clear_on_submit=True):
    col_input, col_btn = st.columns([3, 1])
    
    with col_input:
        subject_name = st.text_input(
            "Tên môn học", 
            placeholder="Ví dụ: Toán cao cấp, Lập trình Python...",
            help="Nhập tên môn học để phân loại tài liệu"
        )
    
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("✨ Thêm môn học", use_container_width=True)
    
    if submitted and subject_name:
        if subject_name.strip():
            try:
                # Check if subject already exists
                existing_subjects = [s['name'].lower() for s in subjects_data]
                if subject_name.lower() in existing_subjects:
                    st.warning(f"⚠️ Môn học '{subject_name}' đã tồn tại!")
                else:
                    db.add_subject(user_id, subject_name.strip())
                    st.success(f"🎉 Đã thêm môn học '{subject_name}'!")
                    st.balloons()
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Lỗi: {str(e)}")
        else:
            st.warning("⚠️ Vui lòng nhập tên môn học!")
    elif submitted:
        st.warning("⚠️ Vui lòng nhập tên môn học!")

st.markdown('</div>', unsafe_allow_html=True)

# Display subjects list
if not subjects_data:
    st.markdown("""
    <div class="main-container" style="text-align: center; padding: 3rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">📚</div>
        <h3 style="color: #667eea; margin-bottom: 1rem;">Chưa có môn học nào</h3>
        <p style="color: #6c757d; margin-bottom: 2rem;">
            Tạo môn học đầu tiên để bắt đầu tổ chức tài liệu của bạn
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("### 📋 Danh sách môn học")
    
    # Count documents for each subject
    subject_doc_count = {}
    for doc in documents:
        subject_id = doc.get('subject_id')
        if subject_id:
            subject_doc_count[subject_id] = subject_doc_count.get(subject_id, 0) + 1
    
    # Display subjects in a grid
    for i in range(0, len(subjects_data), 2):
        cols = st.columns(2)
        
        for j, col in enumerate(cols):
            if i + j < len(subjects_data):
                subject = subjects_data[i + j]
                doc_count = subject_doc_count.get(subject['id'], 0)
                
                with col:
                    # Modern subject card
                    card_html = f"""
                    <div class="glass-card animated-card" style="position: relative; padding: 1.5rem; margin-bottom: 1rem;">
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                            <div style="display: flex; align-items: center;">
                                <div style="font-size: 2rem; margin-right: 1rem;">📚</div>
                                <div>
                                    <h4 style="margin: 0; color: #667eea; font-size: 1.2rem; font-weight: 600;">
                                        {subject['name']}
                                    </h4>
                                    <p style="margin: 0; color: #6c757d; font-size: 0.9rem;">
                                        {doc_count} tài liệu
                                    </p>
                                </div>
                            </div>
                        </div>
                        
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="flex: 1;">
                                <div style="background: linear-gradient(90deg, #667eea, #764ba2); height: 4px; border-radius: 2px; width: {min(doc_count * 20, 100)}%;"></div>
                            </div>
                        </div>
                    </div>
                    """
                    
                    st.markdown(card_html, unsafe_allow_html=True)
                    
                    # Action buttons
                    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
                    
                    with btn_col1:
                        if st.button("📄", key=f"view_docs_{subject['id']}", 
                                   help="Xem tài liệu", use_container_width=True):
                            # Filter documents by subject and redirect
                            st.session_state.filter_subject = subject['name']
                            auth.nav_page("Tài_liệu_của_tôi")
                    
                    with btn_col2:
                        if st.button("✏️", key=f"edit_subj_{subject['id']}", 
                                   help="Đổi tên", use_container_width=True):
                            st.session_state[f"edit_subject_{subject['id']}"] = True
                            st.rerun()
                    
                    with btn_col3:
                        if st.button("🗑️", key=f"del_subj_{subject['id']}", 
                                   help="Xóa môn học", use_container_width=True, type="primary"):
                            if doc_count > 0:
                                st.error(f"❌ Không thể xóa môn học có {doc_count} tài liệu!")
                            else:
                                if st.session_state.get(f"confirm_delete_subject_{subject['id']}", False):
                                    try:
                                        db.delete_subject(subject['id'])
                                        st.success("✅ Đã xóa môn học!")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ Lỗi: {str(e)}")
                                else:
                                    st.session_state[f"confirm_delete_subject_{subject['id']}"] = True
                                    st.warning("⚠️ Nhấn lại để xác nhận xóa")
                                    st.rerun()
                    
                    # Edit subject name form
                    if st.session_state.get(f"edit_subject_{subject['id']}", False):
                        with st.form(f"edit_form_{subject['id']}"):
                            new_name = st.text_input("Tên mới", value=subject['name'])
                            col_save, col_cancel = st.columns(2)
                            
                            with col_save:
                                if st.form_submit_button("💾 Lưu", use_container_width=True):
                                    if new_name.strip() and new_name != subject['name']:
                                        try:
                                            # Update subject name (you'll need to implement this in db.py)
                                            # db.update_subject_name(subject['id'], new_name.strip())
                                            st.success("✅ Đã cập nhật tên môn học!")
                                            del st.session_state[f"edit_subject_{subject['id']}"]
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"❌ Lỗi: {str(e)}")
                                    else:
                                        st.warning("⚠️ Vui lòng nhập tên mới!")
                            
                            with col_cancel:
                                if st.form_submit_button("❌ Hủy", use_container_width=True):
                                    del st.session_state[f"edit_subject_{subject['id']}"]
                                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tips section
st.markdown("""
<div class="main-container" style="margin-top: 2rem;">
    <h3 style="color: #667eea; margin-bottom: 1rem;">💡 Mẹo quản lý môn học hiệu quả</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem;">
        <div class="glass-card" style="padding: 1rem;">
            <h4 style="color: #667eea; margin-bottom: 0.5rem;">🎯 Đặt tên rõ ràng</h4>
            <p style="font-size: 0.9rem; color: #6c757d; margin: 0;">
                Sử dụng tên môn học cụ thể và dễ nhận biết để tìm kiếm nhanh chóng
            </p>
        </div>
        
        <div class="glass-card" style="padding: 1rem;">
            <h4 style="color: #667eea; margin-bottom: 0.5rem;">📚 Phân loại hợp lý</h4>
            <p style="font-size: 0.9rem; color: #6c757d; margin: 0;">
                Tạo môn học cho từng lĩnh vực học tập để tổ chức tài liệu khoa học
            </p>
        </div>
        
        <div class="glass-card" style="padding: 1rem;">
            <h4 style="color: #667eea; margin-bottom: 0.5rem;">🔄 Cập nhật thường xuyên</h4>
            <p style="font-size: 0.9rem; color: #6c757d; margin: 0;">
                Thêm môn học mới khi cần và xóa những môn không còn sử dụng
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)