import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Amazon Analytics", page_icon="🛒", layout="wide")

st.title("🛒 Кейс: Amazon-аналитика под ключ")
st.caption("Демо-данные. Реальная система работает на SP-API + PostgreSQL.")

# ---------- Контекст кейса ----------
with st.container():
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

# ---------- Генерация демо-данных ----------
@st.cache_data
def make_data():
    rng = np.random.default_rng(42)
    days = pd.date_range("2026-01-01", periods=120, freq="D")
    skus = ["WOOL-SOCK-01", "WOOL-TEE-02", "BELT-PRO-03", "PART-TORO-04"]
    rows = []
    for sku in skus:
        base = rng.integers(20, 80)
        for d in days:
            units = max(0, int(base + rng.normal(0, 8) + 15 * np.sin(d.dayofyear / 14)))
            price = round(rng.uniform(15, 60), 2)
            rows.append([d, sku, units, units * price,
                         rng.uniform(0.55, 0.98)])
    df = pd.DataFrame(rows, columns=["date", "sku", "units", "revenue", "buybox"])
    return df

df = make_data()

# ---------- Фильтры ----------
skus = st.multiselect("SKU", df.sku.unique().tolist(),
                      default=df.sku.unique().tolist())
fdf = df[df.sku.isin(skus)]

# ---------- KPI ----------
k1, k2, k3, k4 = st.columns(4)
k1.metric("Выручка (демо)", f"${fdf.revenue.sum():,.0f}")
k2.metric("Юнитов продано", f"{fdf.units.sum():,}")
k3.metric("Средний Buy Box", f"{fdf.buybox.mean()*100:.0f}%")
k4.metric("Активных SKU", fdf.sku.nunique())

st.divider()

# ---------- Графики ----------
c1, c2 = st.columns(2)
with c1:
    st.markdown("**Выручка по дням**")
    daily = fdf.groupby("date").revenue.sum()
    st.line_chart(daily)
with c2:
    st.markdown("**Buy Box % по SKU**")
    bb = fdf.groupby("sku").buybox.mean() * 100
    st.bar_chart(bb)

st.markdown("**Срез по SKU**")
agg = fdf.groupby("sku").agg(
    units=("units", "sum"),
    revenue=("revenue", "sum"),
    buybox=("buybox", "mean"),
).round(2)
st.dataframe(agg, use_container_width=True)

# ---------- Под капотом (для технарей) ----------
with st.expander("⚙️ Под капотом (для технической аудитории)"):
    st.code(
        "# Псевдокод загрузчика SP-API\n"
        "for report in sp_api.get_reports(['ORDERS','PRICING','RETURNS']):\n"
        "    df = transform(report)\n"
        "    upsert_postgres(df, schema='amazon')\n"
        "scheduler.every('15min').do(check_buybox_and_alert)",
        language="python",
    )
    st.write(
        "Реальная система: ~20 загрузчиков, идемпотентный upsert, "
        "structured logging, алерты в Telegram."
    )
