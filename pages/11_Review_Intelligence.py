import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from db import fetch_table, db_badge
from i18n import lang_selector, get_lang

st.set_page_config(page_title="Review Intelligence", page_icon="⭐", layout="wide")
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
    "title": {"EN": "⭐ Case: review intelligence (multi-country)", "RU": "⭐ Кейс: аналитика отзывов (по странам)", "UK": "⭐ Кейс: аналітика відгуків (по країнах)"},
    "cap": {"EN": "I scrape Amazon reviews across marketplaces, store them and surface what's killing the rating — per ASIN, per country. Data anonymized/synthetic.", "RU": "Скрейплю отзывы Amazon по маркетплейсам, складываю в базу и показываю, что убивает рейтинг — по каждому ASIN и стране. Данные обезличены/синтетические.", "UK": "Скрейплю відгуки Amazon по маркетплейсах, складаю в базу і показую, що вбиває рейтинг — по кожному ASIN і країні. Дані знеособлені/синтетичні."},
    "task_h": {"EN": "Task", "RU": "Задача", "UK": "Задача"},
    "task": {
        "EN": "Reviews live on six marketplaces in different languages, thousands of them, and they decide your conversion and ad cost. A dropping rating bleeds money silently. You can't read every review by hand. You need everything collected in one place, scored, and pointed at the exact ASIN and country where the damage is coming from.",
        "RU": "Отзывы живут на шести маркетплейсах на разных языках, тысячами, и они определяют конверсию и стоимость рекламы. Падающий рейтинг тихо сливает деньги. Прочитать каждый отзыв руками невозможно. Нужно собрать всё в одном месте, оценить и ткнуть пальцем в конкретный ASIN и страну, откуда идёт урон.",
        "UK": "Відгуки живуть на шести маркетплейсах різними мовами, тисячами, і вони визначають конверсію та вартість реклами. Падаючий рейтинг тихо зливає гроші. Прочитати кожен відгук руками неможливо. Треба зібрати все в одному місці, оцінити і тицьнути пальцем у конкретний ASIN і країну, звідки йде шкода.",
    },
    "sol_h": {"EN": "Solution", "RU": "Решение", "UK": "Рішення"},
    "sol": {
        "EN": "A scraper pulls reviews by ASIN list from all marketplaces (Apify / Bright Data, you pick which star ratings to collect, optional infinite loop). Everything lands in PostgreSQL and updates daily. The dashboard then computes rating health, negative share, verified share and the single most toxic ASIN — plus a country breakdown showing exactly where the rating is weakest.",
        "RU": "Скрапер тянет отзывы по списку ASIN со всех маркетплейсов (Apify / Bright Data, выбираешь какие звёзды собирать, опционально бесконечный цикл). Всё ложится в PostgreSQL и обновляется ежедневно. Дашборд считает здоровье рейтинга, долю негатива, долю верифицированных и самый токсичный ASIN — плюс разрез по странам, который показывает, где именно рейтинг проседает.",
        "UK": "Скрапер тягне відгуки за списком ASIN з усіх маркетплейсів (Apify / Bright Data, обираєш які зірки збирати, опційно безкінечний цикл). Усе лягає в PostgreSQL і оновлюється щодня. Дашборд рахує здоров'я рейтингу, частку негативу, частку верифікованих і найтоксичніший ASIN — плюс розріз по країнах, що показує, де саме рейтинг просідає.",
    },
    "ov_h": {"EN": "Amazon reviews — overview", "RU": "Amazon Reviews — обзор", "UK": "Amazon Reviews — огляд"},
    "ov_avg": {"EN": "Avg rating", "RU": "Средний рейтинг", "UK": "Середній рейтинг"},
    "ov_pos": {"EN": "Positive (4-5★)", "RU": "Позитив (4-5★)", "UK": "Позитив (4-5★)"},
    "ov_neg": {"EN": "Negative (1-2★)", "RU": "Негатив (1-2★)", "UK": "Негатив (1-2★)"},
    "ov_ver": {"EN": "Verified", "RU": "Верифиц.", "UK": "Верифік."},
    "ov_asin": {"EN": "ASINs", "RU": "ASIN", "UK": "ASIN"},
    "ov_sub": {"EN": "reviews · {a} ASINs · {c} countries", "RU": "отзывов · {a} ASIN · {c} стран", "UK": "відгуків · {a} ASIN · {c} країн"},
    "ins_h": {"EN": "🧠 Insights across all ASINs", "RU": "🧠 Инсайты по всем ASIN", "UK": "🧠 Інсайти по всіх ASIN"},
    "i_health": {"EN": "Rating health", "RU": "Здоровье рейтинга", "UK": "Здоров'я рейтингу"},
    "i_health_bad": {"EN": "Avg {v}★ — critical! Hurts conversion and inflates PPC.", "RU": "Средний {v}★ — критично! Режет конверсию и удорожает PPC.", "UK": "Середній {v}★ — критично! Ріже конверсію і здорожчує PPC."},
    "i_health_ok": {"EN": "Avg {v}★ — healthy.", "RU": "Средний {v}★ — здоровый.", "UK": "Середній {v}★ — здоровий."},
    "i_neg": {"EN": "Negativity level", "RU": "Уровень негатива", "UK": "Рівень негативу"},
    "i_neg_bad": {"EN": "{v}% negative — critical! Fix product or listing now.", "RU": "{v}% негатива — критично! Срочно фиксь продукт или листинг.", "UK": "{v}% негативу — критично! Терміново фікси продукт або лістинг."},
    "i_neg_ok": {"EN": "{v}% negative — under control.", "RU": "{v}% негатива — под контролем.", "UK": "{v}% негативу — під контролем."},
    "i_loyal": {"EN": "Loyalty", "RU": "Лояльность", "UK": "Лояльність"},
    "i_loyal_v": {"EN": "{v}% positive (4-5★).", "RU": "{v}% позитивных (4-5★).", "UK": "{v}% позитивних (4-5★)."},
    "i_ver": {"EN": "Verification", "RU": "Верификация", "UK": "Верифікація"},
    "i_ver_v": {"EN": "{v}% verified — high trust on Amazon.", "RU": "{v}% верифицированы — высокое доверие у Amazon.", "UK": "{v}% верифіковані — висока довіра в Amazon."},
    "i_tox": {"EN": "Toxic ASIN", "RU": "Токсичный ASIN", "UK": "Токсичний ASIN"},
    "i_tox_v": {"EN": "{asin} — {n} negatives. Start the analysis here.", "RU": "{asin} — {n} негативных. Начни анализ с него.", "UK": "{asin} — {n} негативних. Почни аналіз із нього."},
    "geo_h": {"EN": "🌍 Country breakdown", "RU": "🌍 Анализ по странам", "UK": "🌍 Аналіз по країнах"},
    "geo_cnt": {"EN": "Review count", "RU": "Количество", "UK": "Кількість"},
    "geo_rat": {"EN": "Rating", "RU": "Рейтинг", "UK": "Рейтинг"},
    "geo_neg": {"EN": "% Negative", "RU": "% Негатива", "UK": "% Негативу"},
    "g_country": {"EN": "Country", "RU": "Страна", "UK": "Країна"},
    "g_reviews": {"EN": "Reviews", "RU": "Отзывов", "UK": "Відгуків"},
    "g_avg": {"EN": "Avg ★", "RU": "Avg ★", "UK": "Avg ★"},
    "g_pos": {"EN": "% Pos", "RU": "% Pos", "UK": "% Pos"},
    "g_neg": {"EN": "% Neg", "RU": "% Neg", "UK": "% Neg"},
    "shot_h": {"EN": "The scraper that feeds it", "RU": "Скрапер, который это питает", "UK": "Скрапер, що це живить"},
    "shot_cap": {"EN": "Collection UI: ASIN list, source (Apify / Bright Data), which stars to collect, infinite-loop mode.", "RU": "Интерфейс сбора: список ASIN, источник (Apify / Bright Data), какие звёзды собирать, режим бесконечного цикла.", "UK": "Інтерфейс збору: список ASIN, джерело (Apify / Bright Data), які зірки збирати, режим безкінечного циклу."},
    "val_h": {"EN": "Business value", "RU": "Ценность для бизнеса", "UK": "Цінність для бізнесу"},
    "val": {
        "EN": "Rating drives both conversion and ad cost on Amazon, so a slipping rating is a double leak. This turns thousands of multilingual reviews into one verdict: which ASIN and which country to fix first. Instead of guessing, the team works the single toxic ASIN that's dragging the whole account.",
        "RU": "Рейтинг тянет и конверсию, и стоимость рекламы на Amazon, так что просадка рейтинга — двойная течь. Это превращает тысячи многоязычных отзывов в один вердикт: какой ASIN и какую страну чинить первыми. Вместо догадок команда работает с тем самым токсичным ASIN, который тянет вниз весь аккаунт.",
        "UK": "Рейтинг тягне і конверсію, і вартість реклами на Amazon, тож просадка рейтингу — подвійна теча. Це перетворює тисячі багатомовних відгуків на один вердикт: який ASIN і яку країну лагодити першими. Замість здогадок команда працює з тим самим токсичним ASIN, що тягне вниз увесь акаунт.",
    },
    "under_h": {"EN": "⚙️ Under the hood (for technical audience)", "RU": "⚙️ Под капотом (для технической аудитории)", "UK": "⚙️ Під капотом (для технічної аудиторії)"},
    "under": {"EN": "Reviews collected by ASIN list across 6 marketplaces via Apify / Bright Data actors (selectable star filter, optional continuous loop with a pause between passes). Written to PostgreSQL (reviews) with marketplace, stars, verified flag and date; daily incremental update. Dashboard reads via st.secrets and aggregates: avg rating, positive/negative share, verified share, per-ASIN negative counts (toxic-ASIN ranking) and a per-country cut (count / rating / %neg).", "RU": "Отзывы собираются по списку ASIN на 6 маркетплейсах через акторы Apify / Bright Data (выбор фильтра звёзд, опциональный непрерывный цикл с паузой между проходами). Пишутся в PostgreSQL (reviews) с маркетплейсом, звёздами, флагом verified и датой; ежедневное инкрементальное обновление. Дашборд читает через st.secrets и агрегирует: средний рейтинг, доля позитива/негатива, доля верифицированных, счётчики негатива по ASIN (рейтинг токсичных) и разрез по странам (кол-во / рейтинг / %neg).", "UK": "Відгуки збираються за списком ASIN на 6 маркетплейсах через актори Apify / Bright Data (вибір фільтра зірок, опційний безперервний цикл із паузою між проходами). Пишуться в PostgreSQL (reviews) з маркетплейсом, зірками, прапором verified і датою; щоденне інкрементальне оновлення. Дашборд читає через st.secrets і агрегує: середній рейтинг, частка позитиву/негативу, частка верифікованих, лічильники негативу по ASIN (рейтинг токсичних) і розріз по країнах (к-сть / рейтинг / %neg)."},
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
    rng = np.random.default_rng(31)
    countries = {
        "🇺🇸 USA (com)": 956, "🇩🇪 Germany (de)": 746, "🇨🇦 Canada (ca)": 484,
        "🇪🇸 Spain (es)": 457, "🇮🇹 Italy (it)": 320, "🇬🇧 UK (co.uk)": 141,
    }
    # target avg per country (loosely mirrors screenshot)
    target_avg = {"🇺🇸 USA (com)": 3.86, "🇩🇪 Germany (de)": 3.02, "🇨🇦 Canada (ca)": 3.03,
                  "🇪🇸 Spain (es)": 3.07, "🇮🇹 Italy (it)": 3.52, "🇬🇧 UK (co.uk)": 4.33}
    asins = [f"B0{''.join(rng.choice(list('0123456789ABCDEFGHJKLMNPQRSTUVWXYZ'),8))}" for _ in range(31)]
    rows = []
    for country, n in countries.items():
        mu = target_avg[country]
        for _ in range(n):
            # sample star skewed toward mu
            p = np.clip(rng.normal(mu, 1.3), 1, 5)
            star = int(round(p))
            star = min(5, max(1, star))
            rows.append({
                "asin": rng.choice(asins),
                "country": country,
                "stars": star,
                "verified": bool(rng.random() < 0.97),
                "date": pd.Timestamp("2025-01-01") + pd.Timedelta(days=int(rng.integers(0, 120))),
            })
    return pd.DataFrame(rows)


