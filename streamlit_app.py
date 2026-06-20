import streamlit as st
from i18n import lang_selector, t, get_lang

st.set_page_config(
    page_title="Data Architecture Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

lang_selector()

# ---------- Переводы ----------
T = {
    "subtitle": {
        "EN": "I design and build data systems for e-commerce: from raw marketplace APIs to dashboards that drive decisions.",
        "RU": "Проектирую и строю системы данных для e-commerce: от сырых API маркетплейсов до дашбордов, по которым принимают решения.",
        "UK": "Проєктую та будую системи даних для e-commerce: від сирих API маркетплейсів до дашбордів, на основі яких ухвалюють рішення.",
    },
    "value_title": {"EN": "How I create business value", "RU": "Как я приношу ценность бизнесу", "UK": "Яку цінність я приношу бізнесу"},
    "value_intro": {"EN": "I turn scattered data into an autonomous ecosystem:", "RU": "Превращаю разрозненные данные в автономную экосистему:", "UK": "Перетворюю розрізнені дані на автономну екосистему:"},
    "c1_t": {"EN": "Single warehouse", "RU": "Единое хранилище", "UK": "Єдине сховище"},
    "c1_d": {"EN": "All platforms (SP-API, Advertising, Walmart, Shopify) in one DWH", "RU": "Все площадки (SP-API, Advertising, Walmart, Shopify) в одном DWH", "UK": "Усі майданчики (SP-API, Advertising, Walmart, Shopify) в одному DWH"},
    "c2_t": {"EN": "Full automation", "RU": "Полная автоматизация", "UK": "Повна автоматизація"},
    "c2_d": {"EN": "~50 scheduled jobs, 24/7. No manual exports", "RU": "~50 задач по расписанию, 24/7. Никаких ручных выгрузок", "UK": "~50 задач за розкладом, 24/7. Жодних ручних вивантажень"},
    "c3_t": {"EN": "Fault tolerance", "RU": "Отказоустойчивость", "UK": "Відмовостійкість"},
    "c3_d": {"EN": "Auto-retry, pipeline monitoring, Telegram alerts", "RU": "Auto-retry, мониторинг пайплайнов, алерты в Telegram", "UK": "Auto-retry, моніторинг пайплайнів, алерти в Telegram"},
    "c4_t": {"EN": "AI agents", "RU": "AI-агенты", "UK": "AI-агенти"},
    "c4_d": {"EN": "Restock, PPC alerts, chat assistants on Claude/Gemini", "RU": "Ресток, PPC-алерты, чат-ассистенты на Claude/Gemini", "UK": "Ресток, PPC-алерти, чат-асистенти на Claude/Gemini"},
    "c5_t": {"EN": "Decision driver", "RU": "Драйв решений", "UK": "Драйв рішень"},
    "c5_d": {"EN": "Interactive dashboards on fresh data", "RU": "Интерактивные дашборды на свежих данных", "UK": "Інтерактивні дашборди на свіжих даних"},
    "c6_t": {"EN": "Result", "RU": "Результат", "UK": "Результат"},
    "c6_d": {"EN": "Zero missed load failures, hours of analytics freed weekly", "RU": "Ноль пропущенных сбоев, высвобождение часов аналитики в неделю", "UK": "Нуль пропущених збоїв, вивільнення годин аналітики на тиждень"},
    "cases_title": {"EN": "Cases", "RU": "Кейсы", "UK": "Кейси"},
    "cases_intro": {"EN": "In the left menu — detailed cases with interactive dashboards:", "RU": "Слева в меню — разобранные кейсы с интерактивными дашбордами:", "UK": "Зліва в меню — розібрані кейси з інтерактивними дашбордами:"},
    "stack_title": {"EN": "Stack", "RU": "Стек", "UK": "Стек"},
    "nda": {
        "EN": "All figures and names in the demo are synthetic. Real architectures and volumes discussed personally under NDA.",
        "RU": "Все цифры и названия в демо — синтетические. Реальные архитектуры и объёмы обсуждаю персонально под NDA.",
        "UK": "Усі цифри та назви в демо — синтетичні. Реальні архітектури та обсяги обговорюю персонально під NDA.",
    },
    "home_menu": {"EN": "🏠 Home", "RU": "🏠 Главная", "UK": "🏠 Головна"},
}

lang = get_lang()
home_label = T["home_menu"][lang]

# Переименовываем первый пункт меню
st.markdown(
    f"""
    <style>
      [data-testid='stSidebarNav'] li:first-child a p {{ font-size: 0; }}
      [data-testid='stSidebarNav'] li:first-child a p::before {{
        content: '{home_label}'; font-size: 14px;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Шапка ----------
st.title("📊 Data Architecture Portfolio")
st.markdown(f"#### {T['subtitle'][lang]}")

st.markdown(
    "<div style='background:#1A1D24;border-radius:10px;padding:12px 16px;"
    "font-size:1.05rem;font-weight:600;color:#cbd5e1;margin:0.5rem 0 1.5rem'>"
    "Amazon · Walmart · Shopify · Weather &nbsp;→&nbsp; PostgreSQL &nbsp;→&nbsp; BI · AI-agents"
    "</div>",
    unsafe_allow_html=True,
)

# ---------- Ценность ----------
st.subheader(T["value_title"][lang])
st.write(T["value_intro"][lang])

def card(icon, title, text):
    return (
        f"<div style='background:#1A1D24;border-radius:10px;padding:16px 18px;height:100%;'>"
        f"<div style='font-size:1.05rem;font-weight:600;margin-bottom:4px'>{icon} {title}</div>"
        f"<div style='font-size:0.9rem;color:#94a3b8;line-height:1.5'>{text}</div></div>"
    )

r1c1, r1c2 = st.columns(2)
with r1c1: st.markdown(card("🗄️", T["c1_t"][lang], T["c1_d"][lang]), unsafe_allow_html=True)
with r1c2: st.markdown(card("⚙️", T["c2_t"][lang], T["c2_d"][lang]), unsafe_allow_html=True)
st.write("")
r2c1, r2c2 = st.columns(2)
with r2c1: st.markdown(card("🛡️", T["c3_t"][lang], T["c3_d"][lang]), unsafe_allow_html=True)
with r2c2: st.markdown(card("🤖", T["c4_t"][lang], T["c4_d"][lang]), unsafe_allow_html=True)
st.write("")
r3c1, r3c2 = st.columns(2)
with r3c1: st.markdown(card("📊", T["c5_t"][lang], T["c5_d"][lang]), unsafe_allow_html=True)
with r3c2: st.markdown(card("🎯", T["c6_t"][lang], T["c6_d"][lang]), unsafe_allow_html=True)

st.divider()

# ---------- Кейсы ----------
st.subheader(T["cases_title"][lang])
st.write(T["cases_intro"][lang])
tags = ["🛒 Amazon Analytics", "🔄 ETL Orchestrator", "🔍 Listing Analyzer",
        "🌦️ External Data", "🎯 Competitor Intelligence", "🧩 Semantic Core", "🤖 AI Agents"]
tags_html = "".join(
    f"<span style='display:inline-block;background:#1e3a5f;color:#93c5fd;"
    f"padding:6px 14px;border-radius:8px;margin:4px 6px 4px 0;font-size:0.9rem'>{x}</span>"
    for x in tags
)
st.markdown(f"<div>{tags_html}</div>", unsafe_allow_html=True)

st.divider()

# ---------- Стек ----------
st.subheader(T["stack_title"][lang])
st.markdown(
    "**Ingestion & APIs:** `Python` `Amazon SP-API` `Advertising API` `Walmart API` `Shopify API` `Weather APIs`  \n"
    "**Storage & Processing:** `PostgreSQL` `SQL` `custom ETL orchestrator`  \n"
    "**Presentation & AI:** `Streamlit` `Claude API` `Gemini API` `Telegram Bot API`  \n"
    "**Infra & DevOps:** `Docker` `Git` `Supabase / Heroku`"
)

st.divider()
st.info(T["nda"][lang], icon="🔒")
st.caption("Made with Streamlit")
