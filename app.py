import streamlit as st
import json
import os
import requests
from datetime import datetime, timedelta
import random
import time

# --- НАСТРОЙКИ ---
BOT_TOKEN = "8526733369:AAFyb9kE68lFOuCpUINp7fKS0aEapyfkdpA"
USER_IDS = ["1376787931", "5185753365"]
COURSE_URL = "https://juz40.kz"
# Дата ҰБТ: 28 января 2026, 14:30
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
    "🇰🇿 1219 г. — Начало нашествия Чингисхана на Казахстан.",
    "📐 Sin²α + Cos²α = 1",
    "📚 1841 г. — Кенесары официально избран ханом.",
    "📈 Формула Пика: S = В + Г/2 - 1",
    "🚀 Бро, ты будущий грантник, не сдавайся!",
    "🏛 1465 г. — Образование Казахского ханства."
]

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return {"user": None, "active": False, "start_time": None, "total_time": {"Имаш": 0, "Даурен": 0}}

def save_data(data):
    with open(DB_FILE, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

# --- ИНТЕРФЕЙС ---
st.set_page_config(page_title="Juz40 Karaganda", page_icon="👑")
data = load_data()
now_krg = get_krg_time()

# 1. ТАЙМЕР ҰБТ (КАРАГАНДА)
st.markdown("<h3 style='text-align: center;'>🇰🇿 До Қаңтар ҰБТ осталось:</h3>", unsafe_allow_html=True)
timer_place = st.empty()

# Расчет времени до экзамена
diff = TARGET_DATE - now_krg
if diff.total_seconds() > 0:
    days = diff.days
    hours, rem = divmod(diff.seconds, 3600)
    mins, secs = divmod(rem, 60)
    timer_place.markdown(f"<h2 style='text-align: center; color: #FF4B4B;'>{days}д. {hours}ч. {mins}м. {secs}с.</h2>", unsafe_allow_html=True)
else:
    timer_place.error("🏁 Экзамен начался!")

st.divider()

# 2. МУЗЫКА ДЛЯ ФОКУСА
with st.expander("🎧 ВКЛЮЧИТЬ МУЗЫКУ ДЛЯ УЧЕБЫ"):
    st.write("Lofi-биты для концентрации:")
    st.video("https://www.youtube.com/watch?v=jfKfPfyJRdk")

st.divider()

# 3. ЛИДЕРБОРД
st.subheader("🏆 Король Юза")
imash_m = data["total_time"].get("Имаш", 0)
dauren_m = data["total_time"].get("Даурен", 0)
c1, c2 = st.columns(2)
with c1:
    k = "👑" if imash_m >= dauren_m and imash_m > 0 else ""
    st.metric(f"{k} Имаш", f"{imash_m // 60}ч {imash_m % 60}м")
with c2:
    k = "👑" if dauren_m >= imash_m and dauren_m > 0 else ""
    st.metric(f"{k} Даурен", f"{dauren_m // 60}ч {dauren_m % 60}м")

st.divider()

# 4. СТАТУС
if data["active"]:
    st.error(f"🔴 СЕЙЧАС ВНУТРИ: {data['user']}")
    st.info(f"🕒 Зашел в {data['start_time']} (Время Караганды)")
else:
    st.success("🟢 СВОБОДНО. Заходи!")

st.link_button("🔗 ОТКРЫТЬ JUZ40.KZ", COURSE_URL, use_container_width=True)

# 5. КНОПКИ
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("🙋‍♂️ Я Имаш", use_container_width=True):
        if not data["active"]:
            data["active"], data["user"] = True, "Имаш"
            data["start_time"] = get_krg_time().strftime("%H:%M")
            data["start_dt_iso"] = get_krg_time().isoformat()
            save_data(data)
            st.toast(random.choice(MOTIVATORS))
            send_tg_message(f"🚀 Имаш зашел в {data['start_time']}!")
            st.rerun()

with col_btn2:
    if st.button("🙋‍♂️ Я Даурен", use_container_width=True):
        if not data["active"]:
            data["active"], data["user"] = True, "Даурен"
            data["start_time"] = get_krg_time().strftime("%H:%M")
            data["start_dt_iso"] = get_krg_time().isoformat()
            save_data(data)
            st.toast(random.choice(MOTIVATORS))
            send_tg_message(f"🚀 Даурен зашел в {data['start_time']}!")
            st.rerun()

if
