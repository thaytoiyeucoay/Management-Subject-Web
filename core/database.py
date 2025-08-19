from __future__ import annotations
from typing import Any, Dict, List
from datetime import datetime
import io

from utils import db as db_utils

class DatabaseManager:
    """Data layer abstraction over utils.db"""
    def __init__(self, config) -> None:
        self.config = config

    # -------- Aggregations / Stats --------
    def get_user_statistics(self, user_id: str) -> Dict[str, Any]:
        documents = db_utils.get_user_documents(user_id)
        subjects = db_utils.get_user_subjects(user_id)
        total_docs = len(documents or [])
        total_subjects = len(subjects or [])
        # Tags: assume comma-separated string in field 'tags'
        tag_set = set()
        total_size_mb = 0.0
        for d in documents or []:
            tags_field = d.get("tags")
            if tags_field:
                # Support both array and comma-separated string
                if isinstance(tags_field, list):
                    for t in tags_field:
                        t = str(t).strip()
                        if t:
                            tag_set.add(t)
                else:
                    for t in str(tags_field).split(","):
                        t = t.strip()
                        if t:
                            tag_set.add(t)
            size_bytes = d.get("file_size") or 0
            try:
                total_size_mb += float(size_bytes) / (1024 * 1024)
            except Exception:
                pass
        return {
            "total_documents": total_docs,
            "total_subjects": total_subjects,
            "total_tags": len(tag_set),
            "total_size": total_size_mb,
        }

    # -------- Documents --------
    def get_recent_documents(self, user_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        docs = db_utils.get_user_documents(user_id) or []
        # Fallback: sort by created_at desc if present
        try:
            docs.sort(key=lambda x: x.get("created_at"), reverse=True)
        except Exception:
            pass
        return docs[:limit]

    def get_user_documents(self, user_id: str) -> List[Dict[str, Any]]:
        return db_utils.get_user_documents(user_id) or []

    # -------- Subjects --------
    def get_user_subjects(self, user_id: str) -> List[Dict[str, Any]]:
        return db_utils.get_user_subjects(user_id) or []

    def add_subject(self, user_id: str, name: str) -> Dict[str, Any]:
        try:
            db_utils.add_subject(user_id, name)
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def update_subject(self, subject_id: int, name: str) -> Dict[str, Any]:
        try:
            db_utils.update_subject(subject_id, name)
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def delete_subject(self, subject_id: int) -> Dict[str, Any]:
        try:
            db_utils.delete_subject(subject_id)
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}

    # -------- Upload --------
    def upload_document(
        self,
        user_id: str,
        file,
        subject_name: str | None = None,
        tags: str | None = None,
    ) -> Dict[str, Any]:
        try:
            # Build storage path
            ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            safe_name = file.name.replace(" ", "_")
            file_path = f"{user_id}/{ts}_{safe_name}"

            # Upload to storage (pass raw bytes, not BytesIO)
            data = file.read()
            db_utils.upload_file_to_storage(data, file_path)

            # Resolve subject id if provided
            subject_id = None
            if subject_name:
                subjects = self.get_user_subjects(user_id)
                for s in subjects:
                    if s.get("name") == subject_name:
                        subject_id = s.get("id")
                        break

            # Insert metadata
            metadata = {
                "user_id": user_id,
                "file_name": file.name,
                "file_path": file_path,
                "file_size": len(data),
            }
            # Normalize tags to array for Postgres text[]
            if tags is not None:
                parts = [t.strip() for t in str(tags).split(",") if t.strip()]
                metadata["tags"] = parts
            if subject_id:
                metadata["subject_id"] = subject_id

            db_utils.insert_document(metadata)
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}
