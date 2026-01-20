import streamlit as st
import json
import os
import requests
from datetime import datetime

# --- НАСТРОЙКИ (ВСТАВЬ СВОЕ) ---
BOT_TOKEN = "8526733369:AAFyb9kE68lFOuCpUINp7fKS0aEapyfkdpA"
USER_IDS = ["1376787931", "5185753365"]

def send_tg_message(text):
    for user_id in USER_IDS:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        params = {"chat_id": user_id, "text": text}
        try:
            requests.get(url, params=params)
        except:
            pass

# --- ЛОГИКА БАЗЫ ДАННЫХ ---
DB_FILE = "status.json"

def load_status():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"user": None, "active": False, "time": ""}

def save_status(user, active):
    now = datetime.now().strftime("%H:%M")
    status = {"user": user, "active": active, "time": now}
    with open(DB_FILE, "w") as f:
        json.dump(status, f)
    return status

# --- ИНТЕРФЕЙС САЙТА ---
st.set_page_config(page_title="Juz40: Имаш & Даурен", page_icon="👨‍🎓")
st.title("📚 Доступ к Juz40")

status = load_status()

# Отображение текущего состояния
if status["active"]:
    st.error(f"🔴 СЕЙЧАС В АККАУНТЕ: {status['user']}")
    st.info(f"🕒 Время захода: {status['time']}")
else:
    st.success("🟢 СВОБОДНО. Можно заходить!")

st.divider()

# Кнопки для каждого игрока
st.subheader("Кто заходит?")
col1, col2 = st.columns(2)

with col1:
    if st.button("🙋‍♂️ Я Имаш"):
        if not status["active"]:
            save_status("Имаш", True)
            send_tg_message("🚀 Имаш зашел в аккаунт Juz40!")
            st.rerun()
        else:
            st.warning(f"Занято: {status['user']}")

with col2:
    if st.button("🙋‍♂️ Я Даурен"):
        if not status["active"]:
            save_status("Даурен", True)
            send_tg_message("🚀 Даурен зашел в аккаунт Juz40!")
            st.rerun()
        else:
            st.warning(f"Занято: {status['user']}")

st.divider()

# Общая кнопка выхода
if st.button("✅ Я ВЫШЕЛ (Освободить для друга)"):
    if status["active"]:
        old_user = status["user"]
        save_status(None, False)
        send_tg_message(f"✅ {old_user} вышел. Аккаунт СВОБОДЕН!")
        st.rerun()
    else:
        st.write("Аккаунт и так свободен.")
