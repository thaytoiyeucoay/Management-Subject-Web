from __future__ import annotations
import streamlit as st
from typing import List, Dict, Any

class UIManager:
    def __init__(self) -> None:
        pass

    # ---------- Base helpers ----------
    def load_css(self) -> None:
        try:
            with open("styles/custom.css", "r", encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except Exception:
            pass

    def hide_sidebar(self) -> None:
        st.markdown(
            """
            <style>
            [data-testid="stSidebar"] { display: none; }
            </style>
            """,
            unsafe_allow_html=True,
        )

    def apply_theme(self, theme: str) -> None:
        """Apply theme by setting data-theme attribute on <html> element."""
        safe_theme = "dark" if theme == "dark" else "light"
        st.markdown(
            f"""
            <script>
            (function() {{
                try {{
                    const el = document.documentElement;
                    el.setAttribute('data-theme', '{safe_theme}');
                    const app = document.querySelector('.stApp');
                    if (app) {{
                        app.setAttribute('data-theme', '{safe_theme}');
                    }}
                }} catch (e) {{}}
            }})();
            </script>
            """,
            unsafe_allow_html=True,
        )

    def render_theme_toggle(self, current: str = "light") -> str:
        """Render a compact theme switcher; returns selected theme ('light'|'dark')."""
        options = {"🌞 Sáng": "light", "🌙 Tối": "dark"}
        labels = list(options.keys())
        default_index = 0 if current != "dark" else 1
        choice = st.selectbox("Giao diện", labels, index=default_index, key="theme_select", help="Chuyển chế độ sáng/tối")
        return options.get(choice, "light")

    # ---------- Components ----------
    def render_user_info(self, email: str) -> None:
        st.markdown(
            f"""
            <div class="glass-card" style="text-align:center; padding:0.75rem;">
                <div style="font-size:1.6rem">👋</div>
                <div style="font-weight:600; color:#667eea;">{email}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def render_page_header(self, title: str, subtitle: str = "") -> None:
        st.markdown(
            f"""
            <div style="padding:1rem 0 1.5rem 0; text-align:left;">
                <h1 style="margin:0;">{title}</h1>
                <p style="color:#6c757d; margin:0.25rem 0 0 0;">{subtitle}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def render_stat_card(self, icon: str, label: str, value: Any, color: str = "#667eea") -> None:
        st.markdown(
            f"""
            <div class="glass-card" style="padding:1rem; text-align:center; border-left:4px solid {color}">
                <div style="font-size:1.8rem">{icon}</div>
                <div style="font-size:1.4rem; font-weight:700">{value}</div>
                <div style="color:#6c757d">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def render_document_list(self, documents: List[Dict[str, Any]], show_actions: bool = False) -> None:
        for d in documents:
            st.markdown(
                f"""
                <div class="glass-card" style="padding:0.75rem 1rem; margin-bottom:0.5rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div style="font-weight:600">{d.get('file_name','(Không tên)')}</div>
                            <div style="color:#6c757d; font-size:0.85rem;">{d.get('subjects',{}).get('name','')} · {d.get('tags','')}</div>
                        </div>
                        <div style="color:#6c757d; font-size:0.85rem;">{d.get('created_at','')}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    def render_document_grid(self, documents: List[Dict[str, Any]], db_manager) -> None:
        cols = st.columns(3)
        for idx, d in enumerate(documents):
            with cols[idx % 3]:
                st.markdown(
                    f"""
                    <div class=\"glass-card\" style=\"padding:1rem; margin-bottom:0.75rem;\">
                        <div style=\"font-size:2rem\">📄</div>
                        <div style=\"font-weight:600\">{d.get('file_name','(Không tên)')}</div>
                        <div style=\"color:#6c757d; font-size:0.85rem\">{d.get('subjects',{}).get('name','')}</div>
                        <div style=\"color:#6c757d; font-size:0.85rem\">{d.get('tags','')}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    def render_file_preview(self, uploaded_file) -> None:
        size_kb = round(len(uploaded_file.getvalue()) / 1024, 1)
        st.info(f"📄 {uploaded_file.name} · {size_kb} KB")

    def render_subjects_grid(self, subjects: List[Dict[str, Any]], db_manager) -> None:
        cols = st.columns(3)
        for idx, s in enumerate(subjects):
            with cols[idx % 3]:
                st.markdown(
                    f"""
                    <div class=\"glass-card\" style=\"padding:1rem; margin-bottom:0.75rem;\">
                        <div style=\"font-size:1.6rem\">📚</div>
                        <div style=\"font-weight:600\">{s.get('name','(Không tên)')}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    def render_empty_state(self, icon: str, title: str, description: str) -> None:
        st.markdown(
            f"""
            <div style=\"text-align:center; padding:2rem; border:1px dashed #e9ecef; border-radius:12px; color:#6c757d\">
                <div style=\"font-size:2rem\">{icon}</div>
                <div style=\"font-weight:700; color:#212529\">{title}</div>
                <div>{description}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
