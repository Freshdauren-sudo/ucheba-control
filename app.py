import streamlit as st
import json
import os
from datetime import datetime

# Настройки файла базы данных
DB_FILE = "status.json"

def load_status():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"user": None, "active": False, "last_change": ""}

def save_status(user, active):
    status = {
        "user": user,
        "active": active,
        "last_change": datetime.now().strftime("%H:%M:%S")
    }
    with open(DB_FILE, "w") as f:
        json.dump(status, f)
    return status

st.set_page_config(page_title="Juz40 Access Control", page_icon="📚")

st.title("📚 Кто сейчас на аккаунте?")

status = load_status()

# Отображение текущего статуса
if status["active"]:
    st.error(f"🔴 СЕЙЧАС СИДИТ: {status['user']}")
    st.caption(f"Зашел в: {status['last_change']}")
else:
    st.success("🟢 СВОБОДНО. Можно заходить!")

st.divider()

# Кнопки управления
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Я ЗАШЕЛ (Бронирую)"):
        # Тут впиши ваше имя для удобства
        save_status("Друг", True) 
        st.rerun()

with col2:
    if st.button("✅ Я ВЫШЕЛ (Освободил)"):
        save_status(None, False)
        st.rerun()

st.info("Пожалуйста, не забывайте нажимать 'Вышел', когда закончили!")
