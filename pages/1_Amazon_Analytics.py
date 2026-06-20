import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from db import fetch_table, db_badge

st.set_page_config(page_title="Amazon Analytics", page_icon="🛒", layout="wide")

st.title("🛒 Кейс: Amazon-аналитика под ключ")
st.caption("Демо-данные. Реальная система работает на SP-API + PostgreSQL.")

st.markdown("### Задача")
st.write(
    "Продавец выходит на Amazon и тонет в ручных выгрузках: продажи, "
    "Buy Box, возвраты, маржа считаются в Excel по ночам. "
    "Нужна одна панель, которая обновляется сама."
)
st.markdown("### Что построено")
st.write(
    "- ETL-пайплайн по SP-API (заказы, цены, инвентарь, возвраты)\n"
    "- Хранилище на PostgreSQL, планировщик-загрузчики 24/7\n"
    "- Telegram-бот: алерт при потере Buy Box\n"
    "- Дашборд (ниже) для ежедневных решений"
)

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

skus = st.multiselect("SKU", sorted(raw.sku.unique()), default=sorted(raw.sku.unique()))
fdf = raw[raw.sku.isin(skus)]

k1, k2, k3, k4 = st.columns(4)
k1.metric("Выручка", f"${fdf.revenue.sum():,.0f}")
k2.metric("Юнитов продано", f"{int(fdf.units.sum()):,}")
k3.metric("Средний Buy Box", f"{fdf.buybox_pct.mean()*100:.0f}%")
k4.metric("Активных SKU", fdf.sku.nunique())

st.divider()

c1, c2 = st.columns(2)
with c1:
    st.markdown("**Выручка по дням**")
    st.line_chart(fdf.groupby("date").revenue.sum())
with c2:
    st.markdown("**Buy Box % по SKU**")
    st.bar_chart(fdf.groupby("sku").buybox_pct.mean() * 100)

st.markdown("**Срез по SKU**")
agg = fdf.groupby("sku").agg(
    units=("units", "sum"), revenue=("revenue", "sum"), buybox=("buybox_pct", "mean"),
).round(2)
st.dataframe(agg, use_container_width=True)

with st.expander("⚙️ Под капотом (для технической аудитории)"):
    st.code(
        "# Дашборд читает из PostgreSQL\n"
        "SELECT sku, date, units, revenue, buybox_pct\n"
        "FROM amazon_sales ORDER BY date;\n\n"
        "# Реальная система: ~20 SP-API загрузчиков,\n"
        "# идемпотентный upsert, алерты в Telegram",
        language="sql",
    )

st.info("Все цифры синтетические. Реальные проекты — под NDA.", icon="🔒")
