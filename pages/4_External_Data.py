import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from i18n import lang_selector, get_lang

st.set_page_config(page_title="External Data", page_icon="🌦️", layout="wide")
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
    "title": {"EN": "🌦️ Case: enriching data with external sources", "RU": "🌦️ Кейс: обогащение данных внешними источниками", "UK": "🌦️ Кейс: збагачення даних зовнішніми джерелами"},
    "cap": {"EN": "Why e-commerce needs weather and geo-analytics. Demo data (synthetic).", "RU": "Зачем e-commerce погода и гео-аналитика. Демо-данные (синтетика).", "UK": "Навіщо e-commerce погода та гео-аналітика. Демо-дані (синтетика)."},
    "idea_h": {"EN": "Idea", "RU": "Идея", "UK": "Ідея"},
    "idea": {
        "EN": "Sales of many products depend on weather and geography. Adding weather data and state population to sales reveals patterns otherwise lost: where demand grows due to weather, where the market is under-penetrated, where delivery delays are likely.",
        "RU": "Продажи многих товаров зависят от погоды и географии. Если подмешать к продажам погодные данные и население штатов, видно закономерности, которые иначе теряются: где спрос растёт из-за погоды, где рынок недопроникнут, где возможны задержки доставки.",
        "UK": "Продажі багатьох товарів залежать від погоди та географії. Якщо підмішати до продажів погодні дані та населення штатів, видно закономірності, що інакше губляться: де попит зростає через погоду, де ринок недопроникнутий, де можливі затримки доставки.",
    },
    "temp_h": {"EN": "🌡️ Temperature today (°C)", "RU": "🌡️ Температура сегодня (°C)", "UK": "🌡️ Температура сьогодні (°C)"},
    "temp_cap": {"EN": "Blue — cold, red — hot. Hover a state for details.", "RU": "Синее — холодно, красное — жарко. Наведи на штат для деталей.", "UK": "Синє — холодно, червоне — спекотно. Наведи на штат для деталей."},
    "pen_h": {"EN": "🎯 Penetration Index — where under-penetration is", "RU": "🎯 Penetration Index — где недопроникновение", "UK": "🎯 Penetration Index — де недопроникнення"},
    "pen_txt": {
        "EN": "**Why this:** a sales map always highlights big states — they simply have more people. Penetration Index removes that effect: it shows where you sell **stronger or weaker than the market size**.",
        "RU": "**Зачем это:** карта продаж всегда подсвечивает крупные штаты — там просто больше людей. Penetration Index убирает этот эффект: показывает, где ты продаёшь **сильнее или слабее, чем размер рынка**.",
        "UK": "**Навіщо це:** карта продажів завжди підсвічує великі штати — там просто більше людей. Penetration Index прибирає цей ефект: показує, де ти продаєш **сильніше або слабше, ніж розмір ринку**.",
    },
    "pen_cap": {"EN": "Index = (state sales share) / (state population share). 2.0 = twice the market, < 1 = under-penetration.", "RU": "Индекс = (доля продаж в штате) / (доля населения штата). Индекс 2.0 = вдвое сильнее рынка, < 1 = недопроникновение.", "UK": "Індекс = (частка продажів у штаті) / (частка населення штату). Індекс 2.0 = вдвічі сильніше ринку, < 1 = недопроникнення."},
    "under_t": {"EN": "Where under-penetration (index < 1) — growth potential:", "RU": "Где недопроникновение (индекс < 1) — потенциал роста:", "UK": "Де недопроникнення (індекс < 1) — потенціал зростання:"},
    "col_state": {"EN": "State", "RU": "Штат", "UK": "Штат"},
    "col_units": {"EN": "Units 30d", "RU": "Units 30д", "UK": "Units 30д"},
    "corr_h": {"EN": "📈 Demand vs temperature (demo)", "RU": "📈 Спрос против температуры (демо)", "UK": "📈 Попит проти температури (демо)"},
    "temp_lbl": {"EN": "Temperature", "RU": "Температура", "UK": "Температура"},
    "demand_lbl": {"EN": "Demand for warm clothing", "RU": "Спрос на тёплую одежду", "UK": "Попит на теплий одяг"},
    "corr_m": {"EN": "Correlation (demo)", "RU": "Корреляция (демо)", "UK": "Кореляція (демо)"},
    "corr_cap": {"EN": "Negative: colder → demand grows.", "RU": "Отрицательная: холодает → спрос растёт.", "UK": "Від'ємна: холоднішає → попит зростає."},
    "val_h": {"EN": "Business value", "RU": "Ценность для бизнеса", "UK": "Цінність для бізнесу"},
    "val": {
        "EN": "Weather and geo data are cheap external signals. You see where demand will rise due to a cold snap, where the market is under-penetrated (where to push ads), and where delivery delays are likely. Decisions on data, not gut feel.",
        "RU": "Погода и гео-данные — дешёвые внешние сигналы. Видно где спрос вырастет из-за похолодания, где рынок недопроникнут (куда лить рекламу), и где возможны задержки доставки. Решения на данных, а не на ощущениях.",
        "UK": "Погода та гео-дані — дешеві зовнішні сигнали. Видно де попит зросте через похолодання, де ринок недопроникнутий (куди лити рекламу), і де можливі затримки доставки. Рішення на даних, а не на відчуттях.",
    },
    "under_h": {"EN": "⚙️ Under the hood (for technical audience)", "RU": "⚙️ Под капотом (для технической аудитории)", "UK": "⚙️ Під капотом (для технічної аудиторії)"},
    "under": {"EN": "Open-Meteo + NWS for weather, Census API for state population, choropleth maps (Plotly), Penetration Index calc, join with sales in PostgreSQL.", "RU": "Open-Meteo + NWS для погоды, Census API для населения штатов, choropleth-карты (Plotly), расчёт Penetration Index, склейка с продажами в PostgreSQL.", "UK": "Open-Meteo + NWS для погоди, Census API для населення штатів, choropleth-карти (Plotly), розрахунок Penetration Index, склейка з продажами в PostgreSQL."},
    "nda": {"EN": "Real regions, volumes and models — under NDA.", "RU": "Реальные регионы, объёмы и модели — под NDA.", "UK": "Реальні регіони, обсяги та моделі — під NDA."},
}

