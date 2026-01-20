import streamlit as st
import json
import os
import requests
from datetime import datetime, timedelta
import random

# --- НАСТРОЙКИ ---
BOT_TOKEN = "8526733369:AAFyb9kE68lFOuCpUINp7fKS0aEapyfkdpA"
# Вставил сюда твой ID и ID Даурена со скриншота
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
            data = json.load(f)
            if "total_time" not in data: data["total_time"] = {"Имаш": 0, "Даурен": 0}
            return data
    return {"user": None, "active": False, "start_time": None, "start_dt_iso": None, "total_time": {"Имаш": 0, "Даурен": 0}}

def save_data(data):
    with open(DB_FILE, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

# --- ИНТЕРФЕЙС ---
st.set_page_config(page_title="Juz40 Karaganda", page_icon="👑")
data = load_data()
now_krg = get_krg_time()

# 1. ТАЙМЕР ҰБТ
st.markdown("<h3 style='text-align: center;'>⏳ До Қаңтар ҰБТ осталось:</h3>", unsafe_allow_html=True)
diff = TARGET_DATE - now_krg
if diff.total_seconds() > 0:
    days = diff.days
    hours, rem = divmod(diff.seconds, 3600)
    mins, _ = divmod(rem, 60)
    st.markdown(f"<h2 style='text-align: center; color: #FF4B4B;'>{days}д. {hours}ч. {mins}м.</h2>", unsafe_allow_html=True)

st.divider()

# 2. МУЗЫКА
with st.expander("🎧 МУЗЫКА ДЛЯ УЧЕБЫ"):
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
    st.info(f"🕒 Зашел в {data['start_time']} (Караганда)")
else:
    st.success("🟢 СВОБОДНО")

st.link_button("🔗 ОТКРЫТЬ JUZ40.KZ", COURSE_URL, use_container_width=True)

# 5. КНОПКИ
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("🙋‍♂️ Я Имаш", use_container_width=True):
        if not data["active"]:
            data["active"], data["user"] = True, "Имаш"
            data["start_time"] = now_krg.strftime("%H:%M")
            data["start_dt_iso"] = now_krg.isoformat()
            save_data(data)
            st.toast(random.choice(MOTIVATORS))
            send_tg_message(f"🚀 Имаш зашел в {data['start_time']}!")
            st.rerun()

with col_btn2:
    if st.button("🙋‍♂️ Я Даурен", use_container_width=True):
        if not data["active"]:
            data["active"], data["user"] = True, "Даурен"
            data["start_time"] = now_krg.strftime("%H:%M")
            data["start_dt_iso"] = now_krg.isoformat()
            save_data(data)
            st.toast(random.choice(MOTIVATORS))
            send_tg_message(f"🚀 Даурен зашел в {data['start_time']}!")
            st.rerun()

if st.button("✅ Я ВЫШЕЛ", use_container_width=True):
    if data["active"]:
        start_dt = datetime.fromisoformat(data["start_dt_iso"])
        duration = get_krg_time() - start_dt
        m_spent = int(duration.total_seconds() // 60)
        u = data["user"]
        data["total_time"][u] += m_spent
        data["active"], data["user"] = False, None
        save_data(data)
        send_tg_message(f"✅ {u} вышел. Учился {m_spent} мин.")
        st.rerun()
