import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="External Data", page_icon="🌦️", layout="wide")

st.title("🌦️ Кейс: обогащение данных внешними источниками")
st.caption("Зачем e-commerce погода и гео-аналитика. Демо-данные (синтетика).")

st.markdown("### Идея")
st.write(
    "Продажи многих товаров зависят от погоды и географии. Если подмешать "
    "к продажам погодные данные и население штатов, видно закономерности, "
    "которые иначе теряются: где спрос растёт из-за погоды, где рынок "
    "недопроникнут, где возможны задержки доставки."
)

st.divider()

# ---------- Демо-данные по штатам ----------
@st.cache_data
def make_states():
    rng = np.random.default_rng(7)
    states = {
        "CA":("California",6.0),"TX":("Texas",4.5),"NY":("New York",3.8),
        "FL":("Florida",3.5),"WA":("Washington",2.4),"IL":("Illinois",2.6),
        "AZ":("Arizona",1.7),"NC":("North Carolina",1.6),"VA":("Virginia",1.5),
        "NJ":("New Jersey",1.4),"MO":("Missouri",1.1),"CO":("Colorado",1.0),
        "GA":("Georgia",1.6),"OH":("Ohio",1.7),"PA":("Pennsylvania",2.0),
        "MI":("Michigan",1.4),"OR":("Oregon",0.9),"MS":("Mississippi",0.6),
        "AK":("Alaska",0.3),"NH":("New Hampshire",0.3),
    }
    rows = []
    for code,(name,pop_share) in states.items():
        temp = round(rng.uniform(18, 42), 1)
        # сила бренда в штате (0.3..2.2) создаёт реалистичный разброс penetration
        strength = rng.uniform(0.3, 2.2)
        units = max(50, int(pop_share * 200 * strength + rng.normal(0, 30)))
        rows.append({"code":code,"state":name,"temp":temp,"units":units,
                     "pop_share":pop_share})
    df = pd.DataFrame(rows)
    # обе доли в одинаковых единицах (проценты) → penetration около 1
    df["sales_share"] = df["units"] / df["units"].sum() * 100
    df["pop_share_pct"] = df["pop_share"] / df["pop_share"].sum() * 100
    df["penetration"] = (df["sales_share"] / df["pop_share_pct"]).round(2)
    return df

df = make_states()

# ---------- Карта температуры ----------
st.markdown("### 🌡️ Температура сегодня (°C)")
st.caption("Синее — холодно, красное — жарко. Наведи на штат для деталей.")
fig_temp = px.choropleth(
    df, locations="code", locationmode="USA-states", color="temp",
    scope="usa", color_continuous_scale="RdYlBu_r",
    hover_name="state", labels={"temp":"°C"},
)
fig_temp.update_layout(margin=dict(l=0,r=0,t=0,b=0), height=380)
st.plotly_chart(fig_temp, use_container_width=True)

st.divider()

# ---------- Карта Penetration Index ----------
st.markdown("### 🎯 Penetration Index — где недопроникновение")
st.write(
    "**Зачем это:** карта продаж всегда подсвечивает крупные штаты — там просто "
    "больше людей. Penetration Index убирает этот эффект: показывает, где ты "
    "продаёшь **сильнее или слабее, чем размер рынка**."
)
st.caption(
    "Индекс = (доля продаж в штате) / (доля населения штата). "
    "Индекс 2.0 = вдвое сильнее рынка, < 1 = недопроникновение."
)
fig_pen = px.choropleth(
    df, locations="code", locationmode="USA-states", color="penetration",
    scope="usa", color_continuous_scale="RdBu",
    range_color=[0, 2], hover_name="state", labels={"penetration":"Index"},
)
fig_pen.update_layout(margin=dict(l=0,r=0,t=0,b=0), height=380)
st.plotly_chart(fig_pen, use_container_width=True)

# топ недопроникновения
st.markdown("**Где недопроникновение (индекс < 1) — потенциал роста:**")
under = df[df["penetration"] < 1].sort_values("penetration")[["state","penetration","units"]]
under.columns = ["Штат","Penetration","Units 30д"]
st.dataframe(under, use_container_width=True, hide_index=True)

st.divider()

# ---------- Корреляция спрос/температура ----------
st.markdown("### 📈 Спрос против температуры (демо)")
@st.cache_data
def make_corr():
    rng = np.random.default_rng(7)
    days = pd.date_range("2025-01-01", periods=90, freq="D")
    temp = 5 + 15 * np.sin(np.arange(90)/30) + rng.normal(0,2,90)
    demand = np.clip(120 - 4*temp + rng.normal(0,8,90), 0, None)
    return pd.DataFrame({"Дата":days,"Температура":temp.round(1),"Спрос":demand.round(0)})

c = make_corr()
col1,col2 = st.columns(2)
with col1:
    st.markdown("**Температура**")
    st.line_chart(c.set_index("Дата")["Температура"])
with col2:
    st.markdown("**Спрос на тёплую одежду**")
    st.line_chart(c.set_index("Дата")["Спрос"])
st.metric("Корреляция (демо)", f"{c['Температура'].corr(c['Спрос']):.2f}")
st.caption("Отрицательная: холодает → спрос растёт.")

st.divider()

st.markdown("### Ценность для бизнеса")
st.write(
    "Погода и гео-данные — дешёвые внешние сигналы. Видно где спрос вырастет "
    "из-за похолодания, где рынок недопроникнут (куда лить рекламу), "
    "и где возможны задержки доставки. Решения на данных, а не на ощущениях."
)

with st.expander("⚙️ Под капотом (для технической аудитории)"):
    st.write(
        "Open-Meteo + NWS для погоды, Census API для населения штатов, "
        "choropleth-карты (Plotly), расчёт Penetration Index, "
        "склейка с продажами в PostgreSQL."
    )

st.info("Реальные регионы, объёмы и модели — под NDA.", icon="🔒")
