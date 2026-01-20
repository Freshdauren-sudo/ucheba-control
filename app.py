import streamlit as st
import json
import os
import requests
from datetime import datetime

# --- НАСТРОЙКИ (ВСТАВЬ СВОЕ) ---
BOT_TOKEN = "8526733369:AAFyb9kE68lFOuCpUINp7fKS0aEapyfkdpA"
USER_IDS = ["1376787931", "5185753365"]
COURSE_URL = "https://juz40.kz" # Ссылка на вход в курс

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
st.set_page_config(page_title="Juz40 Access", page_icon="🚀")

# Кастомный CSS для красоты кнопок
st.markdown("""
    <style>
    div.stButton > button:first-child {
        height: 3em;
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Управление доступом Juz40")

status = load_status()

# Статус-панель
if status["active"]:
    st.error(f"🔴 СЕЙЧАС ВНУТРИ: {status['user']}")
    st.info(f"🕒 Зашел в {status['time']}")
else:
    st.success("🟢 СВОБОДНО. Путь открыт!")

st.divider()

# Ссылка на курс (Всегда видна)
st.link_button("🔗 ОТКРЫТЬ САЙТ JUZ40.KZ", COURSE_URL, use_container_width=True, type="primary")

st.divider()

# Кнопки выбора пользователя
st.subheader("Кто заходит?")
col1, col2 = st.columns(2)

with col1:
    if st.button("🙋‍♂️ Я Имаш", key="imash"):
        if not status["active"]:
            save_status("Имаш", True)
            send_tg_message("🚀 Имаш зашел в аккаунт Juz40!")
            st.rerun()
        else:
            st.warning(f"Там уже {status['user']}")

with col2:
    if st.button("🙋‍♂️ Я Даурен", key="dauren"):
        if not status["active"]:
            save_status("Даурен", True)
            send_tg_message("🚀 Даурен зашел в аккаунт Juz40!")
            st.rerun()
        else:
            st.warning(f"Там уже {status['user']}")

st.divider()

# Кнопка выхода
if st.button("✅ Я ВЫШЕЛ (Освободить аккаунт)"):
    if status["active"]:
        user_who_left = status["user"]
        save_status(None, False)
        send_tg_message(f"✅ {user_who_left} вышел. Аккаунт СВОБОДЕН!")
        st.rerun()
