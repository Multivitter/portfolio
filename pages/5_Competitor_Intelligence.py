import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from db import fetch_table, db_badge
from i18n import lang_selector, get_lang

st.set_page_config(page_title="Competitor Intelligence", page_icon="🎯", layout="wide")
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
    "title": {"EN": "🎯 Case: competitor intelligence (BSR tracking)", "RU": "🎯 Кейс: конкурентная разведка (BSR-трекинг)", "UK": "🎯 Кейс: конкурентна розвідка (BSR-трекінг)"},
    "cap": {"EN": "I track competitor positions daily. Data anonymized/synthetic.", "RU": "Слежу за позициями конкурентов по дням. Данные обезличены/синтетические.", "UK": "Стежу за позиціями конкурентів по днях. Дані знеособлені/синтетичні."},
    "task_h": {"EN": "Task", "RU": "Задача", "UK": "Задача"},
    "task": {
        "EN": "A niche has dozens of competitors, each with several products. Rank positions (BSR — Best Sellers Rank) change daily. You can't track that by hand. You need a system that captures competitor BSR every day and shows who rises, who falls — per SKU.",
        "RU": "В нише десятки конкурентов, у каждого — несколько товаров. Позиции в рейтинге (BSR — Best Sellers Rank) меняются ежедневно. Вручную это не отследить. Нужна система, которая каждый день снимает BSR конкурентов и показывает, кто растёт, кто падает — по каждому SKU.",
        "UK": "У ніші десятки конкурентів, у кожного — кілька товарів. Позиції в рейтингу (BSR — Best Sellers Rank) змінюються щодня. Вручну це не відстежити. Потрібна система, що щодня знімає BSR конкурентів і показує, хто зростає, хто падає — по кожному SKU.",
    },
    "sol_h": {"EN": "Solution", "RU": "Решение", "UK": "Рішення"},
    "sol": {
        "EN": "Daily BSR scraping of competitors into one table (PostgreSQL). Movement highlighted by color: green — position improved (BSR dropped, sells better), red — worsened. Split by product category.",
        "RU": "Ежедневный парсинг BSR конкурентов в одну таблицу (PostgreSQL). Подсветка движения цветом: зелёный — позиция улучшилась (BSR упал, товар продаётся лучше), красный — ухудшилась. Разрез по категориям.",
        "UK": "Щоденний парсинг BSR конкурентів в одну таблицю (PostgreSQL). Підсвічування руху кольором: зелений — позиція покращилася (BSR упав, товар продається краще), червоний — погіршилася. Розріз по категоріях.",
    },
    "cat": {"EN": "Product category", "RU": "Категория товара", "UK": "Категорія товару"},
    "bsr_h": {"EN": "BSR by day", "RU": "BSR по дням", "UK": "BSR по днях"},
    "bsr_cap": {"EN": "Lower BSR = sells better. 🟢 improved · 🔴 worsened (day to day).", "RU": "Чем меньше BSR, тем лучше продаётся. 🟢 позиция улучшилась · 🔴 ухудшилась (день к дню).", "UK": "Що менший BSR, то краще продається. 🟢 позиція покращилася · 🔴 погіршилася (день до дня)."},
    "rise_h": {"EN": "Who rises, who falls (over the period)", "RU": "Кто растёт, кто падает (за период)", "UK": "Хто зростає, хто падає (за період)"},
    "c_start": {"EN": "Start BSR", "RU": "Старт BSR", "UK": "Старт BSR"},
    "c_end": {"EN": "End BSR", "RU": "Конец BSR", "UK": "Кінець BSR"},
    "c_change": {"EN": "Change", "RU": "Изменение", "UK": "Зміна"},
    "c_trend": {"EN": "Trend", "RU": "Тренд", "UK": "Тренд"},
    "tr_up": {"EN": "🟢 rising", "RU": "🟢 растёт", "UK": "🟢 зростає"},
    "tr_down": {"EN": "🔴 falling", "RU": "🔴 падает", "UK": "🔴 падає"},
    "tr_flat": {"EN": "⚪ flat", "RU": "⚪ ровно", "UK": "⚪ рівно"},
    "shot_h": {"EN": "How it looks in Google Sheets", "RU": "Так это выглядит в Google Sheets", "UK": "Так це виглядає в Google Sheets"},
    "shot_cap": {"EN": "Real tracking tool (brands, ASINs and niche anonymized).", "RU": "Реальный инструмент трекинга (бренды, ASIN и ниша обезличены).", "UK": "Реальний інструмент трекінгу (бренди, ASIN і ніша знеособлені)."},
    "val_h": {"EN": "Business value", "RU": "Ценность для бизнеса", "UK": "Цінність для бізнесу"},
    "val": {
        "EN": "You see in real time which competitor is accelerating (a reason to check their promos/ads) and who is slipping (a reason to take share). Pricing and ad decisions are made on data, not feelings.",
        "RU": "Видно в реальном времени, кто из конкурентов разгоняется (повод проверить их акции/рекламу) и кто проседает (повод забрать долю). Решения по цене и рекламе принимаются на данных, а не на ощущениях.",
        "UK": "Видно в реальному часі, хто з конкурентів розганяється (привід перевірити їхні акції/рекламу) і хто просідає (привід забрати частку). Рішення щодо ціни та реклами ухвалюються на даних, а не на відчуттях.",
    },
    "under_h": {"EN": "⚙️ Under the hood (for technical audience)", "RU": "⚙️ Под капотом (для технической аудитории)", "UK": "⚙️ Під капотом (для технічної аудиторії)"},
    "under": {"EN": "Daily BSR collection by competitor ASIN list via a scraping service, write to PostgreSQL (competitors_bsr) with day history. Dashboard reads from DB via st.secrets, conditional formatting for fast visual scan.", "RU": "Ежедневный сбор BSR по списку ASIN конкурентов через сервис парсинга, запись в PostgreSQL (competitors_bsr) с историей по дням. Дашборд читает из базы через st.secrets, условное форматирование для быстрого визуального скана.", "UK": "Щоденний збір BSR за списком ASIN конкурентів через сервіс парсингу, запис у PostgreSQL (competitors_bsr) з історією по днях. Дашборд читає з бази через st.secrets, умовне форматування для швидкого візуального скану."},
    "nda": {"EN": "Real brands, ASINs and niche — under NDA.", "RU": "Реальные бренды, ASIN и ниша — под NDA.", "UK": "Реальні бренди, ASIN і ніша — під NDA."},
}

