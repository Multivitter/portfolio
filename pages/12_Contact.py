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
        "EN": "Happy to discuss launching a brand on Amazon, analytics, automation or AI agents for your task.",
        "RU": "Готов обсудить вывод бренда на Amazon, аналитику, автоматизацию или AI-агентов под вашу задачу.",
        "UK": "Готовий обговорити вихід бренду на Amazon, аналітику, автоматизацію або AI-агентів під вашу задачу.",
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
st.divider()
st.markdown("**Telegram:** [@vitter](https://t.me/vitter)")
st.markdown("**Email:** multivitter@gmail.com")
st.markdown("**GitHub:** [github.com/Multivitter](https://github.com/Multivitter)")
st.divider()
st.markdown(f"### {T['how_title'][lang]}")
st.write(f"{T['s1'][lang]}\n\n{T['s2'][lang]}\n\n{T['s3'][lang]}")
st.caption(T["footer"][lang])
