"""
Подключение к Supabase через официальный клиент (REST API).
URL и publishable-ключ берутся из st.secrets — не из кода.
Publishable-ключ даёт только то, что разрешено RLS (у нас — read-only).
Если секретов нет или база недоступна — функции вернут None,
и страницы используют синтетический fallback.
"""
import streamlit as st
import pandas as pd


@st.cache_resource
def get_client():
    """Создаёт Supabase client из секретов. None, если секретов нет."""
    try:
        from supabase import create_client
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")
        if not url or not key:
            return None
        return create_client(url, key)
    except Exception:
        return None


@st.cache_data(ttl=600)
def fetch_table(table: str, columns: str = "*", order_by: str | None = None):
    """Читает таблицу через Supabase client. None при ошибке/без подключения."""
    client = get_client()
    if client is None:
        return None
    try:
        q = client.table(table).select(columns)
        if order_by:
            q = q.order(order_by)
        # пагинация: Supabase отдаёт максимум 1000 строк за раз
        rows, start, page = [], 0, 1000
        while True:
            resp = q.range(start, start + page - 1).execute()
            batch = resp.data or []
            rows.extend(batch)
            if len(batch) < page:
                break
            start += page
        return pd.DataFrame(rows) if rows else None
    except Exception:
        return None


def db_badge(is_live: bool):
    """Бейдж-индикатор: данные из базы или демо-fallback."""
    if is_live:
        st.success("Данные из Supabase (PostgreSQL, live)", icon="🟢")
    else:
        st.info("Демо-режим (синтетика). Подключи Supabase через st.secrets для live-данных.", icon="🔵")