raw = fetch_table("reviews", "asin, country, stars, verified, date", order_by="date")
is_live = raw is not None and not raw.empty
if not is_live:
    raw = synthetic()

db_badge(is_live)

total_reviews = len(raw)
avg_rating = raw["stars"].mean()
pos_share = (raw["stars"] >= 4).mean() * 100
neg_share = (raw["stars"] <= 2).mean() * 100
ver_share = raw["verified"].astype(bool).mean() * 100
n_asins = raw["asin"].nunique()
n_countries = raw["country"].nunique()

# ── Overview banner ───────────────────────────────────
st.markdown(f"### {T['ov_h'][lang]}")
rating_color = "#d85a30" if avg_rating < 4.0 else "#1d9e75"
st.markdown(
    f"<div style='background:linear-gradient(90deg,#0d1f14,#14241a);border-radius:12px;padding:18px 22px'>"
    f"<span style='color:#9ad;font-size:12px;letter-spacing:1px'>★ {T['ov_avg'][lang].upper()}</span><br>"
    f"<span style='color:{rating_color};font-size:40px;font-weight:800'>{avg_rating:.2f}★</span>"
    f"<span style='color:#aaa;font-size:13px;margin-left:14px'>"
    f"{total_reviews:,} {T['ov_sub'][lang].format(a=n_asins, c=n_countries)}</span></div>",
    unsafe_allow_html=True,
)
c1, c2, c3, c4 = st.columns(4)
c1.metric(T["ov_pos"][lang], f"{pos_share:.1f}%")
c2.metric(T["ov_neg"][lang], f"{neg_share:.1f}%")
c3.metric(T["ov_ver"][lang], f"{ver_share:.0f}%")
c4.metric(T["ov_asin"][lang], n_asins)

