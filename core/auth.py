from __future__ import annotations
from typing import Dict, Any
from utils.db import supabase

class AuthManager:
    """Authentication manager using Supabase."""
    def __init__(self, config) -> None:
        self.config = config

    def login(self, email: str, password: str) -> Dict[str, Any]:
        try:
            supabase.auth.sign_in_with_password({"email": email, "password": password})
            user = supabase.auth.get_user()
            user_data = {
                "id": user.user.id if getattr(user, "user", None) else None,
                "email": user.user.email if getattr(user, "user", None) else email,
            }
            if not user_data["id"]:
                return {"success": False, "message": "Không lấy được thông tin người dùng", "user": None}
            return {"success": True, "message": "Đăng nhập thành công", "user": user_data}
        except Exception as e:
            return {"success": False, "message": str(e), "user": None}

    def register(self, email: str, password: str) -> Dict[str, Any]:
        try:
            supabase.auth.sign_up({"email": email, "password": password})
            return {"success": True, "message": "Đăng ký thành công"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def logout(self) -> None:
        try:
            supabase.auth.sign_out()
        except Exception:
            # Ignore sign out errors to keep UX smooth
            pass

    def current_user(self) -> Dict[str, Any] | None:
        try:
            user = supabase.auth.get_user()
            if getattr(user, "user", None):
                return {"id": user.user.id, "email": user.user.email}
        except Exception:
            pass
        return None
