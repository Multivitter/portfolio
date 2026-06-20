import streamlit as st

st.set_page_config(
    page_title="Data Architecture Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Шапка ----------
st.title("📊 Data Architecture Portfolio")
st.markdown(
    "#### Проектирую и строю системы данных для e-commerce: "
    "от сырых API маркетплейсов до дашбордов, по которым принимают решения."
)

st.markdown(
    "<div style='background:#1A1D24;border-radius:10px;padding:12px 16px;"
    "font-size:1.05rem;font-weight:600;color:#cbd5e1;margin:0.5rem 0 1.5rem'>"
    "Amazon · Walmart · Shopify · Weather &nbsp;→&nbsp; PostgreSQL &nbsp;→&nbsp; BI · AI-агенты"
    "</div>",
    unsafe_allow_html=True,
)

# ---------- Ценность (карточки) ----------
st.subheader("Как я приношу ценность бизнесу")
st.write("Превращаю разрозненные данные в автономную экосистему:")

def card(icon, title, text):
    return (
        f"<div style='background:#1A1D24;border-radius:10px;padding:16px 18px;"
        f"height:100%;'>"
        f"<div style='font-size:1.05rem;font-weight:600;margin-bottom:4px'>{icon} {title}</div>"
        f"<div style='font-size:0.9rem;color:#94a3b8;line-height:1.5'>{text}</div>"
        f"</div>"
    )

r1c1, r1c2 = st.columns(2)
with r1c1:
    st.markdown(card("🗄️", "Единое хранилище", "Все площадки (SP-API, Advertising, Walmart, Shopify) в одном DWH"), unsafe_allow_html=True)
with r1c2:
    st.markdown(card("⚙️", "Полная автоматизация", "~50 задач по расписанию, 24/7. Никаких ручных выгрузок"), unsafe_allow_html=True)

st.write("")
r2c1, r2c2 = st.columns(2)
with r2c1:
    st.markdown(card("🛡️", "Отказоустойчивость", "Auto-retry, мониторинг пайплайнов, алерты в Telegram"), unsafe_allow_html=True)
with r2c2:
    st.markdown(card("🤖", "AI-агенты", "Ресток, PPC-алерты, чат-ассистенты на Claude/Gemini"), unsafe_allow_html=True)

st.write("")
r3c1, r3c2 = st.columns(2)
with r3c1:
    st.markdown(card("📊", "Драйв решений", "Интерактивные дашборды на свежих данных"), unsafe_allow_html=True)
with r3c2:
    st.markdown(card("🎯", "Результат", "Ноль пропущенных сбоев, высвобождение часов аналитики в неделю"), unsafe_allow_html=True)

st.divider()

# ---------- Кейсы (теги) ----------
st.subheader("Кейсы")
st.write("Слева в меню — разобранные кейсы с интерактивными дашбордами:")

tags = ["🛒 Amazon Analytics", "🔄 ETL Orchestrator", "🔍 Listing Analyzer",
        "🌦️ External Data", "🎯 Competitor Intelligence", "🤖 AI Agents"]
tags_html = "".join(
    f"<span style='display:inline-block;background:#1e3a5f;color:#93c5fd;"
    f"padding:6px 14px;border-radius:8px;margin:4px 6px 4px 0;font-size:0.9rem'>{t}</span>"
    for t in tags
)
st.markdown(f"<div>{tags_html}</div>", unsafe_allow_html=True)

st.divider()

# ---------- Стек ----------
st.subheader("Стек")
st.markdown(
    "**Ingestion & APIs:** `Python` `Amazon SP-API` `Advertising API` `Walmart API` `Shopify API` `Weather APIs`  \n"
    "**Storage & Processing:** `PostgreSQL` `SQL` `кастомный ETL-оркестратор`  \n"
    "**Presentation & AI:** `Streamlit` `Claude API` `Gemini API` `Telegram Bot API`  \n"
    "**Infra & DevOps:** `Docker` `Git` `Heroku / Cloud`"
)

st.divider()

st.info(
    "Все цифры и названия в демо — синтетические. "
    "Реальные архитектуры и объёмы обсуждаю персонально под NDA.",
    icon="🔒",
)
st.caption("Made with Streamlit")
