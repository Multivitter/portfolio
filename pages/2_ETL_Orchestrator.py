import streamlit as st
import pandas as pd
import base64
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from i18n import lang_selector, get_lang

st.set_page_config(page_title="ETL Orchestrator", page_icon="🔄", layout="wide")
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
    "title": {"EN": "🔄 Case: multi-marketplace ETL orchestrator", "RU": "🔄 Кейс: ETL-оркестратор мультимаркетплейс", "UK": "🔄 Кейс: ETL-оркестратор мультимаркетплейс"},
    "cap": {"EN": "One process keeps all e-commerce analytics 24/7. Data/names anonymized.", "RU": "Один процесс держит всю аналитику e-commerce 24/7. Данные/названия обезличены.", "UK": "Один процес тримає всю аналітику e-commerce 24/7. Дані/назви знеособлені."},
    "arch": {"EN": "Architecture", "RU": "Архитектура", "UK": "Архітектура"},
    "task_h": {"EN": "Task", "RU": "Задача", "UK": "Задача"},
    "task": {
        "EN": "A seller works on several platforms at once (Amazon, Walmart, Shopify). Data is scattered, exports manual, nobody notices a load failure until the numbers in a report drift. A single system is needed that pulls data on schedule, stores it in one place, watches itself and reports problems.",
        "RU": "Продавец работает сразу на нескольких площадках (Amazon, Walmart, Shopify). Данные разрозненные, выгрузки ручные, никто не замечает сбой загрузки, пока цифры в отчёте не «поедут». Нужна единая система, которая сама тянет данные по расписанию, складывает в одно хранилище, следит за собой и сообщает о проблемах.",
        "UK": "Продавець працює одразу на кількох майданчиках (Amazon, Walmart, Shopify). Дані розрізнені, вивантаження ручні, ніхто не помічає збій завантаження, поки цифри у звіті не «поїдуть». Потрібна єдина система, що сама тягне дані за розкладом, складає в одне сховище, стежить за собою та повідомляє про проблеми.",
    },
    "sol_h": {"EN": "Solution", "RU": "Решение", "UK": "Рішення"},
    "sol": {
        "EN": "A single orchestrator process: a schedule of ~50 tasks, a worker pool, background table monitors, auto-restart on failures, double-run protection and Telegram summaries.",
        "RU": "Единый процесс-оркестратор: расписание из ~50 задач, пул воркеров, фоновые мониторы за таблицами, авто-перезапуск при сбоях, защита от двойного запуска и сводки в Telegram.",
        "UK": "Єдиний процес-оркестратор: розклад із ~50 задач, пул воркерів, фонові монітори за таблицями, авто-перезапуск при збоях, захист від подвійного запуску та зведення в Telegram.",
    },
    "scale": {"EN": "System scale", "RU": "Масштаб системы", "UK": "Масштаб системи"},
    "m_tasks": {"EN": "Scheduled tasks", "RU": "Задач по графику", "UK": "Задач за розкладом"},
    "m_plat": {"EN": "Platforms", "RU": "Площадок", "UK": "Майданчиків"},
    "m_mon": {"EN": "Background monitors", "RU": "Фоновых мониторов", "UK": "Фонових моніторів"},
    "m_up": {"EN": "Uptime", "RU": "Аптайм", "UK": "Аптайм"},
    "rel_h": {"EN": "What makes the system reliable", "RU": "Что делает систему надёжной", "UK": "Що робить систему надійною"},
    "r1t": {"EN": "🔁 Auto-retry", "RU": "🔁 Auto-retry", "UK": "🔁 Auto-retry"},
    "r1d": {"EN": "Up to 3 retries with growing pause. Then a critical alert and stop, to avoid hammering the API.", "RU": "До 3 повторов с нарастающей паузой. После — критический алерт и стоп, чтобы не долбить API.", "UK": "До 3 повторів зі зростаючою паузою. Після — критичний алерт і стоп, щоб не довбати API."},
    "r2t": {"EN": "🔒 Double-run protection", "RU": "🔒 Защита от двойного запуска", "UK": "🔒 Захист від подвійного запуску"},
    "r2d": {"EN": "A unique task key while running — the same task won't start twice.", "RU": "Уникальный ключ задачи на время выполнения — одна и та же задача не стартует дважды.", "UK": "Унікальний ключ задачі на час виконання — одна й та сама задача не стартує двічі."},
    "r3t": {"EN": "👀 Background monitors", "RU": "👀 Фоновые мониторы", "UK": "👀 Фонові монітори"},
    "r3d": {"EN": "Watch tables: date or row count changed → event breakdown in Telegram.", "RU": "Следят за таблицами: изменилась дата или счётчик строк → разбор события в Telegram.", "UK": "Стежать за таблицями: змінилася дата або лічильник рядків → розбір події в Telegram."},
    "r4t": {"EN": "📊 Daily summary", "RU": "📊 Ежедневная сводка", "UK": "📊 Щоденне зведення"},
    "r4d": {"EN": "Once a day — overview of all loaders: runs, rows, errors, by group.", "RU": "Раз в сутки — overview по всем загрузчикам: сколько запусков, строк, ошибок, по группам.", "UK": "Раз на добу — overview по всіх завантажувачах: скільки запусків, рядків, помилок, по групах."},
    "load_h": {"EN": "How load is distributed over a day", "RU": "Как распределена нагрузка по суткам", "UK": "Як розподілене навантаження по добі"},
    "load_cap": {"EN": "Representative schedule slice (task categories, no implementation detail).", "RU": "Условный срез расписания (категории задач, без деталей реализации).", "UK": "Умовний зріз розкладу (категорії задач, без деталей реалізації)."},
    "col_time": {"EN": "Time", "RU": "Время", "UK": "Час"},
    "col_task": {"EN": "Task", "RU": "Задача", "UK": "Задача"},
    "col_plat": {"EN": "Platform", "RU": "Площадка", "UK": "Майданчик"},
    "dist": {"EN": "Distribution by platform (in this slice)", "RU": "Распределение по площадкам (в этом срезе)", "UK": "Розподіл по майданчиках (у цьому зрізі)"},
    "under_h": {"EN": "⚙️ Under the hood (for technical audience)", "RU": "⚙️ Под капотом (для технической аудитории)", "UK": "⚙️ Під капотом (для технічної аудиторії)"},
    "under": {"EN": "Python, threads + ThreadPoolExecutor, per-task timeouts, ETL log in PostgreSQL, stdout parsing for alert metrics, monitors on daemon threads.", "RU": "Python, потоки + ThreadPoolExecutor, отдельные таймауты на каждый тип задачи, ETL-лог в PostgreSQL, парсинг stdout для метрик в алерты, мониторы на daemon-потоках.", "UK": "Python, потоки + ThreadPoolExecutor, окремі таймаути на кожен тип задачі, ETL-лог у PostgreSQL, парсинг stdout для метрик в алерти, монітори на daemon-потоках."},
    "nda": {"EN": "Real brand names, DB schemas and tokens — under NDA.", "RU": "Реальные названия брендов, схемы БД и токены — под NDA.", "UK": "Реальні назви брендів, схеми БД і токени — під NDA."},
}

