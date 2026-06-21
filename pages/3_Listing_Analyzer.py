import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from i18n import lang_selector, get_lang

st.set_page_config(page_title="Listing Analyzer", page_icon="🔍", layout="wide")
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
    "title": {"EN": "🔍 Case: Amazon Listing Analyzer (product)", "RU": "🔍 Кейс: Amazon Listing Analyzer (продукт)", "UK": "🔍 Кейс: Amazon Listing Analyzer (продукт)"},
    "cap": {"EN": "Not a script, a finished product with a price. Demo data.", "RU": "Не скрипт, а законченный продукт с ценой. Демо-данные.", "UK": "Не скрипт, а завершений продукт з ціною. Демо-дані."},
    "what_h": {"EN": "What it is", "RU": "Что это", "UK": "Що це"},
    "what": {
        "EN": "A tool that takes an Amazon product link and produces a listing review: what's good, what's weak, what to fix first. Packaged as a pay-per-run product — the seller pays for a concrete result, no subscription.",
        "RU": "Инструмент, который берёт ссылку на товар Amazon и выдаёт разбор листинга: что хорошо, что слабо, что чинить в первую очередь. Упакован как продукт с оплатой за запуск — продавец платит за конкретный результат, без подписки.",
        "UK": "Інструмент, що бере посилання на товар Amazon і видає розбір лістингу: що добре, що слабко, що лагодити в першу чергу. Упакований як продукт з оплатою за запуск — продавець платить за конкретний результат, без підписки.",
    },
    "m_model": {"EN": "Model", "RU": "Модель", "UK": "Модель"},
    "m_price": {"EN": "Price per run", "RU": "Цена за запуск", "UK": "Ціна за запуск"},
    "m_time": {"EN": "Analysis time", "RU": "Время разбора", "UK": "Час розбору"},
    "checks_h": {"EN": "What it analyzes in a listing", "RU": "Что разбирает листинг", "UK": "Що розбирає лістинг"},
    "how_h": {"EN": "How it works — 3 steps", "RU": "Как работает — 3 шага", "UK": "Як працює — 3 кроки"},
    "s1_t": {"EN": "1️⃣ Paste the listing URL", "RU": "1️⃣ Вставь URL листинга", "UK": "1️⃣ Встав URL лістингу"},
    "s1_d": {"EN": "A link from Amazon.com / .de / .fr / .it — any marketplace. Up to 5 competitors can be added.", "RU": "Ссылку с Amazon.com / .de / .fr / .it — любой маркетплейс. Можно добавить до 5 конкурентов.", "UK": "Посилання з Amazon.com / .de / .fr / .it — будь-який маркетплейс. Можна додати до 5 конкурентів."},
    "s2_t": {"EN": "2️⃣ Run the analysis", "RU": "2️⃣ Запусти анализ", "UK": "2️⃣ Запусти аналіз"},
    "s2_d": {"EN": "AI analyzes photos, text, BSR, A+ and competitors. Full pass — 2-3 minutes.", "RU": "AI анализирует фото, текст, BSR, A+ и конкурентов. Полный анализ — 2-3 минуты.", "UK": "AI аналізує фото, текст, BSR, A+ і конкурентів. Повний аналіз — 2-3 хвилини."},
    "s3_t": {"EN": "3️⃣ Read the results", "RU": "3️⃣ Читай результаты", "UK": "3️⃣ Читай результати"},
    "s3_d": {"EN": "Overview → Health Score. Photos → Vision. COSMO/Rufus → AI visibility. Top niches → market.", "RU": "Обзор → Health Score. Фото → Vision. COSMO/Rufus → AI-видимость. Топ ниши → рынок.", "UK": "Огляд → Health Score. Фото → Vision. COSMO/Rufus → AI-видимість. Топ ніші → ринок."},
    "how_cap": {"EN": "Listing 3.0 — AI analysis on COSMO + Rufus + Vision.", "RU": "Listing 3.0 — AI-анализ на основе COSMO + Rufus + Vision.", "UK": "Listing 3.0 — AI-аналіз на основі COSMO + Rufus + Vision."},
    "top_h": {"EN": "🔥 Niche leaders — AI scan (demo)", "RU": "🔥 Топ ниши — AI-анализ лидеров (демо)", "UK": "🔥 Топ ніші — AI-аналіз лідерів (демо)"},
    "top_intro": {"EN": "Enter a niche query — the tool finds top sellers and shows what makes their listings win. Synthetic data, anonymized brands.", "RU": "Вводишь запрос ниши — инструмент находит топ-продавцов и показывает, что делает их листинги лучшими. Данные синтетические, бренды обезличены.", "UK": "Вводиш запит ніші — інструмент знаходить топ-продавців і показує, що робить їхні лістинги кращими. Дані синтетичні, бренди знеособлені."},
    "top_query": {"EN": "Example query:", "RU": "Пример запроса:", "UK": "Приклад запиту:"},
    "tm_comp": {"EN": "Competitors", "RU": "Конкурентов", "UK": "Конкурентів"},
    "tm_price": {"EN": "Avg price", "RU": "Средняя цена", "UK": "Середня ціна"},
    "tm_rating": {"EN": "Avg rating", "RU": "Ср. рейтинг", "UK": "Сер. рейтинг"},
    "tm_rev": {"EN": "Avg reviews", "RU": "Ср. отзывов", "UK": "Сер. відгуків"},
    "top_list_h": {"EN": "Top listings", "RU": "Топ листинги", "UK": "Топ лістинги"},
    "top_cap": {"EN": "Real search returns live data; brands here are anonymized for the demo.", "RU": "Реальный поиск выдаёт живые данные; бренды здесь обезличены для демо.", "UK": "Реальний пошук видає живі дані; бренди тут знеособлені для демо."},
    "out_h": {"EN": "Example output (demo)", "RU": "Пример вывода (демо)", "UK": "Приклад виводу (демо)"},
    "out_cap": {"EN": "Representative review of an anonymized product.", "RU": "Условный разбор обезличенного товара.", "UK": "Умовний розбір знеособленого товару."},
    "score": {"EN": "Overall listing score", "RU": "Общая оценка листинга", "UK": "Загальна оцінка лістингу"},
    "strong": {"EN": "✅ Strengths", "RU": "✅ Сильные стороны", "UK": "✅ Сильні сторони"},
    "fix": {"EN": "🔧 To fix", "RU": "🔧 Что чинить", "UK": "🔧 Що лагодити"},
    "strong_t": {
        "EN": "- 7 images, has infographics\n- Title within limit, with keywords\n- 4.5 rating with 800+ reviews",
        "RU": "- 7 изображений, есть инфографика\n- Заголовок в пределах лимита, с ключами\n- Рейтинг 4.5 при 800+ отзывах",
        "UK": "- 7 зображень, є інфографіка\n- Заголовок у межах ліміту, з ключами\n- Рейтинг 4.5 при 800+ відгуках",
    },
    "fix_t": {
        "EN": "- No A+ content — conversion lost\n- Bullets describe features, not benefits\n- No video in gallery",
        "RU": "- Нет A+ контента — упускается конверсия\n- Буллеты описывают свойства, не выгоды\n- Нет видео в галерее",
        "UK": "- Немає A+ контенту — втрачається конверсія\n- Булети описують властивості, не вигоди\n- Немає відео в галереї",
    },
    "prio": {"EN": "🎯 Priority #1", "RU": "🎯 Приоритет №1", "UK": "🎯 Пріоритет №1"},
    "prio_t": {"EN": "Add A+ content — the cheapest conversion lift for this listing.", "RU": "Добавить A+ контент — самый дешёвый рост конверсии для этого листинга.", "UK": "Додати A+ контент — найдешевше зростання конверсії для цього лістингу."},
    "why_h": {"EN": "Why this matters for business", "RU": "Почему это важно для бизнеса", "UK": "Чому це важливо для бізнесу"},
    "why": {
        "EN": "This is an example of a turnkey product: from idea to monetization. The seller gets concrete actions, not a table of metrics. For me — proof I can take a tool to the 'pay for result' stage, not just write code.",
        "RU": "Это пример продукта под ключ: от идеи до монетизации. Продавец получает конкретные действия, а не таблицу метрик. Для меня — доказательство, что умею доводить инструмент до состояния «платят за результат», а не просто пишу код.",
        "UK": "Це приклад продукту під ключ: від ідеї до монетизації. Продавець отримує конкретні дії, а не таблицю метрик. Для мене — доказ, що вмію доводити інструмент до стану «платять за результат», а не просто пишу код.",
    },
    "under_h": {"EN": "⚙️ Under the hood (for technical audience)", "RU": "⚙️ Под капотом (для технической аудитории)", "UK": "⚙️ Під капотом (для технічної аудиторії)"},
    "under": {"EN": "Parse product card, run through a rule set + LLM analysis to generate recommendations, package as an Apify Actor with pay-per-run.", "RU": "Парсинг карточки товара, прогон через набор правил + LLM-анализ для генерации рекомендаций, упаковка как Apify Actor с оплатой за запуск.", "UK": "Парсинг картки товару, прогін через набір правил + LLM-аналіз для генерації рекомендацій, упаковка як Apify Actor з оплатою за запуск."},
    "nda": {"EN": "Real rule logic and prompts — under NDA.", "RU": "Реальная логика правил и промпты — под NDA.", "UK": "Реальна логіка правил і промпти — під NDA."},
    "blk_title": {"EN": "Title", "RU": "Заголовок", "UK": "Заголовок"},
    "blk_title_d": {"EN": "Length, keywords, readability, banned words", "RU": "Длина, ключи, читабельность, запрещённые слова", "UK": "Довжина, ключі, читабельність, заборонені слова"},
    "blk_bul": {"EN": "Bullets", "RU": "Буллеты", "UK": "Булети"},
    "blk_bul_d": {"EN": "Benefit coverage, structure, keyword density", "RU": "Покрытие выгод, структура, плотность ключей", "UK": "Покриття вигод, структура, щільність ключів"},
    "blk_img": {"EN": "Images", "RU": "Изображения", "UK": "Зображення"},
    "blk_img_d": {"EN": "Count, infographics, lifestyle", "RU": "Количество, наличие инфографики, lifestyle", "UK": "Кількість, наявність інфографіки, lifestyle"},
    "blk_aplus": {"EN": "A+ content", "RU": "A+ контент", "UK": "A+ контент"},
    "blk_aplus_d": {"EN": "Present or not, block richness", "RU": "Есть/нет, насыщенность блоков", "UK": "Є/немає, насиченість блоків"},
    "blk_price": {"EN": "Price & Buy Box", "RU": "Цена и Buy Box", "UK": "Ціна та Buy Box"},
    "blk_price_d": {"EN": "Position vs category", "RU": "Позиция против категории", "UK": "Позиція проти категорії"},
    "blk_rev": {"EN": "Reviews", "RU": "Отзывы", "UK": "Відгуки"},
    "blk_rev_d": {"EN": "Rating, count, recency", "RU": "Рейтинг, количество, свежесть", "UK": "Рейтинг, кількість, свіжість"},
    "col_blk": {"EN": "Block", "RU": "Блок", "UK": "Блок"},
    "col_eval": {"EN": "What's evaluated", "RU": "Что оценивается", "UK": "Що оцінюється"},
}