st.title(T["title"][lang])
st.caption(T["cap"][lang])

st.markdown(f"### {T['idea_h'][lang]}")
st.write(T["idea"][lang])

st.divider()

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
        strength = rng.uniform(0.3, 2.2)
        units = max(50, int(pop_share * 200 * strength + rng.normal(0, 30)))
        rows.append({"code":code,"state":name,"temp":temp,"units":units,"pop_share":pop_share})
    df = pd.DataFrame(rows)
    df["sales_share"] = df["units"] / df["units"].sum() * 100
    df["pop_share_pct"] = df["pop_share"] / df["pop_share"].sum() * 100
    df["penetration"] = (df["sales_share"] / df["pop_share_pct"]).round(2)
    return df

df = make_states()

st.markdown(f"### {T['temp_h'][lang]}")
st.caption(T["temp_cap"][lang])
fig_temp = px.choropleth(df, locations="code", locationmode="USA-states", color="temp",
    scope="usa", color_continuous_scale="RdYlBu_r", hover_name="state", labels={"temp":"°C"})
fig_temp.update_layout(margin=dict(l=0,r=0,t=0,b=0), height=380)
st.plotly_chart(fig_temp, use_container_width=True)

st.divider()

st.markdown(f"### {T['pen_h'][lang]}")
st.write(T["pen_txt"][lang])
st.caption(T["pen_cap"][lang])
fig_pen = px.choropleth(df, locations="code", locationmode="USA-states", color="penetration",
    scope="usa", color_continuous_scale="RdBu", range_color=[0, 2], hover_name="state", labels={"penetration":"Index"})
fig_pen.update_layout(margin=dict(l=0,r=0,t=0,b=0), height=380)
st.plotly_chart(fig_pen, use_container_width=True)

st.markdown(f"**{T['under_t'][lang]}**")
under = df[df["penetration"] < 1].sort_values("penetration")[["state","penetration","units"]]
under.columns = [T["col_state"][lang], "Penetration", T["col_units"][lang]]
st.dataframe(under, use_container_width=True, hide_index=True)

st.divider()

st.markdown(f"### {T['corr_h'][lang]}")
@st.cache_data
def make_corr():
    rng = np.random.default_rng(7)
    days = pd.date_range("2025-01-01", periods=90, freq="D")
    temp = 5 + 15 * np.sin(np.arange(90)/30) + rng.normal(0,2,90)
    demand = np.clip(120 - 4*temp + rng.normal(0,8,90), 0, None)
    return pd.DataFrame({"date":days,"temp":temp.round(1),"demand":demand.round(0)})

c = make_corr()
col1,col2 = st.columns(2)
with col1:
    st.markdown(f"**{T['temp_lbl'][lang]}**")
    st.line_chart(c.set_index("date")["temp"])
with col2:
    st.markdown(f"**{T['demand_lbl'][lang]}**")
    st.line_chart(c.set_index("date")["demand"])
st.metric(T["corr_m"][lang], f"{c['temp'].corr(c['demand']):.2f}")
st.caption(T["corr_cap"][lang])

st.divider()

st.markdown(f"### {T['val_h'][lang]}")
st.write(T["val"][lang])

with st.expander(T["under_h"][lang]):
    st.write(T["under"][lang])

st.info(T["nda"][lang], icon="🔒")
