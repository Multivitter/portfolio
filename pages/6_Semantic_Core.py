import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Semantic Core", page_icon="🧩", layout="wide")

st.title("🧩 Кейс: Semantic Core Automation")
st.caption("Автоматизация обработки SEO/PPC-ключевиков в Google Sheets. Данные обезличены.")

# ---------- Задача ----------
st.markdown("### Задача")
st.write(
    "При запуске рекламы на маркетплейсе собираются тысячи ключевых фраз. "
    "Их нужно чистить вручную: убирать дубли, отсекать негативные слова, "
    "проверять бренды и артикулы. Это часы монотонной работы с риском ошибок."
)

st.markdown("### Решение")
st.write(
    "Скрипт прямо в Google Sheets (Apps Script) с меню из проверок. "
    "Одна кнопка — и таблица подсвечивается цветом: дубли, негативы, "
    "совпадения по бренду и артикулам. Умная нормализация: "
    "`belts = belt`, `041-6400 = 041 6400`, регистр игнорируется."
)

st.divider()

# ---------- Что делает ----------
st.markdown("### Проверки (как в реальном инструменте)")
checks = pd.DataFrame([
    ("🟡 Дубли", "Находит повторы фраз с учётом форм слова и дефисов"),
    ("🔴 Негативы", "Отсекает фразы с минус-словами (phrase / exact / модели)"),
    ("🟢 MPT / ASIN", "Проверяет валидные коды товаров по списку"),
    ("🔵 Бренд", "Подсвечивает упоминания своего бренда"),
    ("🟠 Дубль + негатив", "Двойное совпадение — приоритет на удаление"),
], columns=["Проверка", "Что делает"])
st.dataframe(checks, use_container_width=True, hide_index=True)

st.divider()

# ---------- Интерактивное демо ----------
st.markdown("### Интерактивное демо")
st.caption("Введи ключевики (по одному в строке) — увидишь, как скрипт их разметит.")

default_kw = """pulley belt
pulley belts
deck belt 12345
deck belt 12-345
brand-x pulley
gardenpro spindle
gardenpro spindles
mower blade negative cheap
spindle assembly
spindle assembly"""

col_in, col_neg = st.columns([2, 1])
with col_in:
    kw_text = st.text_area("Ключевики", default_kw, height=220)
with col_neg:
    neg_text = st.text_area("Минус-слова", "cheap\nused\nfake", height=100)
    brand = st.text_input("Свой бренд", "gardenpro")

# ---------- Логика (порт из Apps Script) ----------
def to_singular(text):
    s = str(text).lower().strip()
    s = re.sub(r"[-+]", " ", s)
    s = re.sub(r"[/\\]", " ", s)
    s = re.sub(r'[|*"#,.:]', "", s)
    s = re.sub(r"\s+", " ", s).strip()
    words = []
    for w in s.split(" "):
        if len(w) > 3 and w.endswith("s"):
            words.append(w[:-1])
        else:
            words.append(w)
    return " ".join(words)

keywords = [k.strip() for k in kw_text.splitlines() if k.strip()]
negatives = [to_singular(n) for n in neg_text.splitlines() if n.strip()]
brand_norm = brand.lower().strip()

# разметка
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
df.columns = ["Ключевик", "Нормализовано", "Дубль", "Негатив", "Бренд"]

def color_row(row):
    if row["Дубль"] and row["Негатив"]:
        bg = "#d85a30"   # оранжевый — дубль+негатив
    elif row["Негатив"]:
        bg = "#a32d2d"   # красный
    elif row["Дубль"]:
        bg = "#854f0b"   # жёлтый (тёмный для контраста)
    elif row["Бренд"]:
        bg = "#185fa5"   # синий
    else:
        bg = ""
    style = f"background-color: {bg}; color: #fff" if bg else ""
    return [style] * len(row)

st.markdown("**Результат разметки:**")
st.dataframe(
    df.style.apply(color_row, axis=1),
    use_container_width=True, hide_index=True,
)

# сводка
c1, c2, c3 = st.columns(3)
c1.metric("🟡 Дублей", int(df["Дубль"].astype(int).sum()))
c2.metric("🔴 Негативов", int(df["Негатив"].astype(int).sum()))
c3.metric("🔵 Бренд", int(df["Бренд"].astype(int).sum()))

st.divider()

# ---------- Скриншот реального инструмента ----------
st.markdown("### Так это работает в Google Sheets")
st.caption("Реальный инструмент с меню проверок (бренды/артикулы замазаны).")

from pathlib import Path
_img = Path(__file__).parent.parent / "assets" / "semantic_core.png"
if _img.exists():
    st.image(str(_img), use_container_width=True)
else:
    st.info("📷 Сюда добавь скриншот реального инструмента: assets/semantic_core.png (замажь бренды и артикулы перед загрузкой).")

st.divider()

# ---------- Ценность ----------
st.markdown("### Ценность для бизнеса")
st.write(
    "Часы ручной чистки ключевиков превращаются в один клик. "
    "Меньше ошибок, чище семантика, быстрее запуск рекламы. "
    "Инструмент живёт там, где работает команда — прямо в Google Sheets, "
    "без отдельного софта."
)

with st.expander("⚙️ Под капотом (для технической аудитории)"):
    st.write(
        "Google Apps Script (JavaScript): кастомное меню через onOpen, "
        "нормализация форм слова (стемминг ед. числа, дефисы, спецсимволы), "
        "фразовый и точный матчинг негативов, валидация ASIN по regex, "
        "условное форматирование ячеек цветом."
    )
    st.code(
        "// Нормализация: belts→belt, 041-6400→041 6400\n"
        "function toSingular_(text) {\n"
        "  let s = text.toLowerCase().replace(/[-+]/g,' ');\n"
        "  return s.split(' ').map(w =>\n"
        "    w.length>3 && w.endsWith('s') ? w.slice(0,-1) : w\n"
        "  ).join(' ');\n"
        "}",
        language="javascript",
    )

st.info("Реальные бренды, артикулы и ниша — под NDA.", icon="🔒")
