import streamlit as st

st.set_page_config(
    page_title="Data Architecture Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Перейменовуємо перший пункт меню "streamlit app" → "Головна"
st.markdown(
    """
    <style>
      [data-testid='stSidebarNav'] li:first-child a p { font-size: 0; }
      [data-testid='stSidebarNav'] li:first-child a p::before {
        content: '🏠 Головна'; font-size: 14px;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Шапка ----------
st.title("📊 Data Architecture Portfolio")
st.markdown(
    "#### Проєктую та будую системи даних для e-commerce: "
    "від сирих API маркетплейсів до дашбордів, на основі яких ухвалюють рішення."
)

st.markdown(
    "<div style='background:#1A1D24;border-radius:10px;padding:12px 16px;"
    "font-size:1.05rem;font-weight:600;color:#cbd5e1;margin:0.5rem 0 1.5rem'>"
    "Amazon · Walmart · Shopify · Weather &nbsp;→&nbsp; PostgreSQL &nbsp;→&nbsp; BI · AI-агенти"
    "</div>",
    unsafe_allow_html=True,
)

# ---------- Цінність (картки) ----------
st.subheader("Яку цінність я приношу бізнесу")
st.write("Перетворюю розрізнені дані на автономну екосистему:")

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
    st.markdown(card("🗄️", "Єдине сховище", "Усі майданчики (SP-API, Advertising, Walmart, Shopify) в одному DWH"), unsafe_allow_html=True)
with r1c2:
    st.markdown(card("⚙️", "Повна автоматизація", "~50 задач за розкладом, 24/7. Жодних ручних вивантажень"), unsafe_allow_html=True)

st.write("")
r2c1, r2c2 = st.columns(2)
with r2c1:
    st.markdown(card("🛡️", "Відмовостійкість", "Auto-retry, моніторинг пайплайнів, алерти в Telegram"), unsafe_allow_html=True)
with r2c2:
    st.markdown(card("🤖", "AI-агенти", "Ресток, PPC-алерти, чат-асистенти на Claude/Gemini"), unsafe_allow_html=True)

st.write("")
r3c1, r3c2 = st.columns(2)
with r3c1:
    st.markdown(card("📊", "Драйв рішень", "Інтерактивні дашборди на свіжих даних"), unsafe_allow_html=True)
with r3c2:
    st.markdown(card("🎯", "Результат", "Нуль пропущених збоїв, вивільнення годин аналітики на тиждень"), unsafe_allow_html=True)

st.divider()

# ---------- Кейси (теги) ----------
st.subheader("Кейси")
st.write("Зліва в меню — розібрані кейси з інтерактивними дашбордами:")

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
    "**Storage & Processing:** `PostgreSQL` `SQL` `кастомний ETL-оркестратор`  \n"
    "**Presentation & AI:** `Streamlit` `Claude API` `Gemini API` `Telegram Bot API`  \n"
    "**Infra & DevOps:** `Docker` `Git` `Heroku / Cloud`"
)

st.divider()

st.info(
    "Усі цифри та назви в демо — синтетичні. "
    "Реальні архітектури та обсяги обговорюю персонально під NDA.",
    icon="🔒",
)
st.caption("Made with Streamlit")
