import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from db import fetch_table, db_badge
from i18n import lang_selector, get_lang

st.set_page_config(page_title="Catalog Monitor", page_icon="🛒", layout="wide")
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
    "title": {"EN": "🛒 Case: catalog monitor (Catalog vs Amazon)", "RU": "🛒 Кейс: монитор каталога (Каталог vs Amazon)", "UK": "🛒 Кейс: монітор каталогу (Каталог vs Amazon)"},
    "cap": {"EN": "I monitor live Amazon listings against the internal catalog daily. Data anonymized/synthetic.", "RU": "Ежедневно сверяю живые листинги Amazon с внутренним каталогом. Данные обезличены/синтетические.", "UK": "Щодня звіряю живі лістинги Amazon із внутрішнім каталогом. Дані знеособлені/синтетичні."},
    "task_h": {"EN": "Task", "RU": "Задача", "UK": "Задача"},
    "task": {
        "EN": "Hundreds of SKUs across marketplaces. Prices, coupons, promos, stock and ratings on Amazon drift away from what the internal catalog says — silently. Manually checking each listing is impossible. You need a system that pulls live Amazon data every day and flags every mismatch against the catalog: wrong price, missing coupon, out of stock, dropped rating.",
        "RU": "Сотни SKU по маркетплейсам. Цены, купоны, промо, сток и рейтинги на Amazon тихо расходятся с тем, что записано во внутреннем каталоге. Проверять каждый листинг руками невозможно. Нужна система, которая каждый день снимает живые данные Amazon и подсвечивает каждое расхождение с каталогом: не та цена, пропал купон, нет в наличии, упал рейтинг.",
        "UK": "Сотні SKU по маркетплейсах. Ціни, купони, промо, сток і рейтинги на Amazon тихо розходяться з тим, що записано у внутрішньому каталозі. Перевіряти кожен лістинг руками неможливо. Потрібна система, що щодня знімає живі дані Amazon і підсвічує кожне розходження з каталогом: не та ціна, зник купон, немає в наявності, упав рейтинг.",
    },
    "sol_h": {"EN": "Solution", "RU": "Решение", "UK": "Рішення"},
    "sol": {
        "EN": "Daily scraping of every ASIN via a scraping service, written straight into Google Sheets next to the catalog data. Each Amazon field sits beside its catalog counterpart and a cell turns red the moment they disagree. ASIN match, price discount %, coupons, promos, stock and rating are all cross-checked automatically. A built-in scheduler runs separate update groups (full / price-promo / stock-rating) at configured times.",
        "RU": "Ежедневный парсинг каждого ASIN через сервис скрейпинга, запись прямо в Google Sheets рядом с данными каталога. Каждое поле Amazon стоит рядом со своим аналогом из каталога, и ячейка краснеет в тот момент, когда они расходятся. ASIN-матч, скидка %, купоны, промо, сток и рейтинг сверяются автоматически. Встроенный планировщик запускает отдельные группы обновления (полная / цена-промо / сток-рейтинг) в заданное время.",
        "UK": "Щоденний парсинг кожного ASIN через сервіс скрейпінгу, запис прямо в Google Sheets поряд із даними каталогу. Кожне поле Amazon стоїть поряд зі своїм аналогом із каталогу, і клітинка червоніє в той момент, коли вони розходяться. ASIN-матч, знижка %, купони, промо, сток і рейтинг звіряються автоматично. Вбудований планувальник запускає окремі групи оновлення (повна / ціна-промо / сток-рейтинг) у заданий час.",
    },
    "cat": {"EN": "Catalog category", "RU": "Категория каталога", "UK": "Категорія каталогу"},
    "tbl_h": {"EN": "Catalog vs Amazon — live check", "RU": "Каталог vs Amazon — живая сверка", "UK": "Каталог vs Amazon — жива звірка"},
    "tbl_cap": {"EN": "🔴 mismatch between catalog and Amazon · 🟢 ASIN matched.", "RU": "🔴 расхождение каталога и Amazon · 🟢 ASIN совпал.", "UK": "🔴 розходження каталогу та Amazon · 🟢 ASIN збігся."},
    "col_model": {"EN": "Model", "RU": "Модель", "UK": "Модель"},
    "col_asin": {"EN": "ASIN", "RU": "ASIN", "UK": "ASIN"},
    "col_stock": {"EN": "Stock", "RU": "Сток", "UK": "Сток"},
    "col_cprice": {"EN": "Catalog price", "RU": "Цена каталог", "UK": "Ціна каталог"},
    "col_aprice": {"EN": "Amazon price", "RU": "Цена Amazon", "UK": "Ціна Amazon"},
    "col_coupon": {"EN": "Coupon", "RU": "Купон", "UK": "Купон"},
    "col_rating": {"EN": "Rating", "RU": "Рейтинг", "UK": "Рейтинг"},
    "kpi_h": {"EN": "Health snapshot", "RU": "Сводка здоровья", "UK": "Зведення здоров'я"},
    "kpi_total": {"EN": "SKUs monitored", "RU": "SKU под мониторингом", "UK": "SKU під моніторингом"},
    "kpi_issues": {"EN": "With mismatches", "RU": "С расхождениями", "UK": "З розходженнями"},
    "kpi_oos": {"EN": "Out of stock", "RU": "Нет в наличии", "UK": "Немає в наявності"},
    "kpi_ok": {"EN": "Clean", "RU": "Чистые", "UK": "Чисті"},
    "issue_h": {"EN": "What broke (priority list)", "RU": "Что сломалось (список приоритетов)", "UK": "Що зламалося (список пріоритетів)"},
    "i_sku": {"EN": "SKU", "RU": "SKU", "UK": "SKU"},
    "i_problem": {"EN": "Problem", "RU": "Проблема", "UK": "Проблема"},
    "p_price": {"EN": "💰 price differs", "RU": "💰 цена отличается", "UK": "💰 ціна відрізняється"},
    "p_coupon": {"EN": "🎟️ coupon mismatch", "RU": "🎟️ купон не совпадает", "UK": "🎟️ купон не збігається"},
    "p_stock": {"EN": "📦 out of stock", "RU": "📦 нет в наличии", "UK": "📦 немає в наявності"},
    "p_rating": {"EN": "⭐ rating dropped", "RU": "⭐ рейтинг упал", "UK": "⭐ рейтинг упав"},
    "shot_h": {"EN": "How it looks in Google Sheets", "RU": "Так это выглядит в Google Sheets", "UK": "Так це виглядає в Google Sheets"},
    "shot_cap": {"EN": "Real monitoring tool (brands, ASINs and niche anonymized).", "RU": "Реальный инструмент мониторинга (бренды, ASIN и ниша обезличены).", "UK": "Реальний інструмент моніторингу (бренди, ASIN і ніша знеособлені)."},
    "val_h": {"EN": "Business value", "RU": "Ценность для бизнеса", "UK": "Цінність для бізнесу"},
    "val": {
        "EN": "A wrong price or a vanished coupon on Amazon costs money every hour it stays unnoticed. The monitor catches it the same day, sorted by priority, so the team fixes what actually leaks margin first instead of scrolling hundreds of listings by hand.",
        "RU": "Не та цена или пропавший купон на Amazon стоят денег каждый час, пока их не заметили. Монитор ловит это в тот же день, отсортированно по приоритету, и команда чинит в первую очередь то, что реально течёт по марже, а не листает сотни листингов руками.",
        "UK": "Не та ціна або зниклий купон на Amazon коштують грошей щогодини, поки їх не помітили. Монітор ловить це того ж дня, відсортовано за пріоритетом, і команда лагодить насамперед те, що реально тече по маржі, а не гортає сотні лістингів руками.",
    },
    "under_h": {"EN": "⚙️ Under the hood (for technical audience)", "RU": "⚙️ Под капотом (для технической аудитории)", "UK": "⚙️ Під капотом (для технічної аудиторії)"},
    "under": {"EN": "Async scraping (aiohttp + semaphore, rate-limited) of each ASIN via ScrapingDog, with exponential-backoff retries and a fallback marker when GL category returns 'All'. Results are batch-written into Google Sheets (gspread batch_update) — values and per-cell conditional formatting in one pass. Catalog source columns are read from a separate sheet; an internal scheduler loops continuously and triggers Full / Yellow (price-promo) / Red (stock-rating-coupon) update groups at times defined in a Config sheet.", "RU": "Асинхронный парсинг (aiohttp + семафор, с ограничением скорости) каждого ASIN через ScrapingDog, ретраи с экспоненциальным backoff и маркер-фоллбек, когда GL-категория возвращает 'All'. Результаты пакетно пишутся в Google Sheets (gspread batch_update) — значения и поячеечное условное форматирование за один проход. Колонки каталога читаются из отдельного листа; внутренний планировщик крутится в бесконечном цикле и запускает группы Full / Yellow (цена-промо) / Red (сток-рейтинг-купон) во время, заданное в листе Config.", "UK": "Асинхронний парсинг (aiohttp + семафор, з обмеженням швидкості) кожного ASIN через ScrapingDog, ретраї з експоненційним backoff і маркер-фоллбек, коли GL-категорія повертає 'All'. Результати пакетно пишуться в Google Sheets (gspread batch_update) — значення та поклітинкове умовне форматування за один прохід. Колонки каталогу читаються з окремого аркуша; внутрішній планувальник крутиться в безкінечному циклі та запускає групи Full / Yellow (ціна-промо) / Red (сток-рейтинг-купон) у час, заданий в аркуші Config."},
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
    rng = np.random.default_rng(7)
    categories = {
        "Base layer": [f"BL-{i:03d}" for i in range(1, 13)],
        "Hoodie": [f"HD-{i:03d}" for i in range(1, 9)],
        "Socks": [f"SK-{i:03d}" for i in range(1, 11)],
    }
    rows = []
    for cat, models in categories.items():
        for m in models:
            cprice = round(float(rng.integers(25, 90)) + 0.99, 2)
            # mostly aligned, sometimes drifted
            drift = rng.random() < 0.25
            aprice = round(cprice + (rng.normal(0, 6) if drift else 0.0), 2)
            aprice = max(9.99, aprice)
            ccoupon = bool(rng.random() < 0.4)
            acoupon = ccoupon if rng.random() < 0.8 else (not ccoupon)
            in_stock = rng.random() > 0.12
            rating_now = round(float(rng.uniform(3.8, 4.9)), 1)
            rating_old = rating_now if rng.random() < 0.85 else round(rating_now + 0.2, 1)
            asin = "B0" + "".join(rng.choice(list("0123456789ABCDEFGHJKLMNPQRSTUVWXYZ"), 8))
            asin_match = rng.random() > 0.08
            rows.append({
                "model": m, "category": cat, "asin": asin,
                "asin_match": asin_match,
                "in_stock": in_stock,
                "catalog_price": cprice, "amazon_price": aprice,
                "catalog_coupon": ccoupon, "amazon_coupon": acoupon,
                "rating": rating_now, "old_rating": rating_old,
            })
    return pd.DataFrame(rows)