st.divider()

# ── Insights ──────────────────────────────────────────
st.markdown(T["ins_h"][lang])

neg_by_asin = raw[raw["stars"] <= 2].groupby("asin").size().sort_values(ascending=False)
tox_asin = neg_by_asin.index[0] if not neg_by_asin.empty else "—"
tox_n = int(neg_by_asin.iloc[0]) if not neg_by_asin.empty else 0


def card(title, body, accent, bg):
    return (
        f"<div style='background:{bg};border-left:4px solid {accent};border-radius:8px;"
        f"padding:10px 14px;margin-bottom:10px;min-height:74px'>"
        f"<div style='color:{accent};font-weight:700;font-size:14px;margin-bottom:3px'>{title}</div>"
        f"<div style='color:#444;font-size:13px;line-height:1.4'>{body}</div></div>"
    )


RED, GREEN, YEL, BLU = "#d12c2c", "#1d9e75", "#c9a227", "#5b6ee1"
REDBG, GRNBG, YELBG, BLUBG = "#fbecec", "#fff8e6", "#fff8e6", "#eef0fc"

health_bad = avg_rating < 4.0
neg_bad = neg_share >= 20

L, R = st.columns(2)
with L:
    st.markdown(card(
        "🔴 " + T["i_health"][lang],
        (T["i_health_bad"] if health_bad else T["i_health_ok"])[lang].format(v=f"{avg_rating:.1f}"),
        RED if health_bad else GREEN, REDBG if health_bad else GRNBG), unsafe_allow_html=True)
    st.markdown(card(
        "🟢 " + T["i_loyal"][lang],
        T["i_loyal_v"][lang].format(v=f"{pos_share:.1f}"),
        YEL, YELBG), unsafe_allow_html=True)
    st.markdown(card(
        "⚠️ " + T["i_tox"][lang],
        T["i_tox_v"][lang].format(asin=tox_asin, n=tox_n),
        RED, REDBG), unsafe_allow_html=True)
