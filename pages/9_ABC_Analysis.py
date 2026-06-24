import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from db import fetch_table, db_badge
from i18n import lang_selector, get_lang

st.set_page_config(page_title="ABC / XYZ Analysis", page_icon="🔠", layout="wide")
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
    "title": {"EN": "🔠 Case: ABC / XYZ assortment analysis", "RU": "🔠 Кейс: ABC / XYZ-анализ ассортимента", "UK": "🔠 Кейс: ABC / XYZ-аналіз асортименту"},
    "cap": {"EN": "I classify the whole catalog by value and demand stability to drive stock & focus decisions. Data anonymized/synthetic.", "RU": "Классифицирую весь каталог по ценности и стабильности спроса, чтобы управлять закупками и фокусом. Данные обезличены/синтетические.", "UK": "Класифікую весь каталог за цінністю та стабільністю попиту, щоб керувати закупівлями та фокусом. Дані знеособлені/синтетичні."},
    "task_h": {"EN": "Task", "RU": "Задача", "UK": "Задача"},
    "task": {
        "EN": "Hundreds of ASINs, finite money and attention. Treating every SKU equally is the most expensive mistake: you over-stock the tail and starve the winners, you chase margin on items that bring nothing. You need to know — objectively — which ASINs deserve money, which deserve watching, and which deserve cutting.",
        "RU": "Сотни ASIN, конечные деньги и внимание. Относиться ко всем SKU одинаково — самая дорогая ошибка: затовариваешь хвост и душишь лидеров, гоняешься за маржой на товарах, которые не приносят ничего. Нужно понимать — объективно — какие ASIN достойны денег, какие — наблюдения, а какие — вывода.",
        "UK": "Сотні ASIN, скінченні гроші та увага. Ставитися до всіх SKU однаково — найдорожча помилка: затоварюєш хвіст і душиш лідерів, женешся за маржею на товарах, що не приносять нічого. Треба розуміти — об'єктивно — які ASIN гідні грошей, які — спостереження, а які — виводу.",
    },
    "sol_h": {"EN": "Solution", "RU": "Решение", "UK": "Рішення"},
    "sol": {
        "EN": "Each ASIN gets two grades. ABC — its share of value (revenue, profit or tied-up stock; Pareto 80/15/5). XYZ — how stable its demand is (coefficient of variation of weekly sales). Crossed, they form a 9-cell matrix where every product has a clear management strategy: feed it, watch it, or cut it.",
        "RU": "Каждый ASIN получает две оценки. ABC — его доля в ценности (выручка, прибыль или замороженный сток; Парето 80/15/5). XYZ — насколько стабилен его спрос (коэффициент вариации недельных продаж). На пересечении — матрица 9 клеток, где у каждого товара есть чёткая стратегия управления: кормить, наблюдать или резать.",
        "UK": "Кожен ASIN отримує дві оцінки. ABC — його частка в цінності (виручка, прибуток або заморожений сток; Парето 80/15/5). XYZ — наскільки стабільний його попит (коефіцієнт варіації тижневих продажів). На перетині — матриця 9 клітин, де в кожного товару є чітка стратегія керування: годувати, спостерігати чи різати.",
    },
    "basis_h": {"EN": "ABC basis", "RU": "База ABC", "UK": "База ABC"},
    "basis_rev": {"EN": "Revenue", "RU": "Выручка", "UK": "Виручка"},
    "basis_profit": {"EN": "Profit", "RU": "Прибыль", "UK": "Прибуток"},
    "basis_stock": {"EN": "Stock value", "RU": "Стоимость стока", "UK": "Вартість стоку"},
    "basis_units": {"EN": "Units sold", "RU": "Продано штук", "UK": "Продано штук"},
    "kpi_h": {"EN": "Portfolio at a glance", "RU": "Портфель в цифрах", "UK": "Портфель у цифрах"},
    "kpi_total": {"EN": "ASINs", "RU": "ASIN", "UK": "ASIN"},
    "kpi_a": {"EN": "Group A (the money)", "RU": "Группа A (деньги)", "UK": "Група A (гроші)"},
    "kpi_a_help": {"EN": "share of catalog that makes ~80% of value", "RU": "доля каталога, дающая ~80% ценности", "UK": "частка каталогу, що дає ~80% цінності"},
    "kpi_c": {"EN": "Group C (the tail)", "RU": "Группа C (хвост)", "UK": "Група C (хвіст)"},
    "kpi_c_help": {"EN": "many SKUs, ~5% of value", "RU": "много SKU, ~5% ценности", "UK": "багато SKU, ~5% цінності"},
    "kpi_az": {"EN": "AZ — risky stars", "RU": "AZ — рисковые звёзды", "UK": "AZ — ризикові зірки"},
    "kpi_az_help": {"EN": "top value but volatile demand", "RU": "топ по ценности, но рваный спрос", "UK": "топ за цінністю, але рваний попит"},
    "pareto_h": {"EN": "Pareto curve — where the value sits", "RU": "Кривая Парето — где сидит ценность", "UK": "Крива Парето — де сидить цінність"},
    "pareto_cap": {"EN": "Cumulative share of value as ASINs are added from biggest to smallest. The 80% line shows your real core.", "RU": "Накопленная доля ценности по мере добавления ASIN от крупного к мелкому. Линия 80% — твоё реальное ядро.", "UK": "Накопичена частка цінності в міру додавання ASIN від великого до дрібного. Лінія 80% — твоє реальне ядро."},
    "matrix_h": {"EN": "ABC × XYZ matrix — strategy per cell", "RU": "Матрица ABC × XYZ — стратегия по клеткам", "UK": "Матриця ABC × XYZ — стратегія по клітинах"},
    "matrix_cap": {"EN": "Number = ASINs in the cell. Hover the strategy below.", "RU": "Число = ASIN в клетке. Стратегии — под таблицей.", "UK": "Число = ASIN у клітині. Стратегії — під таблицею."},
    "tbl_h": {"EN": "Full classification", "RU": "Полная классификация", "UK": "Повна класифікація"},
    "c_asin": {"EN": "ASIN", "RU": "ASIN", "UK": "ASIN"},
    "c_model": {"EN": "Model", "RU": "Модель", "UK": "Модель"},
    "c_rev": {"EN": "Revenue", "RU": "Выручка", "UK": "Виручка"},
    "c_share": {"EN": "Value share", "RU": "Доля ценности", "UK": "Частка цінності"},
    "c_cv": {"EN": "Demand CV", "RU": "CV спроса", "UK": "CV попиту"},
    "c_abc": {"EN": "ABC", "RU": "ABC", "UK": "ABC"},
    "c_xyz": {"EN": "XYZ", "RU": "XYZ", "UK": "XYZ"},
    "c_cell": {"EN": "Cell", "RU": "Клетка", "UK": "Клітина"},
    "strat_h": {"EN": "Assortment-management playbook", "RU": "Плейбук управления ассортиментом", "UK": "Плейбук керування асортиментом"},
    "shot_h": {"EN": "How it looks in Google Sheets", "RU": "Так это выглядит в Google Sheets", "UK": "Так це виглядає в Google Sheets"},
    "shot_cap": {"EN": "Real classification tool (brands and ASINs anonymized).", "RU": "Реальный инструмент классификации (бренды и ASIN обезличены).", "UK": "Реальний інструмент класифікації (бренди та ASIN знеособлені)."},
    "val_h": {"EN": "Business value", "RU": "Ценность для бизнеса", "UK": "Цінність для бізнесу"},
    "val": {
        "EN": "Money and stock follow value, not habit. Group-A winners never run out; the C-tail stops eating storage fees and cash; volatile Z-items get safety stock instead of blind reorders. One table turns 'we have too many SKUs' into a concrete cut-and-feed list.",
        "RU": "Деньги и сток идут за ценностью, а не за привычкой. Лидеры группы A не уходят в out-of-stock; хвост C перестаёт жрать складские сборы и кэш; рваные Z-товары получают страховой запас вместо слепых дозаказов. Одна таблица превращает «у нас слишком много SKU» в конкретный список — что резать, что кормить.",
        "UK": "Гроші та сток ідуть за цінністю, а не за звичкою. Лідери групи A не йдуть в out-of-stock; хвіст C перестає жерти складські збори та кеш; рвані Z-товари отримують страховий запас замість сліпих дозамовлень. Одна таблиця перетворює «у нас забагато SKU» на конкретний список — що різати, що годувати.",
    },
    "under_h": {"EN": "⚙️ Under the hood (for technical audience)", "RU": "⚙️ Под капотом (для технической аудитории)", "UK": "⚙️ Під капотом (для технічної аудиторії)"},
    "under": {"EN": "Sales facts come from the SP-API ETL (orders / settlements) in PostgreSQL. ABC: sort ASINs by chosen metric desc, take cumulative share, cut at 80% / 95% boundaries. XYZ: coefficient of variation (std/mean) of weekly units — X<0.10, Y<0.25, Z above. Cross-tab gives the 9-cell matrix; each cell maps to a fixed management rule. Dashboard reads the vitrine via st.secrets and lets the user switch the ABC basis (revenue / profit / stock value / units) live.", "RU": "Факты продаж берутся из SP-API ETL (orders / settlements) в PostgreSQL. ABC: сортируем ASIN по выбранной метрике по убыванию, считаем накопленную долю, режем по границам 80% / 95%. XYZ: коэффициент вариации (std/mean) недельных штук — X<0.10, Y<0.25, Z выше. Кросс-таблица даёт матрицу 9 клеток; каждой клетке соответствует фиксированное правило управления. Дашборд читает витрину через st.secrets и позволяет на лету переключать базу ABC (выручка / прибыль / стоимость стока / штуки).", "UK": "Факти продажів беруться зі SP-API ETL (orders / settlements) у PostgreSQL. ABC: сортуємо ASIN за обраною метрикою за спаданням, рахуємо накопичену частку, ріжемо по межах 80% / 95%. XYZ: коефіцієнт варіації (std/mean) тижневих штук — X<0.10, Y<0.25, Z вище. Крос-таблиця дає матрицю 9 клітин; кожній клітині відповідає фіксоване правило керування. Дашборд читає вітрину через st.secrets і дозволяє на льоту перемикати базу ABC (виручка / прибуток / вартість стоку / штуки)."},
    "nda": {"EN": "Real brands and ASINs — under NDA.", "RU": "Реальные бренды и ASIN — под NDA.", "UK": "Реальні бренди та ASIN — під NDA."},
}

