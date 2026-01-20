import streamlit as st
import json
import os
import requests
from datetime import datetime, timedelta
import random

# --- НАСТРОЙКИ ---
BOT_TOKEN = "8526733369:AAFyb9kE68lFOuCpUINp7fKS0aEapyfkdpA"
USER_IDS = ["1376787931", "5185753365"] 
COURSE_URL = "https://juz40.kz"
TARGET_DATE = datetime(2026, 1, 28, 14, 30)

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

# 1. ТАЙМЕР
st.markdown("### ⏳ До Қаңтар ҰБТ осталось:")
diff = TARGET_DATE - now_krg
if diff.total_seconds() > 0:
    days = diff.days
    hours, rem = divmod(diff.seconds, 3600)
    mins, _ = divmod(rem, 60)
    st.subheader(f"{days}д. {hours}ч. {mins}м.")
else:
    st.error("🏁 Экзамен начался!")

st.divider()

# 2. СТАТУС
if data.get("active"):
    st.error(f"🔴 СЕЙЧАС ВНУТРИ: {data['user']}")
    if data.get("start_time"):
        st.info(f"🕒 Зашел в {data['start_time']} (Караганда)")
else:
    st.success("🟢 СВОБОДНО")

st.link_button("🔗 ОТКРЫТЬ JUZ40.KZ", COURSE_URL, use_container_width=True)

st.write("") 

# 3. КНОПКИ
col1, col2 = st.columns(2)
with col1:
    if st.button("🙋‍♂️ Я Имаш", use_container_width=True):
        if not data.get("active"):
            t = get_krg_time().strftime("%H:%M")
            data.update({"active": True, "user": "Имаш", "start_time": t})
            save_data(data)
            st.toast(random.choice(MOTIVATORS))
            send_tg_message(f"🚀 Имаш зашел в {t}!")
            st.rerun()

with col2:
    if st.button("🙋‍♂️ Я Даурен", use_container_width=True):
        if not data.get("active"):
            t = get_krg_time().strftime("%H:%M")
            data.update({"active": True, "user": "Даурен", "start_time": t})
            save_data(data)
            st.toast(random.choice(MOTIVATORS))
            send_tg_message(f"🚀 Даурен зашел в {t}!")
            st.rerun()

if st.button("✅ Я ВЫШЕЛ", use_container_width=True):
    if data.get("active"):
        u = data["user"]
        data.update({"active": False, "user": None, "start_time": None})
        save_data(data)
        send_tg_message(f"✅ {u} вышел. Аккаунт свободен!")
        st.rerun()
