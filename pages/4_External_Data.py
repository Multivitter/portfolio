import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="External Data", page_icon="🌦️", layout="wide")

st.title("🌦️ Кейс: обогащение данных внешними источниками")
st.caption("Зачем e-commerce погода. Демо-данные.")

st.markdown("### Идея")
st.write(
    "Продажи многих товаров зависят от погоды: тёплая одежда, "
    "садовая техника, сезонные товары. Если подмешать погодные данные "
    "к продажам, видно закономерности, которые иначе теряются — "
    "и можно точнее планировать остатки и рекламу."
)

st.markdown("### Что собирается")
st.write(
    "- Прогноз и история погоды по ключевым регионам (Open-Meteo, NWS)\n"
    "- Погодные алерты\n"
    "- Всё складывается рядом с продажами в одном хранилище"
)

st.divider()

# ---------- Демо-корреляция ----------
st.markdown("### Пример: спрос против температуры (демо)")

@st.cache_data
def make():
    rng = np.random.default_rng(7)
    days = pd.date_range("2026-01-01", periods=90, freq="D")
    temp = 5 + 15 * np.sin(np.arange(90) / 30) + rng.normal(0, 2, 90)
    # тёплая одежда: спрос падает с ростом температуры
    demand = np.clip(120 - 4 * temp + rng.normal(0, 8, 90), 0, None)
    return pd.DataFrame({"Дата": days, "Температура °C": temp.round(1),
                         "Спрос (units)": demand.round(0)})

df = make()
c1, c2 = st.columns(2)
with c1:
    st.markdown("**Температура**")
    st.line_chart(df.set_index("Дата")["Температура °C"])
with c2:
    st.markdown("**Спрос на тёплую одежду**")
    st.line_chart(df.set_index("Дата")["Спрос (units)"])

corr = df["Температура °C"].corr(df["Спрос (units)"])
st.metric("Корреляция (демо)", f"{corr:.2f}")
st.caption("Отрицательная: холодает → спрос растёт. На реальных данных помогает планировать сезон.")

st.divider()

st.markdown("### Ценность для бизнеса")
st.write(
    "Погода — дешёвый внешний сигнал. Подмешав его к продажам, "
    "продавец заранее видит сезонные всплески и не уходит в OOS "
    "в пик спроса. Пример того, как обогащение данными даёт "
    "решения, недоступные на «голых» продажах."
)

st.info("Реальные регионы и модели — под NDA.", icon="🔒")
