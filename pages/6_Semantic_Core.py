import streamlit as st
import pandas as pd
import re
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from i18n import lang_selector, get_lang

st.set_page_config(page_title="Semantic Core", page_icon="🧩", layout="wide")
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
    "title": {"EN": "🧩 Case: Semantic Core Automation", "RU": "🧩 Кейс: Semantic Core Automation", "UK": "🧩 Кейс: Semantic Core Automation"},
    "cap": {"EN": "Automating SEO/PPC keyword processing in Google Sheets. Data anonymized.", "RU": "Автоматизация обработки SEO/PPC-ключевиков в Google Sheets. Данные обезличены.", "UK": "Автоматизація обробки SEO/PPC-ключовиків у Google Sheets. Дані знеособлені."},
    "task_h": {"EN": "Task", "RU": "Задача", "UK": "Задача"},
    "task": {
        "EN": "Launching ads on a marketplace gathers thousands of key phrases. They need manual cleaning: removing duplicates, cutting negatives, checking brands and SKUs. Hours of monotonous work with risk of errors.",
        "RU": "При запуске рекламы на маркетплейсе собираются тысячи ключевых фраз. Их нужно чистить вручную: убирать дубли, отсекать негативные слова, проверять бренды и артикулы. Это часы монотонной работы с риском ошибок.",
        "UK": "При запуску реклами на маркетплейсі збираються тисячі ключових фраз. Їх треба чистити вручну: прибирати дублі, відсікати негативні слова, перевіряти бренди та артикули. Це години монотонної роботи з ризиком помилок.",
    },
    "sol_h": {"EN": "Solution", "RU": "Решение", "UK": "Рішення"},
    "sol": {
        "EN": "A script right in Google Sheets (Apps Script) with a menu of checks. One button — and the table is highlighted by color: duplicates, negatives, brand and SKU matches. Smart normalization: `belts = belt`, `041-6400 = 041 6400`, case-insensitive.",
        "RU": "Скрипт прямо в Google Sheets (Apps Script) с меню из проверок. Одна кнопка — и таблица подсвечивается цветом: дубли, негативы, совпадения по бренду и артикулам. Умная нормализация: `belts = belt`, `041-6400 = 041 6400`, регистр игнорируется.",
        "UK": "Скрипт прямо в Google Sheets (Apps Script) з меню з перевірок. Одна кнопка — і таблиця підсвічується кольором: дублі, негативи, збіги за брендом і артикулами. Розумна нормалізація: `belts = belt`, `041-6400 = 041 6400`, регістр ігнорується.",
    },
    "checks_h": {"EN": "Checks (as in the real tool)", "RU": "Проверки (как в реальном инструменте)", "UK": "Перевірки (як у реальному інструменті)"},
    "ch1": {"EN": "🟡 Duplicates", "RU": "🟡 Дубли", "UK": "🟡 Дублі"},
    "ch1d": {"EN": "Finds repeats with word form and hyphen awareness", "RU": "Находит повторы фраз с учётом форм слова и дефисов", "UK": "Знаходить повтори фраз з урахуванням форм слова та дефісів"},
    "ch2": {"EN": "🔴 Negatives", "RU": "🔴 Негативы", "UK": "🔴 Негативи"},
    "ch2d": {"EN": "Cuts phrases with minus-words (phrase / exact / models)", "RU": "Отсекает фразы с минус-словами (phrase / exact / модели)", "UK": "Відсікає фрази з мінус-словами (phrase / exact / моделі)"},
    "ch3": {"EN": "🟢 MPT / ASIN", "RU": "🟢 MPT / ASIN", "UK": "🟢 MPT / ASIN"},
    "ch3d": {"EN": "Validates product codes against a list", "RU": "Проверяет валидные коды товаров по списку", "UK": "Перевіряє валідні коди товарів за списком"},
    "ch4": {"EN": "🔵 Brand", "RU": "🔵 Бренд", "UK": "🔵 Бренд"},
    "ch4d": {"EN": "Highlights mentions of your brand", "RU": "Подсвечивает упоминания своего бренда", "UK": "Підсвічує згадки свого бренду"},
    "ch5": {"EN": "🟠 Duplicate + negative", "RU": "🟠 Дубль + негатив", "UK": "🟠 Дубль + негатив"},
    "ch5d": {"EN": "Double match — priority for removal", "RU": "Двойное совпадение — приоритет на удаление", "UK": "Подвійний збіг — пріоритет на видалення"},
    "col_check": {"EN": "Check", "RU": "Проверка", "UK": "Перевірка"},
    "col_does": {"EN": "What it does", "RU": "Что делает", "UK": "Що робить"},
    "demo_h": {"EN": "Interactive demo", "RU": "Интерактивное демо", "UK": "Інтерактивне демо"},
    "demo_cap": {"EN": "Enter keywords (one per line) — see how the script marks them.", "RU": "Введи ключевики (по одному в строке) — увидишь, как скрипт их разметит.", "UK": "Введи ключовики (по одному в рядку) — побачиш, як скрипт їх розмітить."},
    "kw_lbl": {"EN": "Keywords", "RU": "Ключевики", "UK": "Ключовики"},
    "neg_lbl": {"EN": "Minus-words", "RU": "Минус-слова", "UK": "Мінус-слова"},
    "brand_lbl": {"EN": "Your brand", "RU": "Свой бренд", "UK": "Свій бренд"},
    "kw_col": {"EN": "Keyword", "RU": "Ключевик", "UK": "Ключовик"},
    "norm_col": {"EN": "Normalized", "RU": "Нормализовано", "UK": "Нормалізовано"},
    "dup_col": {"EN": "Duplicate", "RU": "Дубль", "UK": "Дубль"},
    "neg_col": {"EN": "Negative", "RU": "Негатив", "UK": "Негатив"},
    "brand_col": {"EN": "Brand", "RU": "Бренд", "UK": "Бренд"},
    "res_t": {"EN": "Markup result:", "RU": "Результат разметки:", "UK": "Результат розмітки:"},
    "m_dup": {"EN": "🟡 Duplicates", "RU": "🟡 Дублей", "UK": "🟡 Дублів"},
    "m_neg": {"EN": "🔴 Negatives", "RU": "🔴 Негативов", "UK": "🔴 Негативів"},
    "m_brand": {"EN": "🔵 Brand", "RU": "🔵 Бренд", "UK": "🔵 Бренд"},
    "shot_h": {"EN": "How it works in Google Sheets", "RU": "Так это работает в Google Sheets", "UK": "Так це працює в Google Sheets"},
    "shot_cap": {"EN": "Real tool with checks menu (brands/SKUs anonymized).", "RU": "Реальный инструмент с меню проверок (бренды/артикулы замазаны).", "UK": "Реальний інструмент з меню перевірок (бренди/артикули замазані)."},
    "val_h": {"EN": "Business value", "RU": "Ценность для бизнеса", "UK": "Цінність для бізнесу"},
    "val": {
        "EN": "Hours of manual keyword cleaning turn into one click. Fewer errors, cleaner semantics, faster ad launch. The tool lives where the team works — right in Google Sheets, no separate software.",
        "RU": "Часы ручной чистки ключевиков превращаются в один клик. Меньше ошибок, чище семантика, быстрее запуск рекламы. Инструмент живёт там, где работает команда — прямо в Google Sheets, без отдельного софта.",
        "UK": "Години ручної чистки ключовиків перетворюються на один клік. Менше помилок, чистіша семантика, швидший запуск реклами. Інструмент живе там, де працює команда — прямо в Google Sheets, без окремого софту.",
    },
    "under_h": {"EN": "⚙️ Under the hood (for technical audience)", "RU": "⚙️ Под капотом (для технической аудитории)", "UK": "⚙️ Під капотом (для технічної аудиторії)"},
    "under": {"EN": "Google Apps Script (JavaScript): custom menu via onOpen, word-form normalization (singular stemming, hyphens, special chars), phrase and exact negative matching, ASIN regex validation, conditional cell formatting.", "RU": "Google Apps Script (JavaScript): кастомное меню через onOpen, нормализация форм слова (стемминг ед. числа, дефисы, спецсимволы), фразовый и точный матчинг негативов, валидация ASIN по regex, условное форматирование ячеек цветом.", "UK": "Google Apps Script (JavaScript): кастомне меню через onOpen, нормалізація форм слова (стемінг одн. числа, дефіси, спецсимволи), фразовий і точний матчинг негативів, валідація ASIN по regex, умовне форматування клітинок кольором."},
    "nda": {"EN": "Real brands, SKUs and niche — under NDA.", "RU": "Реальные бренды, артикулы и ниша — под NDA.", "UK": "Реальні бренди, артикули і ніша — під NDA."},
}

