import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from i18n import lang_selector, t, get_lang
st.set_page_config(page_title="Contact", page_icon="✉️", layout="centered")
lang_selector()
lang = get_lang()
T = {
    "title": {"EN": "✉️ Contact", "RU": "✉️ Контакты", "UK": "✉️ Контакти"},
    "name": {"EN": "Vitalii Tereshyn", "RU": "Виталий Терешин", "UK": "Віталій Терешин"},
    "role": {
        "EN": "AI & Data Architect | Turning E-commerce Ops into Autonomous Systems",
        "RU": "AI & Data Architect | Превращаю e-commerce операции в автономные системы",
        "UK": "AI & Data Architect | Перетворюю e-commerce операції на автономні системи",
    },
    "intro": {
        "EN": "I turn e-commerce data into decisions: sales forecasting, analytics and autonomous systems for your task.",
        "RU": "Превращаю данные e-commerce в решения: прогнозирование продаж, аналитику и автономные системы под вашу задачу.",
        "UK": "Перетворюю дані e-commerce на рішення: прогнозування продажів, аналітику та автономні системи під вашу задачу.",
    },
    "stack": {
        "EN": "Amazon · Walmart · Shopify · 1C\n\nETL · PostgreSQL · AI agents · Streamlit",
        "RU": "Amazon · Walmart · Shopify · 1С\n\nETL · PostgreSQL · AI-агенты · Streamlit",
        "UK": "Amazon · Walmart · Shopify · 1С\n\nETL · PostgreSQL · AI-агенти · Streamlit",
    },
    "how_title": {"EN": "How I work", "RU": "Как работаю", "UK": "Як працюю"},
    "s1": {
        "EN": "1. Short call — what hurts, what data you have.",
        "RU": "1. Короткий созвон — что болит, какие данные есть.",
        "UK": "1. Короткий дзвінок — що болить, які дані є.",
    },
    "s2": {
        "EN": "2. Prototype on demo data within a few days.",
        "RU": "2. Прототип на демо-данных за несколько дней.",
        "UK": "2. Прототип на демо-даних за кілька днів.",
    },
    "s3": {
        "EN": "3. Integration into your environment under NDA.",
        "RU": "3. Интеграция в ваш контур под NDA.",
        "UK": "3. Інтеграція у ваш контур під NDA.",
    },
    "footer": {
        "EN": "Real cases and figures shown individually.",
        "RU": "Реальные кейсы и цифры показываю индивидуально.",
        "UK": "Реальні кейси та цифри показую індивідуально.",
    },
}
st.title(T["title"][lang])
st.markdown(f"### {T['name'][lang]}")
st.caption(T["role"][lang])
st.write(T["intro"][lang])
st.caption(T["stack"][lang])
st.divider()
st.markdown("**Telegram:** [@vitter](https://t.me/vitter)")
st.markdown("**Email:** multivitter@gmail.com")
st.markdown("**GitHub:** [github.com/Multivitter](https://github.com/Multivitter)")
st.divider()
st.markdown(f"### {T['how_title'][lang]}")
st.write(f"{T['s1'][lang]}\n\n{T['s2'][lang]}\n\n{T['s3'][lang]}")
st.caption(T["footer"][lang])