st.title(T["title"][lang])
st.caption(T["cap"][lang])

st.markdown(f"### {T['what_h'][lang]}")
st.write(T["what"][lang])

c1, c2, c3 = st.columns(3)
c1.metric(T["m_model"][lang], "Pay-per-run")
c2.metric(T["m_price"][lang], "$2.99")
c3.metric(T["m_time"][lang], "< 1 min")

st.divider()

# ---------- Как работает: 3 шага ----------
st.markdown(f"### {T['how_h'][lang]}")

def step_card(title, body, accent):
    return (
        f"<div style='background:#1A1D24;border-top:3px solid {accent};"
        f"border-radius:8px;padding:16px 18px;height:100%'>"
        f"<div style='font-weight:700;font-size:1rem;margin-bottom:8px;color:#e2e8f0'>{title}</div>"
        f"<div style='font-size:0.88rem;color:#cbd5e1;line-height:1.6'>{body}</div></div>"
    )

sc1, sc2, sc3 = st.columns(3)
with sc1:
    st.markdown(step_card(T["s1_t"][lang], T["s1_d"][lang], "#4c8bf5"), unsafe_allow_html=True)
with sc2:
    st.markdown(step_card(T["s2_t"][lang], T["s2_d"][lang], "#16a34a"), unsafe_allow_html=True)
