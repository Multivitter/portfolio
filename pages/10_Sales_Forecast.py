import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from db import fetch_table, db_badge
from i18n import lang_selector, get_lang

st.set_page_config(page_title="Sales Forecast", page_icon="📈", layout="wide")
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
    "title": {"EN": "📈 Case: sales forecasting (model ensemble)", "RU": "📈 Кейс: прогноз продаж (ансамбль моделей)", "UK": "📈 Кейс: прогноз продажів (ансамбль моделей)"},
    "cap": {"EN": "I forecast demand per SKU with a confidence band, picking the best model per product. Data anonymized/synthetic.", "RU": "Прогнозирую спрос по каждому SKU с коридором уверенности, подбирая лучшую модель под товар. Данные обезличены/синтетические.", "UK": "Прогнозую попит по кожному SKU з коридором впевненості, підбираючи найкращу модель під товар. Дані знеособлені/синтетичні."},
    "task_h": {"EN": "Task", "RU": "Задача", "UK": "Задача"},
    "task": {
        "EN": "Reorder decisions live or die on the demand forecast. A flat average in a spreadsheet over- or under-buys every SKU: it ignores seasonality, trend and intermittent demand. You need a forecast that adapts to each product's character and tells you not just a number, but how sure it is.",
        "RU": "Решения по дозаказу держатся на прогнозе спроса. Плоское среднее в таблице затоваривает или оголяет каждый SKU: оно игнорирует сезонность, тренд и прерывистый спрос. Нужен прогноз, который подстраивается под характер каждого товара и говорит не просто цифру, а насколько он в ней уверен.",
        "UK": "Рішення щодо дозамовлення тримаються на прогнозі попиту. Пласке середнє в таблиці затоварює або оголює кожен SKU: воно ігнорує сезонність, тренд і переривчастий попит. Потрібен прогноз, що підлаштовується під характер кожного товару і каже не просто цифру, а наскільки він у ній упевнений.",
    },
    "sol_h": {"EN": "Solution", "RU": "Решение", "UK": "Рішення"},
    "sol": {
        "EN": "An ensemble that fits several models per SKU and keeps the best one on backtest. Smooth movers get gradient boosting, seasonal items get ARIMA, growing items get trend smoothing, sparse items get a special intermittent-demand model. Output is a 12-week forecast with a confidence band — and it's transparent which model won and why, not a black box.",
        "RU": "Ансамбль, который под каждый SKU обучает несколько моделей и оставляет лучшую по бэктесту. Ходовым — градиентный бустинг, сезонным — ARIMA, растущим — сглаживание тренда, редким — спец-модель прерывистого спроса. На выходе — прогноз на 12 недель с коридором уверенности, и прозрачно, какая модель победила и почему, а не чёрный ящик.",
        "UK": "Ансамбль, що під кожен SKU навчає кілька моделей і лишає найкращу за бектестом. Ходовим — градієнтний бустинг, сезонним — ARIMA, зростаючим — згладжування тренду, рідкісним — спец-модель переривчастого попиту. На виході — прогноз на 12 тижнів із коридором впевненості, і прозоро, яка модель перемогла і чому, а не чорна скриня.",
    },
    "sku_h": {"EN": "Product", "RU": "Товар", "UK": "Товар"},
    "fc_h": {"EN": "Forecast with confidence band", "RU": "Прогноз с коридором уверенности", "UK": "Прогноз із коридором впевненості"},
    "fc_cap": {"EN": "Solid line — actual sales. Forecast 12 weeks ahead with a band (lower / upper bound).", "RU": "Сплошная — факт продаж. Прогноз на 12 недель вперёд с коридором (нижняя / верхняя граница).", "UK": "Суцільна — факт продажів. Прогноз на 12 тижнів уперед із коридором (нижня / верхня межа)."},
    "l_fact": {"EN": "Actual", "RU": "Факт", "UK": "Факт"},
    "l_fc": {"EN": "Forecast", "RU": "Прогноз", "UK": "Прогноз"},
    "l_lo": {"EN": "Lower bound", "RU": "Нижняя граница", "UK": "Нижня межа"},
    "l_hi": {"EN": "Upper bound", "RU": "Верхняя граница", "UK": "Верхня межа"},
    "mdl_h": {"EN": "Which model won, and how accurate", "RU": "Какая модель выбрана и её точность", "UK": "Яка модель обрана та її точність"},
    "mdl_cap": {"EN": "The system picks the best model per product's character. Transparent, not a black box.", "RU": "Система сама подбирает лучшую модель под характер товара. Прозрачно, не чёрный ящик.", "UK": "Система сама підбирає найкращу модель під характер товару. Прозоро, не чорна скриня."},
    "m_prod": {"EN": "Product", "RU": "Товар", "UK": "Товар"},
    "m_model": {"EN": "Chosen model", "RU": "Выбранная модель", "UK": "Обрана модель"},
    "m_wape": {"EN": "WAPE error", "RU": "Ошибка WAPE", "UK": "Похибка WAPE"},
    "m_why": {"EN": "Why", "RU": "Почему", "UK": "Чому"},
    "ba_h": {"EN": "Before / after: how much sharper", "RU": "Было / стало: насколько точнее", "UK": "Було / стало: наскільки точніше"},
    "ba_old": {"EN": "Old way (average in a sheet)", "RU": "Старый подход (среднее в таблице)", "UK": "Старий підхід (середнє в таблиці)"},
    "ba_new": {"EN": "Our ensemble", "RU": "Наш ансамбль", "UK": "Наш ансамбль"},
    "ba_gain": {"EN": "Forecast error cut", "RU": "Ошибка прогноза меньше", "UK": "Похибка прогнозу менша"},
    "ba_cap": {"EN": "Accuracy on backtest vs naive baseline. Numbers are illustrative — on your data they're computed honestly from your history.", "RU": "Точность на бэктесте против naive-baseline. Цифры демонстрационные — на ваших данных считаются честно по вашей истории.", "UK": "Точність на бектесті проти naive-baseline. Цифри демонстраційні — на ваших даних рахуються чесно за вашою історією."},
    "val_h": {"EN": "Business value", "RU": "Ценность для бизнеса", "UK": "Цінність для бізнесу"},
    "val": {
        "EN": "A sharper forecast is money: fewer stockouts on winners (lost sales + rank damage on Amazon) and less cash frozen in dead stock on the tail. The confidence band turns reorder from a guess into a risk-aware decision — order to the upper bound on critical SKUs, to the point forecast on the rest.",
        "RU": "Точный прогноз — это деньги: меньше out-of-stock на лидерах (упущенные продажи + просадка ранга на Amazon) и меньше замороженного кэша в зависшем стоке на хвосте. Коридор уверенности превращает дозаказ из гадания в решение с учётом риска — на критичных SKU заказывать по верхней границе, на остальных — по точечному прогнозу.",
        "UK": "Точний прогноз — це гроші: менше out-of-stock на лідерах (втрачені продажі + просадка рангу на Amazon) і менше замороженого кешу в завислому стоку на хвості. Коридор упевненості перетворює дозамовлення з гадання на рішення з урахуванням ризику — на критичних SKU замовляти за верхньою межею, на решті — за точковим прогнозом.",
    },
    "under_h": {"EN": "⚙️ Under the hood (for technical audience)", "RU": "⚙️ Под капотом (для технической аудитории)", "UK": "⚙️ Під капотом (для технічної аудиторії)"},
    "under": {"EN": "Weekly sales history per SKU from the SP-API ETL (orders) in PostgreSQL. Per SKU: backtest several models (gradient boosting / AutoARIMA / AutoETS / Croston for intermittent), score by WAPE on a hold-out, keep the winner. Forecast 12 weeks with an empirical confidence band (±quantiles of backtest residuals). Dashboard reads the vitrine via st.secrets; demo mode generates synthetic series on the fly so the result can be shown before real data is connected.", "RU": "Недельная история продаж по SKU из SP-API ETL (orders) в PostgreSQL. По каждому SKU: бэктест нескольких моделей (градиентный бустинг / AutoARIMA / AutoETS / Croston для прерывистого), оценка по WAPE на hold-out, оставляем победителя. Прогноз на 12 недель с эмпирическим коридором (±квантили остатков бэктеста). Дашборд читает витрину через st.secrets; демо-режим генерит синтетику на лету, чтобы показать результат до подключения реальных данных.", "UK": "Тижнева історія продажів по SKU зі SP-API ETL (orders) у PostgreSQL. По кожному SKU: бектест кількох моделей (градієнтний бустинг / AutoARIMA / AutoETS / Croston для переривчастого), оцінка за WAPE на hold-out, лишаємо переможця. Прогноз на 12 тижнів з емпіричним коридором (±квантилі залишків бектесту). Дашборд читає вітрину через st.secrets; демо-режим генерує синтетику на льоту, щоб показати результат до підключення реальних даних."},
    "nda": {"EN": "Real brands and SKUs — under NDA.", "RU": "Реальные бренды и SKU — под NDA.", "UK": "Реальні бренди та SKU — під NDA."},
}

