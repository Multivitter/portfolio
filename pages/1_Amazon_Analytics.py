import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from db import fetch_table, db_badge
from i18n import lang_selector, get_lang

st.set_page_config(page_title="Amazon Analytics", page_icon="🛒", layout="wide")
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
    "title": {"EN": "🛒 Case: turnkey Amazon analytics", "RU": "🛒 Кейс: Amazon-аналитика под ключ", "UK": "🛒 Кейс: Amazon-аналітика під ключ"},
    "cap": {"EN": "Demo data. Real system runs on SP-API + PostgreSQL.", "RU": "Демо-данные. Реальная система работает на SP-API + PostgreSQL.", "UK": "Демо-дані. Реальна система працює на SP-API + PostgreSQL."},
    "task_h": {"EN": "Task", "RU": "Задача", "UK": "Задача"},
    "task": {
        "EN": "A seller launches on Amazon and drowns in manual exports: sales, Buy Box, returns, margin counted in Excel overnight. They need one panel that updates itself.",
        "RU": "Продавец выходит на Amazon и тонет в ручных выгрузках: продажи, Buy Box, возвраты, маржа считаются в Excel по ночам. Нужна одна панель, которая обновляется сама.",
        "UK": "Продавець виходить на Amazon і тоне в ручних вивантаженнях: продажі, Buy Box, повернення, маржа рахуються в Excel ночами. Потрібна одна панель, що оновлюється сама.",
    },
    "built_h": {"EN": "What's built", "RU": "Что построено", "UK": "Що побудовано"},
    "built": {
        "EN": "- SP-API ETL pipeline (orders, prices, inventory, returns)\n- PostgreSQL storage, 24/7 scheduler-loaders\n- Telegram bot: alert on Buy Box loss\n- Dashboard (below) for daily decisions",
        "RU": "- ETL-пайплайн по SP-API (заказы, цены, инвентарь, возвраты)\n- Хранилище на PostgreSQL, планировщик-загрузчики 24/7\n- Telegram-бот: алерт при потере Buy Box\n- Дашборд (ниже) для ежедневных решений",
        "UK": "- ETL-пайплайн по SP-API (замовлення, ціни, інвентар, повернення)\n- Сховище на PostgreSQL, планувальник-завантажувачі 24/7\n- Telegram-бот: алерт при втраті Buy Box\n- Дашборд (нижче) для щоденних рішень",
    },
    "sku": {"EN": "SKU", "RU": "SKU", "UK": "SKU"},
    "m_rev": {"EN": "Revenue", "RU": "Выручка", "UK": "Виручка"},
    "m_units": {"EN": "Units sold", "RU": "Юнитов продано", "UK": "Юнітів продано"},
    "m_bb": {"EN": "Avg Buy Box", "RU": "Средний Buy Box", "UK": "Середній Buy Box"},
    "m_sku": {"EN": "Active SKUs", "RU": "Активных SKU", "UK": "Активних SKU"},
    "rev_day": {"EN": "Revenue by day", "RU": "Выручка по дням", "UK": "Виручка по днях"},
    "bb_sku": {"EN": "Buy Box % by SKU", "RU": "Buy Box % по SKU", "UK": "Buy Box % по SKU"},
    "by_sku": {"EN": "Breakdown by SKU", "RU": "Срез по SKU", "UK": "Зріз по SKU"},
    "scope_h": {"EN": "System scale — what the platform covers", "RU": "Масштаб системы — что покрывает платформа", "UK": "Масштаб системи — що покриває платформа"},
    "scope_intro": {
        "EN": "Not a single dashboard but a BI platform: 25+ report sections in one place, all fed by the ETL pipeline. A few of the directions:",
        "RU": "Не один дашборд, а BI-платформа: 25+ разделов отчётов в одном месте, все питаются от ETL-пайплайна. Часть направлений:",
        "UK": "Не один дашборд, а BI-платформа: 25+ розділів звітів в одному місці, усі живляться від ETL-пайплайна. Частина напрямків:",
    },
    "scope_cap": {"EN": "Module list only — figures and internals under NDA.", "RU": "Только список модулей — цифры и внутренности под NDA.", "UK": "Лише список модулів — цифри та нутрощі під NDA."},
    "under_h": {"EN": "⚙️ Under the hood (for technical audience)", "RU": "⚙️ Под капотом (для технической аудитории)", "UK": "⚙️ Під капотом (для технічної аудиторії)"},
    "nda": {"EN": "All figures synthetic. Real projects under NDA.", "RU": "Все цифры синтетические. Реальные проекты — под NDA.", "UK": "Усі цифри синтетичні. Реальні проєкти — під NDA."},
}