raw = fetch_table(
    "catalog_monitor",
    "model, category, asin, asin_match, in_stock, catalog_price, amazon_price, catalog_coupon, amazon_coupon, rating, old_rating",
)
is_live = raw is not None and not raw.empty
if not is_live:
    raw = synthetic()

db_badge(is_live)


def _flag(row):
    issues = []
    if abs(float(row["catalog_price"]) - float(row["amazon_price"])) > 0.5:
        issues.append("price")
    if bool(row["catalog_coupon"]) != bool(row["amazon_coupon"]):
        issues.append("coupon")
    if not bool(row["in_stock"]):
        issues.append("stock")
    if float(row["old_rating"]) - float(row["rating"]) >= 0.1:
        issues.append("rating")
    if not bool(row["asin_match"]):
        issues.append("asin")
    return issues


raw["_issues"] = raw.apply(_flag, axis=1)
raw["_n_issues"] = raw["_issues"].apply(len)

total = len(raw)
with_issues = int((raw["_n_issues"] > 0).sum())
oos = int((~raw["in_stock"].astype(bool)).sum())
clean = total - with_issues

st.markdown(f"### {T['kpi_h'][lang]}")
k1, k2, k3, k4 = st.columns(4)
k1.metric(T["kpi_total"][lang], total)
k2.metric(T["kpi_issues"][lang], with_issues)
k3.metric(T["kpi_oos"][lang], oos)
k4.metric(T["kpi_ok"][lang], clean)