st.title(T["title"][lang])
st.caption(T["cap"][lang])

st.markdown(f"### {T['task_h'][lang]}")
st.write(T["task"][lang])
st.markdown(f"### {T['sol_h'][lang]}")
st.write(T["sol"][lang])

st.divider()

@st.cache_data
def synthetic():
    rng = np.random.default_rng(11)
    categories = {
        "Base layer": ["Brand A — model 1", "Brand A — model 2", "Brand B — model 1", "Brand C — model 1"],
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

cat = st.selectbox(T["cat"][lang], sorted(raw["category"].unique()))
sub = raw[raw["category"] == cat].copy()
sub["d"] = sub["date"].dt.strftime("%d.%m")
df = sub.pivot_table(index="product", columns="d", values="bsr", aggfunc="first")

st.markdown(f"### {T['bsr_h'][lang]} — {cat}")
st.caption(T["bsr_cap"][lang])

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

st.markdown(f"### {T['rise_h'][lang]}")
first_col, last_col = df.columns[0], df.columns[-1]
summary = pd.DataFrame({T["c_start"][lang]: df[first_col], T["c_end"][lang]: df[last_col]})
summary[T["c_change"][lang]] = summary[T["c_start"][lang]] - summary[T["c_end"][lang]]
summary[T["c_trend"][lang]] = summary[T["c_change"][lang]].apply(
    lambda x: T["tr_up"][lang] if x > 0 else (T["tr_down"][lang] if x < 0 else T["tr_flat"][lang])
)
summary = summary.sort_values(T["c_change"][lang], ascending=False)
st.dataframe(
    summary.style.format({T["c_start"][lang]: "{:,.0f}", T["c_end"][lang]: "{:,.0f}", T["c_change"][lang]: "{:+,.0f}"}),
    use_container_width=True,
)

st.divider()

st.markdown(f"### {T['shot_h'][lang]}")
st.caption(T["shot_cap"][lang])
_img = Path(__file__).parent.parent / "assets" / "competitor_bsr.png"
if _img.exists():
    st.image(str(_img), use_container_width=True)
else:
    st.info("📷 assets/competitor_bsr.png", icon="📷")

st.divider()

st.markdown(f"### {T['val_h'][lang]}")
st.write(T["val"][lang])

with st.expander(T["under_h"][lang]):
    st.write(T["under"][lang])
    st.code("SELECT product, category, date, bsr\nFROM competitors_bsr\nORDER BY category, product, date;", language="sql")

st.info(T["nda"][lang], icon="🔒")
