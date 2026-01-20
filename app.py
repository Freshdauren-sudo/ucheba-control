import streamlit as st
import json
import os
import requests
from datetime import datetime, timedelta
import random

# --- НАСТРОЙКИ ---
BOT_TOKEN = "8526733369:AAFyb9kE68lFOuCpUINp7fKS0aEapyfkdpA"

# 1376787931 - Твой ID (Имаш)
# 5185753365 - ID Даурена
USER_IDS = ["1376787931", "5185753365"] 

COURSE_URL = "https://juz40.kz"
TARGET_DATE = datetime(2026, 1, 28, 14, 30)

# Функция для получения времени Караганды (UTC+5)
def get_krg_time():
    return datetime.utcnow() + timedelta(hours=5)

def send_tg_message(text):
    for user_id in USER_IDS:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        params = {"chat_id": user_id, "text": text}
        try: requests.get(url, params=params)
        except: pass

# --- ЛОГИКА ДАННЫХ ---
DB_FILE = "status.json"
MOTIVATORS = [
    "🇰🇿 1465 г. — Образование Казахского ханства.",
    "📐 Sin²α + Cos²α = 1",
    "📚 1841 г. — Кенесары официально избран ханом.",
    "🚀 Бро, ты будущий грантник, не сдавайся!"
]

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: 
            return json.load(f)
    return {"user": None, "active": False, "start_time": None}

def save_data(data):
    with open(DB_FILE, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

# --- ИНТЕРФЕЙС ---
st.set_page_config(page_title="Juz40 Access", page_icon="🚀")
data = load_data()
now_krg = get_krg_time()

# 1. ТАЙМЕР ҰБТ
st.markdown("<h3 style='text-align: center;'>⏳ До Қ