st.title(T["title"][lang])
st.caption(T["cap"][lang])

st.markdown(f"### {T['task_h'][lang]}")
st.write(T["task"][lang])
st.markdown(f"### {T['built_h'][lang]}")
st.write(T["built"][lang])

st.divider()

# ---------- Масштаб системы: карта модулей ----------
st.markdown(f"### {T['scope_h'][lang]}")
st.write(T["scope_intro"][lang])

modules = [
    "📈 Sales & Traffic", "💰 Finance", "💸 Reimbursement", "🛒 Orders",
    "📦 Inventory", "↩️ Returns", "📝 Listings", "🔎 Keepa", "💲 Price / BuyBox",
    "🎯 BuyBox Monitor", "📦 FBA Operations", "🌦️ Weather", "💵 Margin",
    "🧾 Taxes", "⭐ Reviews", "📣 Customer Feedback", "📊 Brand Analytics",
    "📦 Restock Agent", "📈 Forecast", "🩺 ETL Status",
]
chips = "".join(
    f"<span style='display:inline-block;background:#1A1D24;color:#cbd5e1;"
    f"padding:6px 12px;border-radius:8px;margin:4px 6px 4px 0;font-size:0.85rem;"
    f"border:1px solid #2a2f3a'>{m}</span>"
    for m in modules
)
st.markdown(f"<div>{chips}</div>", unsafe_allow_html=True)
st.caption(T["scope_cap"][lang])

st.divider()

@st.cache_data
def synthetic():
    rng = np.random.default_rng(42)
    days = pd.date_range("2025-01-01", periods=120, freq="D")
    skus = ["WOOL-SOCK-01", "BASE-TEE-02", "HOOD-ZIP-03", "THERM-LEG-04"]
    rows = []
    for sku in skus:
        base = rng.integers(20, 80)
        for d in days:
            units = max(0, int(base + rng.normal(0, 8) + 15 * np.sin(d.dayofyear / 14)))
            price = round(rng.uniform(15, 60), 2)
            rows.append({"sku": sku, "date": d, "units": units,
                         "revenue": units * price, "buybox_pct": rng.uniform(0.55, 0.98)})
    return pd.DataFrame(rows)

raw = fetch_table("amazon_sales", "sku, date, units, revenue, buybox_pct", order_by="date")
is_live = raw is not None and not raw.empty
if not is_live:
    raw = synthetic()

db_badge(is_live)
raw["date"] = pd.to_datetime(raw["date"])

skus = st.multiselect(T["sku"][lang], sorted(raw.sku.unique()), default=sorted(raw.sku.unique()))
fdf = raw[raw.sku.isin(skus)]

k1, k2, k3, k4 = st.columns(4)
k1.metric(T["m_rev"][lang], f"${fdf.revenue.sum():,.0f}")
k2.metric(T["m_units"][lang], f"{int(fdf.units.sum()):,}")
k3.metric(T["m_bb"][lang], f"{fdf.buybox_pct.mean()*100:.0f}%")
k4.metric(T["m_sku"][lang], fdf.sku.nunique())

st.divider()

c1, c2 = st.columns(2)
with c1:
    st.markdown(f"**{T['rev_day'][lang]}**")
    st.line_chart(fdf.groupby("date").revenue.sum())
with c2:
    st.markdown(f"**{T['bb_sku'][lang]}**")
    st.bar_chart(fdf.groupby("sku").buybox_pct.mean() * 100)

st.markdown(f"**{T['by_sku'][lang]}**")
agg = fdf.groupby("sku").agg(
    units=("units", "sum"), revenue=("revenue", "sum"), buybox=("buybox_pct", "mean"),
).round(2)
st.dataframe(agg, use_container_width=True)

with st.expander(T["under_h"][lang]):
    st.code(
        "SELECT sku, date, units, revenue, buybox_pct\n"
        "FROM amazon_sales ORDER BY date;\n\n"
        "# ~20 SP-API loaders, idempotent upsert, Telegram alerts",
        language="sql",
    )

st.info(T["nda"][lang], icon="🔒")
