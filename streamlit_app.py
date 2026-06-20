import streamlit as st

st.set_page_config(
    page_title="Portfolio · Data & Amazon Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Шапка ----------
col1, col2 = st.columns([1, 3])
with col1:
    st.markdown("## 👋")
with col2:
    st.title("Аналитика данных · Amazon · AI-агенты")
    st.markdown(
        "Строю системы, которые превращают сырые данные "
        "(SP-API, парсинг, цены) в решения: дашборды, боты, авто-пайплайны."
    )

st.divider()

# ---------- Что я делаю ----------
st.subheader("Что я делаю")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("#### 🛒 Amazon-аналитика")
    st.write(
        "ETL по SP-API, мониторинг Buy Box, маржа по SKU, "
        "анализ возвратов и отзывов, авто-запросы отзывов."
    )
with c2:
    st.markdown("#### 🤖 AI-агенты и боты")
    st.write(
        "Telegram-боты, агенты на Claude/Gemini для рестока, "
        "PPC-алертов, парсинга и обработки данных."
    )
with c3:
    st.markdown("#### 🔎 Парсинг и BI")
    st.write(
        "Каталоги запчастей, конкурентная разведка, "
        "Streamlit-дашборды на PostgreSQL."
    )

st.divider()

# ---------- Стек ----------
st.subheader("Стек")
st.markdown(
    "`Python` · `PostgreSQL` · `Streamlit` · `Amazon SP-API` · "
    "`Telegram Bot API` · `Claude / Gemini API` · `Google Sheets API` · "
    "`Docker` · `Heroku / Cloud`"
)

st.divider()

# ---------- Призыв ----------
st.subheader("Кейсы")
st.markdown(
    "Слева в меню — разобранные кейсы с интерактивными дашбордами "
    "(данные обезличены/демо). Контакты — на странице **Contact**."
)

st.info(
    "Все цифры и названия в демо — синтетические. "
    "Реальные проекты обсуждаю индивидуально под NDA.",
    icon="🔒",
)

st.caption("Made with Streamlit")