with R:
    st.markdown(card(
        "🔴 " + T["i_neg"][lang],
        (T["i_neg_bad"] if neg_bad else T["i_neg_ok"])[lang].format(v=f"{neg_share:.1f}"),
        RED if neg_bad else GREEN, REDBG if neg_bad else GRNBG), unsafe_allow_html=True)
    st.markdown(card(
        "✅ " + T["i_ver"][lang],
        T["i_ver_v"][lang].format(v=f"{ver_share:.1f}"),
        BLU, BLUBG), unsafe_allow_html=True)

st.divider()

# ── Country breakdown ─────────────────────────────────
st.markdown(T["geo_h"][lang])

geo = raw.groupby("country").agg(
    reviews=("stars", "size"),
    avg=("stars", "mean"),
    pos=("stars", lambda x: (x >= 4).mean() * 100),
    neg=("stars", lambda x: (x <= 2).mean() * 100),
).reset_index()

g1, g2, g3 = st.columns(3)
with g1:
    st.markdown(f"**📊 {T['geo_cnt'][lang]}**")
    st.bar_chart(geo.set_index("country")["reviews"].sort_values(), horizontal=True, height=260)
with g2:
    st.markdown(f"**⭐ {T['geo_rat'][lang]}**")
    st.bar_chart(geo.set_index("country")["avg"].sort_values(), horizontal=True, height=260)
