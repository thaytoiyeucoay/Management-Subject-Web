import streamlit as st

class Config:
    """Application configuration wrapper."""
    def __init__(self) -> None:
        # Secrets for Supabase
        self.supabase_url: str = st.secrets.get("SUPABASE_URL", "")
        self.supabase_key: str = st.secrets.get("SUPABASE_KEY", "")
        # Storage bucket name
        self.storage_bucket: str = "document_files"
        # UI config
        self.css_path: str = "styles/custom.css"