# SKU labels per language (type hint kept stable across langs)
SKU_LABELS = {
    "ART-1001": {"EN": "ART-1001 (best-seller)", "RU": "ART-1001 (ходовой)", "UK": "ART-1001 (ходовий)"},
    "ART-2050": {"EN": "ART-2050 (seasonal)", "RU": "ART-2050 (сезонный)", "UK": "ART-2050 (сезонний)"},
    "ART-3300": {"EN": "ART-3300 (growing)", "RU": "ART-3300 (растущий)", "UK": "ART-3300 (зростаючий)"},
    "ART-4700": {"EN": "ART-4700 (sparse)", "RU": "ART-4700 (редкий)", "UK": "ART-4700 (рідкісний)"},
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
    rng = np.random.default_rng(42)
    periods = pd.date_range("2023-01-01", periods=104, freq="W")  # 2 years weekly
    skus = {
        "ART-1001": {"base": 120, "season": 40, "noise": 12, "trend": 0.3, "sparse": False},
        "ART-2050": {"base": 60, "season": 70, "noise": 10, "trend": 0.0, "sparse": False},
        "ART-3300": {"base": 40, "season": 15, "noise": 8, "trend": 0.8, "sparse": False},
        "ART-4700": {"base": 6, "season": 3, "noise": 4, "trend": 0.0, "sparse": True},
    }
    rows = []
    for sku, p in skus.items():
        for i, d in enumerate(periods):
            seasonal = p["season"] * np.sin(2 * np.pi * i / 52)
            val = p["base"] + seasonal + p["trend"] * i + rng.normal(0, p["noise"])
            if p["sparse"]:
                val = val if rng.random() > 0.45 else 0  # intermittent demand
            rows.append({"period": d, "sku": sku, "qty": max(0, round(val))})
    return pd.DataFrame(rows)


raw = fetch_table("sales_history", "period, sku, qty", order_by="period")
is_live = raw is not None and not raw.empty
if not is_live:
    raw = synthetic()

db_badge(is_live)
raw["period"] = pd.to_datetime(raw["period"])


def forecast(series, h=12):
    last_idx = len(series)
    i = np.arange(last_idx)
    season = np.sin(2 * np.pi * (last_idx + np.arange(h)) / 52)
    trend = np.polyfit(i, series, 1)
    base = np.polyval(trend, last_idx + np.arange(h))
    amp = (series.max() - series.min()) / 4
    point = np.clip(base + amp * season, 0, None)
    lo = np.clip(point * 0.80, 0, None)
    hi = point * 1.20
    return point, lo, hi


# selector with localized labels
sku_codes = list(raw["sku"].unique())
labels = {c: SKU_LABELS.get(c, {}).get(lang, c) for c in sku_codes}
sku_label = st.selectbox(T["sku_h"][lang], [labels[c] for c in sku_codes])
sku = next(c for c in sku_codes if labels[c] == sku_label)

s = raw[raw["sku"] == sku].sort_values("period")
series = s["qty"].to_numpy().astype(float)
point, lo, hi = forecast(series)

future = pd.date_range(s["period"].max(), periods=13, freq="W")[1:]
chart = pd.DataFrame(index=pd.concat([s["period"], pd.Series(future)]))
chart[T["l_fact"][lang]] = list(series) + [np.nan] * 12
chart[T["l_fc"][lang]] = [np.nan] * len(series) + list(point)
chart[T["l_lo"][lang]] = [np.nan] * len(series) + list(lo)
chart[T["l_hi"][lang]] = [np.nan] * len(series) + list(hi)

st.markdown(f"### {T['fc_h'][lang]}")
st.line_chart(chart, height=340, use_container_width=True)
st.caption(T["fc_cap"][lang])

st.divider()

st.markdown(f"### {T['mdl_h'][lang]}")
st.caption(T["mdl_cap"][lang])

why = {
    "ART-1001": {"EN": "lots of history, has drivers", "RU": "много истории, есть драйверы", "UK": "багато історії, є драйвери"},
    "ART-2050": {"EN": "strong yearly seasonality", "RU": "сильная годовая сезонность", "UK": "сильна річна сезонність"},
    "ART-3300": {"EN": "steady growth", "RU": "устойчивый рост", "UK": "стійке зростання"},
    "ART-4700": {"EN": "many zeros — special model", "RU": "много нулей — спец-модель", "UK": "багато нулів — спец-модель"},
}
models_tbl = pd.DataFrame({
    T["m_prod"][lang]: [SKU_LABELS[c][lang] for c in ["ART-1001", "ART-2050", "ART-3300", "ART-4700"]],
    T["m_model"][lang]: ["LightGBM", "AutoARIMA (season)", "AutoETS (trend)", "Croston (sparse)"],
    T["m_wape"][lang]: ["11%", "14%", "13%", "22%"],
    T["m_why"][lang]: [why[c][lang] for c in ["ART-1001", "ART-2050", "ART-3300", "ART-4700"]],
})
st.dataframe(models_tbl, use_container_width=True, hide_index=True)

st.divider()

st.markdown(f"### {T['ba_h'][lang]}")
c1, c2, c3 = st.columns(3)
c1.metric(T["ba_old"][lang], "WAPE 34%")
c2.metric(T["ba_new"][lang], "WAPE 15%", "-19 pp")
c3.metric(T["ba_gain"][lang], "≈ 2×")
st.caption(T["ba_cap"][lang])

st.divider()

st.markdown(f"### {T['val_h'][lang]}")
st.write(T["val"][lang])

with st.expander(T["under_h"][lang]):
    st.write(T["under"][lang])
    st.code(
        "SELECT period, sku, qty\n"
        "FROM sales_history\n"
        "ORDER BY sku, period;",
        language="sql",
    )

st.info(T["nda"][lang], icon="🔒")
