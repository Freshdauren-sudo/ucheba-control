import streamlit as st
import json
import os
import requests
import time
from datetime import datetime

# --- НАСТРОЙКИ (ВСТАВЬ СВОЕ) ---
BOT_TOKEN = "8526733369:AAFyb9kE68lFOuCpUINp7fKS0aEapyfkdpA"
USER_IDS = ["1376787931", "5185753365"]
COURSE_URL = "https://juz40.kz"
TARGET_DATE = datetime(2026, 1, 28, 14, 30) # Дата ҰБТ

def send_tg_message(text):
    for user_id in USER_IDS:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        params = {"chat_id": user_id, "text": text}
        try: requests.get(url, params=params)
        except: pass

# --- ЛОГИКА БАЗЫ ---
DB_FILE = "status.json"
def load_status():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return {"user": None, "active": False, "time": ""}

def save_status(user, active):
    now = datetime.now().strftime("%H:%M")
    status = {"user": user, "active": active, "time": now}
    with open(DB_FILE, "w") as f: json.dump(status, f)
    return status

# --- ИНТЕРФЕЙС ---
st.set_page_config(page_title="Juz40 & ҰБТ Timer", page_icon="🎯")

# --- ЖИВОЙ ТАЙМЕР ---
st.markdown("### ⏳ До Қаңтар ҰБТ осталось:")
timer_place = st.empty() # Место для обновляющегося таймера

# Функция для отрисовки таймера
def show_timer():
    diff = TARGET_DATE - datetime.now()
    if diff.total_seconds() > 0:
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        timer_place.subheader(f"📅 {days}д. {hours}ч. {minutes}м. {seconds}с.")
    else:
        timer_place.error("🏁 Экзамен начался!")

# Показываем таймер сразу
show_timer()

st.divider()

# --- ПАНЕЛЬ ДОСТУПА ---
status = load_status()
if status["active"]:
    st.error(f"🔴 СЕЙЧАС ВНУТРИ: {status['user']} (с {status['time']})")
else:
    st.success("🟢 СВОБОДНО. Заходи!")

st.link_button("🔗 ОТКРЫТЬ JUZ40.KZ", COURSE_URL, use_container_width=True)

st.divider()

col1, col2 = st.columns(2)
with col1:
    if st.button("🙋‍♂️ Я Имаш"):
        if not status["active"]:
            save_status("Имаш", True)
            send_tg_message("🚀 Имаш зашел в аккаунт Juz40!")
            st.rerun()
with col2:
    if st.button("🙋‍♂️ Я Даурен"):
        if not status["active"]:
            save_status("Даурен", True)
            send_tg_message("🚀 Даурен зашел в аккаунт Juz40!")
            st.rerun()

if st.button("✅ Я ВЫШЕЛ", use_container_width=True):
    if status["active"]:
        u = status["user"]
        save_status(None, False)
        send_tg_message(f"✅ {u} вышел. Аккаунт СВОБОДЕН!")
        st.rerun()

# --- АВТО-ОБНОВЛЕНИЕ ТАЙМЕРА ---
# Этот цикл заставляет таймер тикать каждую секунду
for i in range(60): 
    time.sleep(1)
    show_timer()