st.divider()

cat = st.selectbox(T["cat"][lang], sorted(raw["category"].unique()))
sub = raw[raw["category"] == cat].copy()

view = pd.DataFrame({
    T["col_model"][lang]: sub["model"],
    T["col_asin"][lang]: sub["asin"],
    T["col_stock"][lang]: sub["in_stock"].map(lambda x: "✅" if x else "❌"),
    T["col_cprice"][lang]: sub["catalog_price"],
    T["col_aprice"][lang]: sub["amazon_price"],
    T["col_coupon"][lang]: sub.apply(
        lambda r: ("✅" if r["amazon_coupon"] else "❌"), axis=1
    ),
    T["col_rating"][lang]: sub["rating"],
}).reset_index(drop=True)

# keep issue info aligned by position for styling
_issues_list = sub["_issues"].reset_index(drop=True)
_cmatch = sub["catalog_coupon"].reset_index(drop=True)
_amatch = sub["amazon_coupon"].reset_index(drop=True)

st.markdown(f"### {T['tbl_h'][lang]} — {cat}")
st.caption(T["tbl_cap"][lang])

RED = "background-color: #d85a30; color: #ffffff"
GREEN = "background-color: #1d9e75; color: #ffffff"


def style_row(row):
    i = row.name
    styles = [""] * len(row)
    issues = _issues_list.iloc[i]
    cols = list(row.index)

    def setc(colkey, style):
        if colkey in cols:
            styles[cols.index(colkey)] = style

    # ASIN match coloring (green ok / red mismatch)
    setc(T["col_asin"][lang], RED if "asin" in issues else GREEN)
    if "price" in issues:
        setc(T["col_aprice"][lang], RED)
    if "stock" in issues:
        setc(T["col_stock"][lang], RED)
    if "coupon" in issues:
        setc(T["col_coupon"][lang], RED)
    if "rating" in issues:
        setc(T["col_rating"][lang], RED)
    return styles