with sc3:
    st.markdown(step_card(T["s3_t"][lang], T["s3_d"][lang], "#8b5cf6"), unsafe_allow_html=True)

st.caption(T["how_cap"][lang])

_photo1 = Path(__file__).parent.parent / "assets" / "Photo1.png"
if _photo1.exists():
    st.image(str(_photo1), use_container_width=True)
else:
    st.info("📷 assets/Photo1.png", icon="📷")

st.divider()

# ---------- Топ ниши: AI-анализ лидеров (обезличенно) ----------
st.markdown(f"### {T['top_h'][lang]}")
st.write(T["top_intro"][lang])
st.markdown(f"**{T['top_query'][lang]}** `merino wool base layer`")

tk1, tk2, tk3, tk4 = st.columns(4)
tk1.metric(T["tm_comp"][lang], "12")
tk2.metric(T["tm_price"][lang], "$42")
tk3.metric(T["tm_rating"][lang], "4.5★")
tk4.metric(T["tm_rev"][lang], "249")

st.markdown(f"**{T['top_list_h'][lang]}**")
_img = Path(__file__).parent.parent / "assets" / "top_niche.png"
if _img.exists():
    st.image(str(_img), use_container_width=True)
else:
    st.info("📷 assets/top_niche.png", icon="📷")
