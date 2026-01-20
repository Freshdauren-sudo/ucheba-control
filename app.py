import streamlit as st
import json
import os
import requests
from datetime import datetime

# --- НАСТРОЙКИ TELEGRAM (ВСТАВЬ СВОИ ДАННЫЕ) ---
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

# --- ГЛАВНАЯ ЛОГИКА ---
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

st.set_page_config(page_title="Juz40 Access", page_icon="📚")
st.title("📚 Juz40 Контроль")

status = load_status()

if status["active"]:
    st.error(f"🔴 СЕЙЧАС СИДИТ: {status['user']}")
    st.caption(f"Зашел в {status['time']}")
else:
    st.success("🟢 СВОБОДНО. Можно заходить!")

st.divider()

# КНОПКА ЗАХОДА
if st.button("🚀 Я ЗАШЕЛ (Занять аккаунт)"):
    if not status["active"]:
        save_status("Друг", True)
        send_tg_message("🚀 Кто-то зашел в аккаунт Juz40! Теперь занято.")
        st.rerun()
    else:
        st.warning("Аккаунт уже занят!")

# КНОПКА ВЫХОДА
if st.button("✅ Я ВЫШЕЛ (Освободить)"):
    save_status(None, False)
    send_tg_message("✅ Аккаунт Juz40 СВОБОДЕН! Можно заходить.")
    st.rerun()
