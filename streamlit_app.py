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

# Пайплайн-строка
st.markdown(
    "<div style='font-size:1.1rem;font-weight:600;color:#475569;margin:0.5rem 0 1rem'>"
    "Amazon · Walmart · Shopify · Weather &nbsp;→&nbsp; PostgreSQL &nbsp;→&nbsp; BI · AI-агенты"
    "</div>",
    unsafe_allow_html=True,
)

st.divider()

# ---------- Как приношу ценность ----------
st.subheader("Как я приношу ценность бизнесу")
st.write("Превращаю разрозненные данные в автономную экосистему:")

c1, c2 = st.columns(2)
with c1:
    st.markdown("#### 🗄️ Единое хранилище")
    st.write("Собираю данные со всех площадок (SP-API, Advertising API, Walmart, Shopify) в консолидированный DWH.")
    st.markdown("#### ⚙️ Полная автоматизация")
    st.write("~50 задач по расписанию, 24/7. Никаких ручных выгрузок.")
    st.markdown("#### 🛡️ Отказоустойчивость")
    st.write("Auto-retry, мониторинг пайплайнов и алерты в Telegram при любом сбое.")
with c2:
    st.markdown("#### 📊 Драйв решений")
    st.write("Интерактивные дашборды, которые обновляются на свежих данных.")
    st.markdown("#### 🤖 AI-автоматизация рутины")
    st.write("Ресток-агенты, PPC-алерты, чат-ассистенты на базе Claude/Gemini.")
    st.markdown("#### 🎯 Результат")
    st.write("Ноль пропущенных сбоев загрузки и высвобождение часов аналитики в неделю.")

st.divider()

# ---------- Кейсы ----------
st.subheader("Кейсы")
st.markdown(
    "Слева в меню — разобранные кейсы с интерактивными дашбордами:\n"
    "- 🛒 **Amazon Analytics** — ETL по SP-API, Buy Box, маржа\n"
    "- 🔄 **ETL Orchestrator** — система держит 4 площадки 24/7\n"
    "- 🔍 **Listing Analyzer** — разбор листинга как продукт (pay-per-run)\n"
    "- 🌦️ **External Data** — погода как сигнал спроса\n"
    "- 🎯 **Competitor Intelligence** — трекинг BSR конкурентов по дням\n"
    "- 🤖 **AI Agents** — агенты на Claude/Gemini"
)

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
