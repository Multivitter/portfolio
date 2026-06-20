"""
Простой механизм мультиязычности.
Язык хранится в st.session_state, переключатель — в сайдбаре.
t(key) возвращает строку на текущем языке.
"""
import streamlit as st

LANGS = {"EN": "🇬🇧 English", "RU": "🇷🇺 Русский", "UK": "🇺🇦 Українська"}


def get_lang():
    if "lang" not in st.session_state:
        st.session_state.lang = "EN"
    return st.session_state.lang


def lang_selector():
    """Рисует переключатель языка в сайдбаре."""
    current = get_lang()
    codes = list(LANGS.keys())
    choice = st.sidebar.radio(
        "🌐 Language",
        codes,
        index=codes.index(current),
        format_func=lambda c: LANGS[c],
        horizontal=False,
        key="lang_radio",
    )
    st.session_state.lang = choice
    return choice


def t(translations: dict, key: str) -> str:
    """translations — словарь {key: {EN:..., RU:..., UK:...}}. Возвращает строку."""
    lang = get_lang()
    entry = translations.get(key, {})
    return entry.get(lang) or entry.get("EN") or key
