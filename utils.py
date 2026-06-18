# utils.py
"""
Utility helpers for the Streamlit app.
"""

from __future__ import annotations

import os
from typing import Optional, Dict, List

import streamlit as st


def load_api_key_from_secrets() -> Optional[str]:
    """
    Load API key from Streamlit secrets or environment variables.
    Streamlit Cloud: set OPENAI_API_KEY in app secrets.
    Local dev: set OPENAI_API_KEY in environment or use .env.
    """
    if "OPENAI_API_KEY" in st.secrets:
        return st.secrets["OPENAI_API_KEY"]
    return os.getenv("OPENAI_API_KEY")


def init_session_state() -> None:
    """Initialize session state keys used by the app."""
    if "conversation" not in st.session_state:
        st.session_state.conversation = []  # type: List[Dict[str, str]]
    if "metadata" not in st.session_state:
        st.session_state.metadata = {}
