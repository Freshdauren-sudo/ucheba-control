import streamlit as st
import json
import os
import requests
from datetime import datetime

# --- НАСТРОЙКИ TELEGRAM ---
BOT_TOKEN = "8526733369:AAFyb9kE68lFOuCpUINp7fKS0aEapyfkdpA"  # Вставь сюда токен от BotFather
USER_IDS = ["1376787931", "5185753365"] # Вставь ID (свой и друга) через запятую

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
    return {"user": None, "active": False}

def save_status(user, active):
    status = {"user": user, "active": active, "time": datetime.now().strftime("%H:%M")}
    with open(DB_FILE, "w") as f:
        json.dump(status, f)
    return status

st.title("📚 Juz40 Контроль")

status = load_status()

if status["active"]:
    st.error(f"🔴 СЕЙЧАС СИДИТ: {status['user']}")
else:
    st.success("🟢 СВОБОДНО. Заходи!")

st.divider()

if st.button("🚀 Я ЗАШЕЛ"):
    save_status("Кто-то из вас", True)
    st.rerun()

if st.button("✅ Я ВЫШЕЛ"):
    save_status(None, False)
    # Когда нажимаете "Вышел", бот пишет в Телеграм
    send_tg_message("✅ Аккаунт Juz40 освободился! Можно заходить.")
    st.rerun()