with g3:
    st.markdown(f"**🔴 {T['geo_neg'][lang]}**")
    st.bar_chart(geo.set_index("country")["neg"].sort_values(), horizontal=True, height=260)

geo_tbl = geo.sort_values("reviews", ascending=False).rename(columns={
    "country": T["g_country"][lang], "reviews": T["g_reviews"][lang],
    "avg": T["g_avg"][lang], "pos": T["g_pos"][lang], "neg": T["g_neg"][lang],
})
st.dataframe(
    geo_tbl.style.format({
        T["g_avg"][lang]: "{:.2f}", T["g_pos"][lang]: "{:.1f}%", T["g_neg"][lang]: "{:.1f}%",
    }).background_gradient(subset=[T["g_neg"][lang]], cmap="Reds"),
    use_container_width=True, hide_index=True,
)

st.divider()

st.markdown(f"### {T['shot_h'][lang]}")
st.caption(T["shot_cap"][lang])
_img = Path(__file__).parent.parent / "assets" / "scraper_reviews.png"
if _img.exists():
    st.image(str(_img), use_container_width=True)
else:
    st.info("📷 assets/scraper_reviews.png", icon="📷")

st.divider()

st.markdown(f"### {T['val_h'][lang]}")
st.write(T["val"][lang])

with st.expander(T["under_h"][lang]):
    st.write(T["under"][lang])
    st.code(
        "SELECT country,\n"
        "       COUNT(*) AS reviews,\n"
        "       AVG(stars) AS avg_rating,\n"
        "       AVG((stars >= 4)::int) * 100 AS pct_pos,\n"
        "       AVG((stars <= 2)::int) * 100 AS pct_neg\n"
        "FROM reviews\n"
        "GROUP BY country\n"
        "ORDER BY reviews DESC;",
        language="sql",
    )

st.info(T["nda"][lang], icon="🔒")
