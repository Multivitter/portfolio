import streamlit as st
import pandas as pd
import base64
from pathlib import Path

st.set_page_config(page_title="ETL Orchestrator", page_icon="🔄", layout="wide")

st.title("🔄 Кейс: ETL-оркестратор мультимаркетплейс")
st.caption("Один процесс держит всю аналитику e-commerce 24/7. Данные/названия обезличены.")


def render_svg(path: str):
    """Отрисовать SVG-файл в Streamlit через base64."""
    svg = Path(path).read_text(encoding="utf-8")
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    st.markdown(
        f'<div style="text-align:center">'
        f'<img src="data:image/svg+xml;base64,{b64}" style="max-width:100%;height:auto"/>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ---------- Схема архитектуры ----------
st.markdown("### Архитектура")
_svg = Path(__file__).parent.parent / "assets" / "orchestrator_architecture.svg"
if _svg.exists():
    render_svg(str(_svg))
else:
    st.info("Схема: assets/orchestrator_architecture.svg")

st.divider()

# ---------- Задача ----------
st.markdown("### Задача")
st.write(
    "Продавец работает сразу на нескольких площадках (Amazon, Walmart, Shopify). "
    "Данные разрозненные, выгрузки ручные, никто не замечает сбой загрузки, "
    "пока цифры в отчёте не «поедут». Нужна единая система, которая сама "
    "тянет данные по расписанию, складывает в одно хранилище, следит за собой "
    "и сообщает о проблемах."
)

st.markdown("### Решение")
st.write(
    "Единый процесс-оркестратор: расписание из ~50 задач, пул воркеров, "
    "фоновые мониторы за таблицами, авто-перезапуск при сбоях, "
    "защита от двойного запуска и сводки в Telegram."
)

st.divider()

# ---------- Метрики ----------
st.markdown("### Масштаб системы")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Задач по графику", "~50")
c2.metric("Площадок", "4")
c3.metric("Фоновых мониторов", "9")
c4.metric("Аптайм", "24/7")

st.caption(
    "Площадки: Amazon (SP-API + Advertising), Walmart, Shopify, Weather. "
    "Хранилище — PostgreSQL."
)

st.divider()

# ---------- Ключевые механизмы ----------
st.markdown("### Что делает систему надёжной")
m1, m2 = st.columns(2)
with m1:
    st.markdown("**🔁 Auto-retry**")
    st.write("До 3 повторов с нарастающей паузой. После — критический алерт и стоп, чтобы не долбить API.")
    st.markdown("**🔒 Защита от двойного запуска**")
    st.write("Уникальный ключ задачи на время выполнения — одна и та же задача не стартует дважды.")
with m2:
    st.markdown("**👀 Фоновые мониторы**")
    st.write("Следят за таблицами: изменилась дата или счётчик строк → разбор события в Telegram.")
    st.markdown("**📊 Ежедневная сводка**")
    st.write("Раз в сутки — overview по всем загрузчикам: сколько запусков, строк, ошибок, по группам.")

st.divider()

# ---------- Таймлайн расписания (обезличенный, репрезентативный) ----------
st.markdown("### Как распределена нагрузка по суткам")
st.caption("Условный срез расписания (категории задач, без деталей реализации).")

schedule = pd.DataFrame([
    ("00:45", "Promotions", "Amazon"),
    ("02:00", "Ads", "Amazon"),
    ("04:15", "Orders", "Shopify"),
    ("04:25", "P&L daily", "Shopify"),
    ("05:00", "Orders (batch)", "Amazon"),
    ("06:00", "Weather", "Weather"),
    ("07:00", "Returns", "Walmart"),
    ("08:10", "Inventory (AWD)", "Amazon"),
    ("09:00", "Inventory", "Amazon"),
    ("10:05", "Alerts", "Amazon"),
    ("12:00", "Review request", "Amazon"),
    ("16:20", "Transactions", "Amazon"),
    ("17:15", "Orders", "Walmart"),
    ("23:30", "Orders (full)", "Amazon"),
], columns=["Время (Киев)", "Задача", "Площадка"])

st.dataframe(schedule, use_container_width=True, hide_index=True)

counts = schedule["Площадка"].value_counts()
st.markdown("**Распределение по площадкам (в этом срезе)**")
st.bar_chart(counts)

st.divider()

# ---------- Под капотом ----------
with st.expander("⚙️ Под капотом (для технической аудитории)"):
    st.write(
        "Python, потоки + ThreadPoolExecutor, отдельные таймауты на каждый тип "
        "задачи, ETL-лог в PostgreSQL (etl_log), парсинг stdout воркеров для "
        "извлечения метрик в алерты, мониторы на отдельных daemon-потоках."
    )
    st.code(
        "# Логика главного цикла (упрощённо)\n"
        "while True:\n"
        "    for task in due_tasks(now):\n"
        "        if not is_running(task):       # анти-дабл\n"
        "            executor.submit(run_task, task)\n"
        "    sleep(10)\n\n"
        "# run_task: таймаут по типу, retry x3, write_etl_log(), telegram",
        language="python",
    )

st.info("Реальные названия брендов, схемы БД и токены — под NDA.", icon="🔒")