styled = view.style.apply(style_row, axis=1).format({
    T["col_cprice"][lang]: "${:,.2f}",
    T["col_aprice"][lang]: "${:,.2f}",
    T["col_rating"][lang]: "{:.1f}",
})
st.dataframe(styled, use_container_width=True, hide_index=True)

st.divider()

st.markdown(f"### {T['issue_h'][lang]}")
prob_map = {
    "price": T["p_price"][lang],
    "coupon": T["p_coupon"][lang],
    "stock": T["p_stock"][lang],
    "rating": T["p_rating"][lang],
    "asin": "🔗 ASIN mismatch",
}
issue_rows = []
for _, r in raw[raw["_n_issues"] > 0].iterrows():
    issue_rows.append({
        T["i_sku"][lang]: r["model"],
        T["col_asin"][lang]: r["asin"],
        T["i_problem"][lang]: " · ".join(prob_map.get(x, x) for x in r["_issues"]),
    })
if issue_rows:
    issues_df = pd.DataFrame(issue_rows)
    st.dataframe(issues_df, use_container_width=True, hide_index=True)
else:
    st.success("✅ all clean")

st.divider()

st.markdown(f"### {T['shot_h'][lang]}")
st.caption(T["shot_cap"][lang])
_img = Path(__file__).parent.parent / "assets" / "catalog_monitor.png"
if _img.exists():
    st.image(str(_img), use_container_width=True)
else:
    st.info("📷 assets/catalog_monitor.png", icon="📷")

st.divider()

st.markdown(f"### {T['val_h'][lang]}")
st.write(T["val"][lang])

with st.expander(T["under_h"][lang]):
    st.write(T["under"][lang])
    st.code(
        "SELECT model, category, asin, asin_match, in_stock,\n"
        "       catalog_price, amazon_price,\n"
        "       catalog_coupon, amazon_coupon,\n"
        "       rating, old_rating\n"
        "FROM catalog_monitor\n"
        "ORDER BY category, model;",
        language="sql",
    )

st.info(T["nda"][lang], icon="🔒")