# 9-cell playbook
PLAY = {
    "AX": {"EN": "**AX — cash cows.** Top value, predictable. Never let them go out of stock; automate reorder, lean safety stock, protect Buy Box & price.", "RU": "**AX — дойные коровы.** Топ ценности, предсказуемы. Никогда не допускать out-of-stock; авто-дозаказ, минимальный страховой запас, защищать Buy Box и цену.", "UK": "**AX — дійні корови.** Топ цінності, передбачувані. Ніколи не допускати out-of-stock; авто-дозамовлення, мінімальний страховий запас, захищати Buy Box і ціну."},
    "AY": {"EN": "**AY — important but wavy.** Big value, moderate swings. Hold a bigger safety stock, forecast with seasonality, watch weekly.", "RU": "**AY — важные, но волнистые.** Большая ценность, средние колебания. Держать повышенный страховой запас, прогноз с сезонностью, контроль еженедельно.", "UK": "**AY — важливі, але хвилясті.** Велика цінність, середні коливання. Тримати підвищений страховий запас, прогноз із сезонністю, контроль щотижня."},
    "AZ": {"EN": "**AZ — risky stars.** High value, erratic demand. The dangerous cell: big money on unpredictable items. Generous safety stock, manual review, investigate the volatility (promo-driven? one big buyer?).", "RU": "**AZ — рисковые звёзды.** Высокая ценность, рваный спрос. Опасная клетка: большие деньги на непредсказуемых товарах. Щедрый страховой запас, ручной разбор, искать причину рваности (промо? один крупный покупатель?).", "UK": "**AZ — ризикові зірки.** Висока цінність, рваний попит. Небезпечна клітина: великі гроші на непередбачуваних товарах. Щедрий страховий запас, ручний розбір, шукати причину рваності (промо? один великий покупець?)."},
    "BX": {"EN": "**BX — stable mid-tier.** Reliable workhorses. Standard automated reorder, modest safety stock, low attention needed.", "RU": "**BX — стабильный середняк.** Надёжные рабочие лошадки. Стандартный авто-дозаказ, умеренный страховой запас, внимания почти не требуют.", "UK": "**BX — стабільний середняк.** Надійні робочі конячки. Стандартне авто-дозамовлення, помірний страховий запас, уваги майже не потребують."},
    "BY": {"EN": "**BY — average all round.** Moderate value & swings. Keep standard rules, review monthly, candidate for promo to push into A.", "RU": "**BY — средние во всём.** Умеренная ценность и колебания. Стандартные правила, обзор раз в месяц, кандидат на промо для перевода в A.", "UK": "**BY — середні в усьому.** Помірна цінність і коливання. Стандартні правила, огляд раз на місяць, кандидат на промо для переведення в A."},
    "BZ": {"EN": "**BZ — unstable mid.** OK value, jumpy demand. Order to demand (don't pre-stock heavily), watch for dead stock.", "RU": "**BZ — нестабильный середняк.** Норм ценность, прыгающий спрос. Заказывать под спрос (не затоваривать заранее), следить за зависанием стока.", "UK": "**BZ — нестабільний середняк.** Норм цінність, стрибаючий попит. Замовляти під попит (не затоварювати заздалегідь), стежити за зависанням стоку."},
    "CX": {"EN": "**CX — small but steady.** Low value, predictable. Keep minimal stock, automate fully, near-zero attention.", "RU": "**CX — мелкие, но ровные.** Низкая ценность, предсказуемы. Минимальный сток, полная автоматизация, внимания почти ноль.", "UK": "**CX — дрібні, але рівні.** Низька цінність, передбачувані. Мінімальний сток, повна автоматизація, уваги майже нуль."},
    "CY": {"EN": "**CY — minor & wavy.** Low value, some swings. Order on demand only; review for delisting if it stalls.", "RU": "**CY — мелкие и волнистые.** Низкая ценность, есть колебания. Заказывать только под спрос; кандидат на снятие, если буксует.", "UK": "**CY — дрібні та хвилясті.** Низька цінність, є коливання. Замовляти лише під попит; кандидат на зняття, якщо буксує."},
    "CZ": {"EN": "**CZ — the cut list.** Low value, unpredictable. Prime candidates to discontinue or liquidate — they tie up cash and storage for almost nothing. Keep only if strategic (bundle, brand width).", "RU": "**CZ — список на вывод.** Низкая ценность, непредсказуемы. Первые кандидаты на снятие/распродажу — морозят кэш и склад почти ни за что. Оставлять только если стратегически нужны (бандл, ширина бренда).", "UK": "**CZ — список на вивід.** Низька цінність, непередбачувані. Перші кандидати на зняття/розпродаж — морозять кеш і склад майже ні за що. Лишати тільки якщо стратегічно потрібні (бандл, ширина бренда)."},
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
    n = 60
    rows = []
    for i in range(n):
        # heavy-tailed revenue (few big, many small)
        base_units_week = max(1.0, rng.lognormal(mean=2.6, sigma=1.1))
        price = round(float(rng.uniform(20, 95)), 2)
        margin_pct = float(rng.uniform(0.08, 0.42))
        # weekly units over 12 weeks with item-specific volatility
        vol = float(rng.uniform(0.04, 0.55))
        weeks = np.maximum(0, rng.normal(base_units_week, base_units_week * vol, 12))
        units = float(weeks.sum())
        revenue = units * price
        profit = revenue * margin_pct
        on_hand = float(rng.integers(0, 400))
        stock_value = on_hand * price * (1 - margin_pct)
        mean_w = weeks.mean() if weeks.mean() > 0 else 1e-9
        cv = float(weeks.std() / mean_w)
        asin = "B0" + "".join(rng.choice(list("0123456789ABCDEFGHJKLMNPQRSTUVWXYZ"), 8))
        rows.append({
            "asin": asin,
            "model": f"SKU-{i+1:03d}",
            "revenue": round(revenue, 2),
            "profit": round(profit, 2),
            "stock_value": round(stock_value, 2),
            "units": round(units, 0),
            "demand_cv": round(cv, 3),
        })
    return pd.DataFrame(rows)


raw = fetch_table(
    "abc_xyz_analysis",
    "asin, model, revenue, profit, stock_value, units, demand_cv",
)
is_live = raw is not None and not raw.empty
if not is_live:
    raw = synthetic()

db_badge(is_live)

basis_options = {
    T["basis_rev"][lang]: "revenue",
    T["basis_profit"][lang]: "profit",
    T["basis_stock"][lang]: "stock_value",
    T["basis_units"][lang]: "units",
}
basis_label = st.selectbox(T["basis_h"][lang], list(basis_options.keys()))
metric = basis_options[basis_label]

df = raw.copy()
df = df[df[metric] > 0].copy()
df = df.sort_values(metric, ascending=False).reset_index(drop=True)

total_val = df[metric].sum()
df["value_share"] = df[metric] / total_val
df["cum_share"] = df["value_share"].cumsum()


def abc_of(cum):
    if cum <= 0.80:
        return "A"
    if cum <= 0.95:
        return "B"
    return "C"


df["ABC"] = df["cum_share"].apply(abc_of)


def xyz_of(cv):
    if cv < 0.10:
        return "X"
    if cv < 0.25:
        return "Y"
    return "Z"


df["XYZ"] = df["demand_cv"].apply(xyz_of)
df["cell"] = df["ABC"] + df["XYZ"]

# ── KPIs ──────────────────────────────────────────────
total = len(df)
n_a = int((df["ABC"] == "A").sum())
n_c = int((df["ABC"] == "C").sum())
n_az = int((df["cell"] == "AZ").sum())

st.markdown(f"### {T['kpi_h'][lang]}")
k1, k2, k3, k4 = st.columns(4)
k1.metric(T["kpi_total"][lang], total)
k2.metric(T["kpi_a"][lang], f"{n_a} · {n_a/total*100:.0f}%", help=T["kpi_a_help"][lang])
k3.metric(T["kpi_c"][lang], f"{n_c} · {n_c/total*100:.0f}%", help=T["kpi_c_help"][lang])
k4.metric(T["kpi_az"][lang], n_az, help=T["kpi_az_help"][lang])

st.divider()

# ── Pareto ────────────────────────────────────────────
st.markdown(f"### {T['pareto_h'][lang]}")
st.caption(T["pareto_cap"][lang])
pareto = pd.DataFrame({
    "rank": range(1, total + 1),
    "cum_pct": (df["cum_share"] * 100).values,
})
st.line_chart(pareto.set_index("rank"), height=280, use_container_width=True)

st.divider()

# ── ABC×XYZ matrix ────────────────────────────────────
st.markdown(f"### {T['matrix_h'][lang]}")
st.caption(T["matrix_cap"][lang])

mat = pd.crosstab(df["ABC"], df["XYZ"])
for r in ["A", "B", "C"]:
    if r not in mat.index:
        mat.loc[r] = 0
for c in ["X", "Y", "Z"]:
    if c not in mat.columns:
        mat[c] = 0
mat = mat.loc[["A", "B", "C"], ["X", "Y", "Z"]]

# color: green good (AX), red dangerous (CZ), via simple rule
CELL_COLOR = {
    "AX": "#1d9e75", "AY": "#3a9d6e", "AZ": "#d85a30",
    "BX": "#5a8f6a", "BY": "#9a9a55", "BZ": "#c77a3a",
    "CX": "#6e7d63", "CY": "#b08a45", "CZ": "#b03030",
}


def color_matrix(data):
    styles = pd.DataFrame("", index=data.index, columns=data.columns)
    for r in data.index:
        for c in data.columns:
            styles.loc[r, c] = f"background-color: {CELL_COLOR.get(r+c, '#444')}; color: #ffffff; text-align:center; font-weight:600"
    return styles


st.dataframe(
    mat.style.apply(color_matrix, axis=None).format("{:d}"),
    use_container_width=True,
)

st.divider()

# ── Full table ────────────────────────────────────────
st.markdown(f"### {T['tbl_h'][lang]}")
view = pd.DataFrame({
    T["c_asin"][lang]: df["asin"],
    T["c_model"][lang]: df["model"],
    T["c_rev"][lang]: df[metric],
    T["c_share"][lang]: df["value_share"] * 100,
    T["c_cv"][lang]: df["demand_cv"],
    T["c_abc"][lang]: df["ABC"],
    T["c_xyz"][lang]: df["XYZ"],
    T["c_cell"][lang]: df["cell"],
}).reset_index(drop=True)

cell_series = view[T["c_cell"][lang]]


def style_full(row):
    styles = [""] * len(row)
    cols = list(row.index)
    cell = cell_series.iloc[row.name]
    col = CELL_COLOR.get(cell, "#444")
    styles[cols.index(T["c_cell"][lang])] = f"background-color: {col}; color:#fff; font-weight:600; text-align:center"
    abc = row[T["c_abc"][lang]]
    abc_col = {"A": "#1d9e75", "B": "#9a9a55", "C": "#b03030"}.get(abc, "")
    if abc_col:
        styles[cols.index(T["c_abc"][lang])] = f"background-color:{abc_col}; color:#fff; text-align:center"
    return styles


styled = view.style.apply(style_full, axis=1).format({
    T["c_rev"][lang]: "${:,.0f}" if metric != "units" else "{:,.0f}",
    T["c_share"][lang]: "{:.1f}%",
    T["c_cv"][lang]: "{:.2f}",
})
st.dataframe(styled, use_container_width=True, hide_index=True)

st.divider()

# ── Playbook ──────────────────────────────────────────
st.markdown(f"### {T['strat_h'][lang]}")
order = ["AX", "AY", "AZ", "BX", "BY", "BZ", "CX", "CY", "CZ"]
cols = st.columns(3)
for idx, cell in enumerate(order):
    with cols[idx % 3]:
        st.markdown(
            f"<div style='background:#1e1e2e;border-left:4px solid {CELL_COLOR[cell]};"
            f"border-radius:8px;padding:10px 14px;margin-bottom:10px;min-height:150px'>"
            f"<div style='color:{CELL_COLOR[cell]};font-weight:700;font-size:15px;margin-bottom:4px'>{cell}</div>"
            f"<div style='color:#ccc;font-size:13px;line-height:1.45'>"
            f"{PLAY[cell][lang].replace('**','')}</div></div>",
            unsafe_allow_html=True,
        )

st.divider()

st.markdown(f"### {T['shot_h'][lang]}")
st.caption(T["shot_cap"][lang])
_img = Path(__file__).parent.parent / "assets" / "abc_xyz.png"
if _img.exists():
    st.image(str(_img), use_container_width=True)
else:
    st.info("📷 assets/abc_xyz.png", icon="📷")

st.divider()

st.markdown(f"### {T['val_h'][lang]}")
st.write(T["val"][lang])

with st.expander(T["under_h"][lang]):
    st.write(T["under"][lang])
    st.code(
        "WITH ranked AS (\n"
        "  SELECT asin, model, revenue, profit, stock_value, units, demand_cv,\n"
        "         SUM(revenue) OVER (ORDER BY revenue DESC)\n"
        "           / SUM(revenue) OVER () AS cum_share\n"
        "  FROM abc_xyz_analysis\n"
        ")\n"
        "SELECT *,\n"
        "  CASE WHEN cum_share <= 0.80 THEN 'A'\n"
        "       WHEN cum_share <= 0.95 THEN 'B' ELSE 'C' END AS abc,\n"
        "  CASE WHEN demand_cv < 0.10 THEN 'X'\n"
        "       WHEN demand_cv < 0.25 THEN 'Y' ELSE 'Z' END AS xyz\n"
        "FROM ranked\n"
        "ORDER BY revenue DESC;",
        language="sql",
    )

st.info(T["nda"][lang], icon="🔒")
