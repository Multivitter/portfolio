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
    "demo_h": {"EN": "🧠 AI Insights — agent in action (demo)", "RU": "🧠 AI Insights — агент в действии (демо)", "UK": "🧠 AI Insights — агент у дії (демо)"},
    "demo_intro": {
        "EN": "The agent doesn't just chat — it reads the data and gives a verdict with numbers and a recommendation. Pick a question:",
        "RU": "Агент не просто болтает — он читает данные и выдаёт вердикт с цифрами и рекомендацией. Выбери вопрос:",
        "UK": "Агент не просто балакає — він читає дані та видає вердикт з цифрами та рекомендацією. Обери питання:",
    },
    "q1": {"EN": "What needs attention right now?", "RU": "Что требует внимания прямо сейчас?", "UK": "Що потребує уваги прямо зараз?"},
    "q2": {"EN": "Which SKUs risk out-of-stock in 14 days?", "RU": "Какие SKU под риском out-of-stock за 14 дней?", "UK": "Які SKU під ризиком out-of-stock за 14 днів?"},
    "q3": {"EN": "Where do we lose the most — fees, refunds or promos?", "RU": "Где теряем больше — fees, refunds или промо?", "UK": "Де втрачаємо більше — fees, refunds чи промо?"},
    "a1": {
        "EN": "🔴 **Priority: SKU HOOD-ZIP-03.** Buy Box dropped to 41% over 3 days (was 88%) — a competitor undercut price by ~6%. Estimated loss ~$1,200/week. **Action:** match price or enable a coupon, recheck in 24h.",
        "RU": "🔴 **Приоритет: SKU HOOD-ZIP-03.** Buy Box упал до 41% за 3 дня (было 88%) — конкурент сбил цену на ~6%. Оценка потерь ~$1,200/нед. **Действие:** сматчить цену или включить купон, перепроверить через 24ч.",
        "UK": "🔴 **Пріоритет: SKU HOOD-ZIP-03.** Buy Box упав до 41% за 3 дні (було 88%) — конкурент збив ціну на ~6%. Оцінка втрат ~$1,200/тиж. **Дія:** зматчити ціну або ввімкнути купон, перевірити через 24г.",
    },
    "a2": {
        "EN": "⚠️ **2 SKUs at risk.** WOOL-SOCK-01: 18 days of stock left, but lead time is 21 days → gap of 3 days. BASE-TEE-02: sales accelerating +40%, will run out in ~12 days. **Action:** place a restock order for both today.",
        "RU": "⚠️ **2 SKU под риском.** WOOL-SOCK-01: остаток на 18 дней, но срок поставки 21 день → разрыв 3 дня. BASE-TEE-02: продажи ускоряются +40%, кончится за ~12 дней. **Действие:** разместить заказ на ресток по обоим сегодня.",
        "UK": "⚠️ **2 SKU під ризиком.** WOOL-SOCK-01: залишок на 18 днів, але термін постачання 21 день → розрив 3 дні. BASE-TEE-02: продажі прискорюються +40%, закінчиться за ~12 днів. **Дія:** розмістити замовлення на ресток по обох сьогодні.",
    },
    "a3": {
        "EN": "💸 **Fees are the biggest leak: 29% of gross.** Refunds 17%, promos only 3%. Within fees, FBA storage grew +22% MoM — slow-movers eating fees. **Action:** review storage for the bottom-10 SKUs by turnover, consider removal/liquidation.",
        "RU": "💸 **Больше всего утекает в fees: 29% от валовой.** Refunds 17%, промо лишь 3%. Внутри fees хранение FBA выросло +22% м/м — медленные товары едят комиссию. **Действие:** разобрать хранение по 10 худшим SKU по оборачиваемости, рассмотреть вывоз/ликвидацию.",
        "UK": "💸 **Найбільше витікає у fees: 29% від валової.** Refunds 17%, промо лише 3%. Усередині fees зберігання FBA зросло +22% м/м — повільні товари їдять комісію. **Дія:** розібрати зберігання по 10 найгірших SKU за оборотністю, розглянути вивіз/ліквідацію.",
    },
    "demo_cap": {"EN": "Demo answers on synthetic data. The real agent runs on Claude/Gemini over live DB.", "RU": "Демо-ответы на синтетике. Реальный агент работает на Claude/Gemini поверх живой БД.", "UK": "Демо-відповіді на синтетиці. Реальний агент працює на Claude/Gemini поверх живої БД."},
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

# ---------- AI Insights демо ----------
st.markdown(f"### {T['demo_h'][lang]}")
st.write(T["demo_intro"][lang])

questions = [T["q1"][lang], T["q2"][lang], T["q3"][lang]]
answers = {T["q1"][lang]: T["a1"][lang], T["q2"][lang]: T["a2"][lang], T["q3"][lang]: T["a3"][lang]}

if "ai_pick" not in st.session_state:
    st.session_state.ai_pick = questions[0]

cols = st.columns(3)
for i, q in enumerate(questions):
    if cols[i].button(q, use_container_width=True, key=f"q{i}"):
        st.session_state.ai_pick = q

with st.chat_message("assistant"):
    st.markdown(answers[st.session_state.ai_pick])

st.caption(T["demo_cap"][lang])

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