st.title(T["title"][lang])
st.caption(T["cap"][lang])

st.markdown(f"### {T['task_h'][lang]}")
st.write(T["task"][lang])
st.markdown(f"### {T['sol_h'][lang]}")
st.write(T["sol"][lang])

st.divider()

st.markdown(f"### {T['checks_h'][lang]}")
checks = pd.DataFrame([
    (T["ch1"][lang], T["ch1d"][lang]), (T["ch2"][lang], T["ch2d"][lang]),
    (T["ch3"][lang], T["ch3d"][lang]), (T["ch4"][lang], T["ch4d"][lang]),
    (T["ch5"][lang], T["ch5d"][lang]),
], columns=[T["col_check"][lang], T["col_does"][lang]])
st.dataframe(checks, use_container_width=True, hide_index=True)

st.divider()

st.markdown(f"### {T['demo_h'][lang]}")
st.caption(T["demo_cap"][lang])

default_kw = "pulley belt\npulley belts\ndeck belt 12345\ndeck belt 12-345\nbrand-x pulley\ngardenpro spindle\ngardenpro spindles\nmower blade negative cheap\nspindle assembly\nspindle assembly"

col_in, col_neg = st.columns([2, 1])
with col_in:
    kw_text = st.text_area(T["kw_lbl"][lang], default_kw, height=220)
