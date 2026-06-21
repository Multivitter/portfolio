import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from i18n import lang_selector, get_lang

st.set_page_config(page_title="AI Agents", page_icon="🤖", layout="wide")
lang_selector()
lang = get_lang()
_home = {"EN": "🏠 Home", "RU": "🏠 Главная", "UK": "🏠 Головна"}[lang]
st.markdown(
    f"<style>[data-testid='stSidebarNav'] li:first-child a p{{font-size:0}}"
    f"[data-testid='stSidebarNav'] li:first-child a p::before"
    f"{{content:'{_home}';font-size:14px}}</style>",
    unsafe_allow_html=True,
)

T = {
    "title": {"EN": "🤖 Case: AI agents and bots", "RU": "🤖 Кейс: AI-агенты и боты", "UK": "🤖 Кейс: AI-агенти та боти"},
    "cap": {"EN": "Demo. Architecture described without sensitive data.", "RU": "Демо. Описание архитектуры без чувствительных данных.", "UK": "Демо. Опис архітектури без чутливих даних."},
    "build_h": {"EN": "What I build", "RU": "Что строю", "UK": "Що будую"},
    "build": {
        "EN": "Agents that don't just answer, but do the work: watch data, make decisions, send alerts, process inbound.",
        "RU": "Агентов, которые не просто отвечают, а делают работу: следят за данными, принимают решения, шлют алерты, обрабатывают входящие.",
        "UK": "Агентів, які не просто відповідають, а роблять роботу: стежать за даними, ухвалюють рішення, шлють алерти, обробляють вхідні.",
    },
    "a1": {"EN": "📦 Restock agent", "RU": "📦 Агент рестока", "UK": "📦 Агент рестоку"},
    "a1d": {"EN": "Looks at stock, sales velocity and lead times, suggests what and how much to order. On Claude/Gemini.", "RU": "Смотрит на остатки, скорость продаж и сроки поставки, предлагает что и сколько заказывать. На Claude/Gemini.", "UK": "Дивиться на залишки, швидкість продажів і терміни постачання, пропонує що і скільки замовляти. На Claude/Gemini."},
    "a2": {"EN": "📣 PPC alerts", "RU": "📣 PPC-алерты", "UK": "📣 PPC-алерти"},
    "a2d": {"EN": "Catches ad drops and sends a breakdown to Telegram: what fell, a hypothesis, what to check.", "RU": "Ловит просадки по рекламе и шлёт разбор в Telegram: что упало, гипотеза, что проверить.", "UK": "Ловить просадки по рекламі та шле розбір у Telegram: що впало, гіпотеза, що перевірити."},
    "a3": {"EN": "💬 Brand chat agent", "RU": "💬 Чат-агент для бренда", "UK": "💬 Чат-агент для бренду"},
    "a3d": {"EN": "Answers customers in the brand voice, knows the catalog, escalates the hard cases to a human.", "RU": "Отвечает покупателям в стиле бренда, знает каталог, эскалирует сложное человеку.", "UK": "Відповідає покупцям у стилі бренду, знає каталог, ескалює складне людині."},
    "a4": {"EN": "🎓 Learning mentor", "RU": "🎓 Обучающий ментор", "UK": "🎓 Навчальний ментор"},
    "a4d": {"EN": "An FSM Telegram bot with cognitive states — leads a student through the program, adapts to level.", "RU": "Telegram-бот на FSM с когнитивными состояниями — ведёт ученика по программе, адаптируется под уровень.", "UK": "Telegram-бот на FSM з когнітивними станами — веде учня по програмі, адаптується під рівень."},
    "arch_h": {"EN": "Typical architecture", "RU": "Типовая архитектура", "UK": "Типова архітектура"},
    "nda": {"EN": "Real prompts, schemas and integrations — under NDA.", "RU": "Реальные промпты, схемы и интеграции — под NDA.", "UK": "Реальні промпти, схеми та інтеграції — під NDA."},
}

st.title(T["title"][lang])
st.caption(T["cap"][lang])

st.markdown(f"### {T['build_h'][lang]}")
st.write(T["build"][lang])

st.divider()

c1, c2 = st.columns(2)
with c1:
    st.markdown(f"#### {T['a1'][lang]}"); st.write(T["a1d"][lang])
    st.markdown(f"#### {T['a2'][lang]}"); st.write(T["a2d"][lang])
with c2:
    st.markdown(f"#### {T['a3'][lang]}"); st.write(T["a3d"][lang])
    st.markdown(f"#### {T['a4'][lang]}"); st.write(T["a4d"][lang])

st.divider()

st.markdown(f"### {T['arch_h'][lang]}")
st.code(
    "Source (SP-API / scraper / chat)\n"
    "        ↓\n"
    "  PostgreSQL  ←→  Scheduler (run_forever)\n"
    "        ↓\n"
    "   LLM agent (Claude / Gemini)  →  decision / text\n"
    "        ↓\n"
    "  Telegram bot  /  Dashboard  /  DB write",
    language="text",
)

st.info(T["nda"][lang], icon="🔒")
