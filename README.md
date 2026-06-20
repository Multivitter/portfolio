# portfolio
Архитектор данных для e-commerce: Amazon · Walmart · Shopify · Weather → PostgreSQL → BI · AI-агенты. Интерактивные кейсы на Streamlit.
# 📊 Data Architecture Portfolio

> Проектирую и строю системы данных для e-commerce-бизнеса:
> от сырых API маркетплейсов до дашбордов, по которым принимают решения.

**Amazon · Walmart · Shopify · Weather → PostgreSQL → BI · AI-агенты**

🔗 **Live demo:** https://your-app.streamlit.app

---

## Что я делаю для бизнеса

Превращаю разрозненные данные в единую систему, которая работает сама:

- **Собираю данные** со всех площадок (SP-API, Advertising API, Walmart, Shopify) в одно хранилище.
- **Автоматизирую** — ~50 задач по расписанию, 24/7, без ручных выгрузок.
- **Слежу за надёжностью** — auto-retry, мониторы, алерты в Telegram при любом сбое.
- **Показываю результат** — интерактивные дашборды для ежедневных решений.
- **Внедряю AI-агентов** — реcток, PPC-алерты, чат-агенты, обработка данных.

Результат для клиента: меньше ручной работы, ноль пропущенных сбоев, решения на свежих данных.

---

## Кейсы (в этом демо)

| Кейс | О чём |
|------|-------|
| 🛒 **Amazon Analytics** | ETL по SP-API, Buy Box, маржа, живой дашборд |
| 🔄 **ETL Orchestrator** | Один процесс держит аналитику 4 площадок 24/7 |
| 🤖 **AI Agents** | Агенты на Claude/Gemini: реcток, алерты, чат |

> Все данные в демо — синтетические. Реальные проекты обсуждаю под NDA.

---

## Стек

`Python` · `PostgreSQL` · `Streamlit` · `Amazon SP-API` · `Advertising API`
`Walmart API` · `Shopify API` · `Telegram Bot API` · `Claude / Gemini` · `Docker`

---

## Запуск локально

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Деплой (Streamlit Cloud)

1. Залить репозиторий на GitHub.
2. На [share.streamlit.io](https://share.streamlit.io) → **New app** → выбрать репо.
3. Main file: `streamlit_app.py` → получить ссылку.
4. Вставить ссылку в шапку профиля и в этот README.

---

## Структура

```
streamlit_app.py            # главная
pages/
  1_Amazon_Analytics.py     # кейс Amazon (живой дашборд)
  2_ETL_Orchestrator.py     # кейс ETL-оркестратора + схема
  3_AI_Agents.py            # кейс AI-агентов
  4_Contact.py              # контакты
assets/
  orchestrator_architecture.svg
```

---

📬 **Контакты:**tg  @vitter
