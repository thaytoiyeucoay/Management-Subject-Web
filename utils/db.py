# utils/db.py
import streamlit as st
from supabase import create_client, Client
from typing import List, Dict, Any

@st.cache_resource
def init_connection() -> Client:
    """Khởi tạo và trả về client Supabase."""
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase: Client = init_connection()

# --- CÁC HÀM LIÊN QUAN ĐẾN TÀI LIỆU (DOCUMENTS) ---

def get_user_documents(user_id: str) -> List[Dict[str, Any]]:
    """Lấy tất cả tài liệu của một user, sắp xếp theo ngày tạo mới nhất."""
    res = supabase.table("documents").select("*, subjects(name)").eq("user_id", user_id).order("created_at", desc=True).execute()
    return res.data

def insert_document(metadata: Dict[str, Any]) -> None:
    """Chèn thông tin tài liệu vào database."""
    supabase.table("documents").insert(metadata).execute()

def delete_document(doc_id: str, file_path: str) -> None:
    """Xóa tài liệu khỏi Storage và Database."""
    supabase.storage.from_("document_files").remove([file_path])
    supabase.table("documents").delete().eq("id", doc_id).execute()
    
def get_document_by_id(doc_id: str) -> Dict[str, Any]:
    """Lấy thông tin một tài liệu cụ thể bằng ID."""
    res = supabase.table("documents").select("*, subjects(name)").eq("id", doc_id).single().execute()
    return res.data

def update_document_metadata(doc_id: str, updates: Dict[str, Any]) -> None:
    """Cập nhật thông tin của một tài liệu."""
    supabase.table("documents").update(updates).eq("id", doc_id).execute()
    
def upload_file_to_storage(file_bytes, file_path: str):
    """Tải file lên Supabase Storage, nếu tồn tại thì cập nhật."""
    try:
        supabase.storage.from_("document_files").upload(path=file_path, file=file_bytes)
    except Exception as e:
        if "Duplicate" in str(e):
            supabase.storage.from_("document_files").update(path=file_path, file=file_bytes)
        else:
            raise e

# --- CÁC HÀM LIÊN QUAN ĐẾN MÔN HỌC (SUBJECTS) ---

def get_user_subjects(user_id: str) -> List[Dict[str, Any]]:
    """Lấy tất cả môn học của một user."""
    res = supabase.table("subjects").select("id, name").eq("user_id", user_id).order("name").execute()
    return res.data

def add_subject(user_id: str, name: str) -> None:
    """Thêm một môn học mới."""
    supabase.table("subjects").insert({"name": name, "user_id": user_id}).execute()

def delete_subject(subject_id: int) -> None:
    """Xóa một môn học."""
    supabase.table("subjects").delete().eq("id", subject_id).execute()

def update_subject(subject_id: int, name: str) -> None:
    """Cập nhật tên môn học."""
    supabase.table("subjects").update({"name": name}).eq("id", subject_id).execute()

def get_subject_by_id(subject_id: int) -> Dict[str, Any] | None:
    """Lấy thông tin môn học theo ID."""
    res = supabase.table("subjects").select("id, name, user_id").eq("id", subject_id).single().execute()
    return res.data