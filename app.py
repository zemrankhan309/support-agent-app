# app.py
"""
Streamlit front-end for Customer Support Intelligence.

- Modular: uses llm_client.py and utils.py
- No hardcoded secrets. Use st.secrets or environment variables.
- Designed for local VS Code and Streamlit Community Cloud deployment.
"""

from __future__ import annotations

import streamlit as st
from pydantic import ValidationError

from llm_client import LLMClient, LLMConfig
from utils import load_api_key_from_secrets, init_session_state

# Page config
st.set_page_config(page_title="Customer Support Intelligence", page_icon="💬", layout="wide")


def render_sidebar(config: LLMConfig) -> LLMConfig:
    st.sidebar.title("⚙️ LLM Configuration")
    st.sidebar.caption("Adjust model and generation parameters")

    model = st.sidebar.text_input("Model", value=config.model)
    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, value=config.temperature, step=0.05)
    max_tokens = st.sidebar.slider("Max tokens", 64, 4096, value=config.max_tokens, step=64)
    system_prompt = st.sidebar.text_area("System prompt", value=config.system_prompt, height=160)

    try:
        updated = LLMConfig(
            provider=config.provider,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            system_prompt=system_prompt,
        )
        return updated
    except ValidationError as exc:
        st.sidebar.error(f"Invalid configuration: {exc}")
        return config


def render_header() -> None:
    st.title("🛠️ Customer Support Intelligence")
    st.markdown(
        "LLM-powered assistant for customer support agents. "
        "Use the chat to ask questions, summarize tickets, or generate responses."
    )


def render_conversation() -> None:
    """Render chat history using Streamlit chat components."""
    for msg in st.session_state.conversation:
        role = msg.get("role", "assistant")
        content = msg.get("content", "")
        if role == "user":
            with st.chat_message("user"):
                st.markdown(content)
        else:
            with st.chat_message("assistant"):
                st.markdown(content)


def append_message(role: str, content: str) -> None:
    st.session_state.conversation.append({"role": role, "content": content})


def main() -> None:
    init_session_state()

    # Default LLM config
    default_config = LLMConfig()
    llm_config = render_sidebar(default_config)

    api_key = load_api_key_from_secrets()
    if not api_key:
        st.error(
            "No API key found. Set OPENAI_API_KEY in Streamlit secrets or as an environment variable."
        )
        st.stop()

    # Instantiate client
    try:
        client = LLMClient(config=llm_config, api_key=api_key)
    except Exception as exc:
        st.error(f"Failed to initialize LLM client: {exc}")
        st.stop()

    render_header()

    col_chat, col_meta = st.columns([3, 1])

    with col_chat:
        st.subheader("💬 Chat")
        render_conversation()

        user_input = st.chat_input("Type a customer question, paste a ticket, or ask for a summary...")
        if user_input:
            append_message("user", user_input)

            # Example: plug-in point for RAG / KB retrieval or CRM lookup
            extra_context = None
            # If you have notebook logic that extracts customer profile or ticket history,
            # call it here and set extra_context accordingly.

            with st.chat_message("assistant"):
                with st.spinner("Generating response..."):
                    response = client.generate_response(
                        user_query=user_input,
                        conversation_history=st.session_state.conversation,
                        extra_context=extra_context,
                    )
                    st.markdown(response)
            append_message("assistant", response)

    with col_meta:
        st.subheader("📊 Insights")
        st.markdown(
            "- **Messages:** " f"{len(st.session_state.conversation)}\n\n"
            "- **Suggested actions:** Placeholder for macros, escalation rules, and tags.\n\n"
            "- **Ticket summary:** Use the LLM to summarize long tickets (example button below)."
        )

        if st.button("Summarize last user message"):
            # Find last user message
            last_user = next(
                (m["content"] for m in reversed(st.session_state.conversation) if m["role"] == "user"),
                None,
            )
            if not last_user:
                st.info("No user message to summarize.")
            else:
                with st.spinner("Summarizing..."):
                    summary_prompt = (
                        "Please provide a concise support-ticket summary (3-5 bullet points) "
                        "for the following customer message. Include detected intent and urgency.\n\n"
                        f"{last_user}"
                    )
                    summary = client.generate_response(
                        user_query=summary_prompt,
                        conversation_history=st.session_state.conversation,
                    )
                    st.markdown("**Summary**")
                    st.markdown(summary)

        if st.button("Clear conversation"):
            st.session_state.conversation = []
            st.experimental_rerun()


if __name__ == "__main__":
    main()
