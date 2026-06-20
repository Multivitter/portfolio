import streamlit as st

st.set_page_config(page_title="Контакты", page_icon="✉️", layout="centered")

st.title("✉️ Контакты")

st.write(
    "Готов обсудить вывод бренда на Amazon, аналитику, "
    "автоматизацию или AI-агентов под вашу задачу."
)

st.divider()

st.markdown("**Telegram:** `@your_handle`")
st.markdown("**Email:** `you@example.com`")
st.markdown("**GitHub:** `github.com/your_handle`")

st.divider()

st.markdown("### Как работаю")
st.write(
    "1. Короткий созвон — что болит, какие данные есть.\n"
    "2. Прототип на демо-данных за несколько дней.\n"
    "3. Интеграция в ваш контур под NDA."
)

st.caption("Реальные кейсы и цифры показываю индивидуально.")