st.caption(T["top_cap"][lang])

st.divider()

st.markdown(f"### {T['checks_h'][lang]}")
checks = pd.DataFrame([
    (T["blk_title"][lang], T["blk_title_d"][lang]),
    (T["blk_bul"][lang], T["blk_bul_d"][lang]),
    (T["blk_img"][lang], T["blk_img_d"][lang]),
    (T["blk_aplus"][lang], T["blk_aplus_d"][lang]),
    (T["blk_price"][lang], T["blk_price_d"][lang]),
    (T["blk_rev"][lang], T["blk_rev_d"][lang]),
], columns=[T["col_blk"][lang], T["col_eval"][lang]])
st.dataframe(checks, use_container_width=True, hide_index=True)

st.divider()

st.markdown(f"### {T['out_h'][lang]}")
st.caption(T["out_cap"][lang])
score = 72
st.markdown(f"**{T['score'][lang]}:** {score}/100")
st.progress(score / 100)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"#### {T['strong'][lang]}")
    st.write(T["strong_t"][lang])
with col2:
    st.markdown(f"#### {T['fix'][lang]}")
    st.write(T["fix_t"][lang])

st.markdown(f"#### {T['prio'][lang]}")
st.info(T["prio_t"][lang], icon="💡")

st.divider()

st.markdown(f"### {T['why_h'][lang]}")
st.write(T["why"][lang])

with st.expander(T["under_h"][lang]):
    st.write(T["under"][lang])
    st.code("url → scrape(listing) → rules_check() + llm_review()\n    → score + prioritized_actions → JSON", language="text")

st.info(T["nda"][lang], icon="🔒")
