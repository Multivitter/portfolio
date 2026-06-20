import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from db import fetch_table, db_badge

st.set_page_config(page_title="Competitor Intelligence", page_icon="🎯", layout="wide")

st.title("🎯 Кейс: конкурентная разведка (BSR-трекинг)")
st.caption("Слежу за позициями конкурентов по дням. Данные обезличены/синтетические.")

st.markdown("### Задача")
st.write(
    "В нише десятки конкурентов, у каждого — несколько товаров. "
    "Позиции в рейтинге (BSR — Best Sellers Rank) меняются ежедневно. "
    "Вручную это не отследить. Нужна система, которая каждый день снимает "
    "BSR конкурентов и показывает, кто растёт, кто падает — по каждому SKU."
)

st.markdown("### Решение")
st.write(
    "Ежедневный парсинг BSR конкурентов в одну таблицу (PostgreSQL). "
    "Подсветка движения цветом: зелёный — позиция улучшилась (BSR упал, "
    "товар продаётся лучше), красный — ухудшилась. Разрез по категориям."
)

st.divider()

@st.cache_data
def synthetic():
    rng = np.random.default_rng(11)
    categories = {
        "Base layer": ["Brand A — model 1", "Brand A — model 2",
                       "Brand B — model 1", "Brand C — model 1"],
        "Hoodie": ["Brand A — hoodie", "Brand B — hoodie", "Brand D — hoodie"],
        "Socks": ["Brand B — socks", "Brand C — socks", "Brand E — socks"],
    }
    dates = pd.date_range("2025-01-01", periods=8, freq="D")
    rows = []
    for cat, products in categories.items():
        for p in products:
            val = rng.integers(2000, 60000)
            for d in dates:
                val = max(500, int(val + rng.normal(0, val * 0.15)))
                rows.append({"product": p, "category": cat, "date": d, "bsr": val})
    return pd.DataFrame(rows)

raw = fetch_table("competitors_bsr", "product, category, date, bsr", order_by="date")
is_live = raw is not None and not raw.empty
if not is_live:
    raw = synthetic()

db_badge(is_live)
raw["date"] = pd.to_datetime(raw["date"])

cat = st.selectbox("Категория товара", sorted(raw["category"].unique()))
sub = raw[raw["category"] == cat].copy()
sub["d"] = sub["date"].dt.strftime("%d.%m")
df = sub.pivot_table(index="product", columns="d", values="bsr", aggfunc="first")

st.markdown(f"### BSR по дням — {cat}")
st.caption("Чем меньше BSR, тем лучше продаётся. 🟢 позиция улучшилась · 🔴 ухудшилась (день к дню).")

def highlight_trend(row):
    styles = [""] * len(row)
    vals = row.values
    for i in range(1, len(vals)):
        prev, cur = vals[i - 1], vals[i]
        if pd.isna(prev) or pd.isna(cur):
            continue
        if cur < prev:
            styles[i] = "background-color: #1d9e75; color: #ffffff"
        elif cur > prev:
            styles[i] = "background-color: #d85a30; color: #ffffff"
    return styles

styled = df.style.apply(highlight_trend, axis=1).format("{:,.0f}", na_rep="—")
st.dataframe(styled, use_container_width=True)

st.divider()

st.markdown("### Кто растёт, кто падает (за период)")
first_col, last_col = df.columns[0], df.columns[-1]
summary = pd.DataFrame({"Старт BSR": df[first_col], "Конец BSR": df[last_col]})
summary["Изменение"] = summary["Старт BSR"] - summary["Конец BSR"]
summary["Тренд"] = summary["Изменение"].apply(
    lambda x: "🟢 растёт" if x > 0 else ("🔴 падает" if x < 0 else "⚪ ровно")
)
summary = summary.sort_values("Изменение", ascending=False)
st.dataframe(
    summary.style.format({"Старт BSR": "{:,.0f}", "Конец BSR": "{:,.0f}", "Изменение": "{:+,.0f}"}),
    use_container_width=True,
)

st.divider()

st.markdown("### Ценность для бизнеса")
st.write(
    "Видно в реальном времени, кто из конкурентов разгоняется (повод проверить "
    "их акции/рекламу) и кто проседает (повод забрать долю). Решения по цене и "
    "рекламе принимаются на данных, а не на ощущениях."
)

with st.expander("⚙️ Под капотом (для технической аудитории)"):
    st.write(
        "Ежедневный сбор BSR по списку ASIN конкурентов через сервис парсинга, "
        "запись в PostgreSQL (таблица competitors_bsr) с историей по дням. "
        "Дашборд читает из базы через st.secrets, условное форматирование "
        "для быстрого визуального скана движения."
    )
    st.code(
        "SELECT product, category, date, bsr\n"
        "FROM competitors_bsr\n"
        "ORDER BY category, product, date;",
        language="sql",
    )

st.info("Реальные бренды, ASIN и ниша — под NDA.", icon="🔒")
