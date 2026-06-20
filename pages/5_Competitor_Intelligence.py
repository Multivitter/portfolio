import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Competitor Intelligence", page_icon="🎯", layout="wide")

st.title("🎯 Кейс: конкурентная разведка (BSR-трекинг)")
st.caption("Слежу за позициями конкурентов по дням. Данные обезличены/синтетические.")

# ---------- Задача ----------
st.markdown("### Задача")
st.write(
    "В нише десятки конкурентов, у каждого — несколько товаров. "
    "Позиции в рейтинге (BSR — Best Sellers Rank) меняются ежедневно. "
    "Вручную это не отследить. Нужна система, которая каждый день снимает "
    "BSR конкурентов и показывает, кто растёт, кто падает — по каждому SKU."
)

st.markdown("### Решение")
st.write(
    "Ежедневный парсинг BSR конкурентов в одну таблицу. Подсветка движения "
    "цветом: зелёный — позиция улучшилась (BSR упал, товар продаётся лучше), "
    "красный — ухудшилась. Разрез по категориям товаров."
)

st.divider()

# ---------- Генерация обезличенных данных ----------
@st.cache_data
def make_data():
    rng = np.random.default_rng(11)
    categories = {
        "Базовый слой": ["Brand A — модель 1", "Brand A — модель 2",
                         "Brand B — модель 1", "Brand C — модель 1"],
        "Худи": ["Brand A — худи", "Brand B — худи", "Brand D — худи"],
        "Носки": ["Brand B — носки", "Brand C — носки", "Brand E — носки"],
    }
    dates = pd.date_range("2026-01-14", periods=8, freq="D")
    data = {}
    for cat, products in categories.items():
        rows = []
        for p in products:
            base = rng.integers(2000, 60000)
            series = []
            val = base
            for _ in dates:
                # случайное блуждание BSR
                val = max(500, int(val + rng.normal(0, val * 0.15)))
                series.append(val)
            rows.append([p] + series)
        cols = ["Товар"] + [d.strftime("%d.%m") for d in dates]
        data[cat] = pd.DataFrame(rows, columns=cols)
    return data

data = make_data()

# ---------- Выбор категории ----------
cat = st.selectbox("Категория товара", list(data.keys()))
df = data[cat].set_index("Товар")

st.markdown(f"### BSR по дням — {cat}")
st.caption("Чем меньше BSR, тем лучше продаётся. 🟢 позиция улучшилась · 🔴 ухудшилась (день к дню).")

# ---------- Подсветка динамики ----------
def highlight_trend(row):
    styles = [""] * len(row)
    vals = row.values
    for i in range(1, len(vals)):
        prev, cur = vals[i - 1], vals[i]
        if cur < prev:        # BSR упал = лучше
            styles[i] = "background-color: #c8f7c5"
        elif cur > prev:      # BSR вырос = хуже
            styles[i] = "background-color: #f7c5c5"
    return styles

styled = df.style.apply(highlight_trend, axis=1).format("{:,.0f}")
st.dataframe(styled, use_container_width=True)

st.divider()

# ---------- Сводка движения ----------
st.markdown("### Кто растёт, кто падает (за период)")
first_col, last_col = df.columns[0], df.columns[-1]
summary = pd.DataFrame({
    "Старт BSR": df[first_col],
    "Конец BSR": df[last_col],
})
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

# ---------- Ценность ----------
st.markdown("### Ценность для бизнеса")
st.write(
    "Видно в реальном времени, кто из конкурентов разгоняется (повод проверить "
    "их акции/рекламу) и кто проседает (повод забрать долю). Решения по цене и "
    "рекламе принимаются на данных, а не на ощущениях."
)

with st.expander("⚙️ Под капотом (для технической аудитории)"):
    st.write(
        "Ежедневный сбор BSR по списку ASIN конкурентов через сервис парсинга, "
        "запись в таблицу/БД с историей по дням, условное форматирование для "
        "быстрого визуального скана движения."
    )

st.info("Реальные бренды, ASIN и ниша — под NDA.", icon="🔒")