with col_neg:
    neg_text = st.text_area(T["neg_lbl"][lang], "cheap\nused\nfake", height=100)
    brand = st.text_input(T["brand_lbl"][lang], "gardenpro")

def to_singular(text):
    s = str(text).lower().strip()
    s = re.sub(r"[-+]", " ", s)
    s = re.sub(r"[/\\]", " ", s)
    s = re.sub(r'[|*"#,.:]', "", s)
    s = re.sub(r"\s+", " ", s).strip()
    words = []
    for w in s.split(" "):
        words.append(w[:-1] if len(w) > 3 and w.endswith("s") else w)
    return " ".join(words)

keywords = [k.strip() for k in kw_text.splitlines() if k.strip()]
negatives = [to_singular(n) for n in neg_text.splitlines() if n.strip()]
brand_norm = brand.lower().strip()

seen = {}
results = []
for kw in keywords:
    norm = to_singular(kw)
    is_dup = norm in seen
    seen[norm] = seen.get(norm, 0) + 1
    is_neg = any(f" {neg} " in f" {norm} " for neg in negatives)
    is_brand = bool(brand_norm) and bool(re.search(rf"\b{re.escape(brand_norm)}", norm))
    results.append({"kw": kw, "norm": norm, "dup": is_dup, "neg": is_neg, "brand": is_brand})

df = pd.DataFrame(results)
df.columns = [T["kw_col"][lang], T["norm_col"][lang], T["dup_col"][lang], T["neg_col"][lang], T["brand_col"][lang]]

def color_row(row):
    dup, neg, br = row[T["dup_col"][lang]], row[T["neg_col"][lang]], row[T["brand_col"][lang]]
    if dup and neg: bg = "#d85a30"
    elif neg: bg = "#a32d2d"
    elif dup: bg = "#854f0b"
    elif br: bg = "#185fa5"
    else: bg = ""
    style = f"background-color: {bg}; color: #fff" if bg else ""
    return [style] * len(row)

st.markdown(f"**{T['res_t'][lang]}**")
st.dataframe(df.style.apply(color_row, axis=1), use_container_width=True, hide_index=True)

c1, c2, c3 = st.columns(3)
c1.metric(T["m_dup"][lang], int(df[T["dup_col"][lang]].astype(int).sum()))
c2.metric(T["m_neg"][lang], int(df[T["neg_col"][lang]].astype(int).sum()))
c3.metric(T["m_brand"][lang], int(df[T["brand_col"][lang]].astype(int).sum()))

st.divider()

st.markdown(f"### {T['shot_h'][lang]}")
st.caption(T["shot_cap"][lang])
_img = Path(__file__).parent.parent / "assets" / "semantic_core.png"
if _img.exists():
    st.image(str(_img), use_container_width=True)
else:
    st.info("📷 assets/semantic_core.png", icon="📷")

st.divider()

st.markdown(f"### {T['val_h'][lang]}")
st.write(T["val"][lang])

with st.expander(T["under_h"][lang]):
    st.write(T["under"][lang])
    st.code("function toSingular_(text) {\n  let s = text.toLowerCase().replace(/[-+]/g,' ');\n  return s.split(' ').map(w =>\n    w.length>3 && w.endsWith('s') ? w.slice(0,-1) : w\n  ).join(' ');\n}", language="javascript")

st.info(T["nda"][lang], icon="🔒")
