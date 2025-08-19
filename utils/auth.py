# utils/auth.py
import streamlit as st
import streamlit.components.v1 as components
from .db import supabase

def get_user_id() -> str | None:
    """Lấy user_id từ session state."""
    if st.session_state.get("user_session"):
        return st.session_state.user_session.user.id
    return None

def get_user_email() -> str | None:
    """Lấy email của user từ session state."""
    if st.session_state.get("user_session"):
        return st.session_state.user_session.user.email
    return None

def nav_page(page_name, timeout_secs=3):
    """Navigates to a page in a multipage app.

    Args:
        page_name (str): The name of the page to navigate to.
        timeout_secs (int, optional): The number of seconds to wait for the page to load. Defaults to 3.
    """
    nav_script = f"""
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {{
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {{
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {{
                        links[i].click();
                        return;
                    }}
                }}
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {{
                    setTimeout(function() {{
                        attempt_nav_page(page_name, start_time, timeout_secs);
                    }}, 100);
                }}
            }}
            window.addEventListener("load", function() {{
                attempt_nav_page('{page_name}', new Date(), {timeout_secs});
            }});
        </script>
    """
    components.html(nav_script, height=0)