st.title(T["title"][lang])
st.caption(T["cap"][lang])

st.markdown(f"### {T['arch'][lang]}")
_svg = Path(__file__).parent.parent / "assets" / "orchestrator_architecture.svg"
if _svg.exists():
    b64 = base64.b64encode(_svg.read_text(encoding="utf-8").encode("utf-8")).decode("utf-8")
    st.markdown(
        f'<div style="text-align:center"><img src="data:image/svg+xml;base64,{b64}" style="max-width:100%;height:auto"/></div>',
        unsafe_allow_html=True,
    )
else:
    st.info("assets/orchestrator_architecture.svg")

st.divider()

st.markdown(f"### {T['task_h'][lang]}")
st.write(T["task"][lang])
st.markdown(f"### {T['sol_h'][lang]}")
st.write(T["sol"][lang])

st.divider()

st.markdown(f"### {T['scale'][lang]}")
c1, c2, c3, c4 = st.columns(4)
c1.metric(T["m_tasks"][lang], "~50")
c2.metric(T["m_plat"][lang], "4")
c3.metric(T["m_mon"][lang], "9")
c4.metric(T["m_up"][lang], "24/7")
st.caption("Amazon (SP-API + Advertising), Walmart, Shopify, Weather → PostgreSQL")

st.divider()

st.markdown(f"### {T['rel_h'][lang]}")
m1, m2 = st.columns(2)
with m1:
    st.markdown(f"**{T['r1t'][lang]}**"); st.write(T["r1d"][lang])
    st.markdown(f"**{T['r2t'][lang]}**"); st.write(T["r2d"][lang])
with m2:
    st.markdown(f"**{T['r3t'][lang]}**"); st.write(T["r3d"][lang])
    st.markdown(f"**{T['r4t'][lang]}**"); st.write(T["r4d"][lang])

st.divider()

st.markdown(f"### {T['load_h'][lang]}")
st.caption(T["load_cap"][lang])
schedule = pd.DataFrame([
    ("00:45","Promotions","Amazon"),("02:00","Ads","Amazon"),("04:15","Orders","Shopify"),
    ("04:25","P&L daily","Shopify"),("05:00","Orders (batch)","Amazon"),("06:00","Weather","Weather"),
    ("07:00","Returns","Walmart"),("08:10","Inventory (AWD)","Amazon"),("09:00","Inventory","Amazon"),
    ("10:05","Alerts","Amazon"),("12:00","Review request","Amazon"),("16:20","Transactions","Amazon"),
    ("17:15","Orders","Walmart"),("23:30","Orders (full)","Amazon"),
], columns=[T["col_time"][lang], T["col_task"][lang], T["col_plat"][lang]])
st.dataframe(schedule, use_container_width=True, hide_index=True)

st.markdown(f"**{T['dist'][lang]}**")
st.bar_chart(schedule[T["col_plat"][lang]].value_counts())

st.divider()

with st.expander(T["under_h"][lang]):
    st.write(T["under"][lang])
    st.code(
        "while True:\n"
        "    for task in due_tasks(now):\n"
        "        if not is_running(task):\n"
        "            executor.submit(run_task, task)\n"
        "    sleep(10)",
        language="python",
    )

st.info(T["nda"][lang], icon="🔒")
