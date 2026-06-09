import streamlit as st
import requests
import os
import json
import firebase_admin
from firebase_admin import credentials, auth, firestore
import re
from datetime import datetime, timedelta

# --- AYARLAR ---
KURUCU_EMAIL = "ayazscma92@gmail.com"
KURUCU_ISIM = "Ayaz Kaplan"
MODEL = "anthropic/claude-3-haiku"
AVATAR_URL = "https://i.imgur.com/3EfO8Ae.jpeg"
USER_AVATAR = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
FIREBASE_API_KEY = os.environ.get("FIREBASE_API_KEY") 

TEMALAR = {
    "🦁 Aslan İni": "linear-gradient(135deg, #0f2027, #203a43, #2c5364)",
    "👑 Kraliyet": "linear-gradient(135deg, #1a0000, #4a0000, #8b0000)",
    "🌲 Orman Derinliği": "linear-gradient(135deg, #061700, #142f10, #2c4a2c)",
    "💻 Teknoloji": "linear-gradient(135deg, #000428, #004e92)",
    "🌌 Uzay": "linear-gradient(135deg, #0f0c29, #302b63, #24243e)"
}

# --- CSS STİLLERİ ---
STIL = """
<style>
    .assistant-box { background-color: rgba(30,30,30,0.8); padding: 15px; border-radius: 10px; border-left: 5px solid gold; margin-bottom: 15px; display: flex; align-items: flex-start; gap: 10px; color: white; }
    .user-box { background-color: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin-bottom: 15px; display: flex; justify-content: flex-end; align-items: flex-start; gap: 10px; color: white; }
    .avatar { width: 40px; height: 40px; border-radius: 50%; }
    .header-box { font-weight: bold; margin-bottom: 5px; }
</style>
"""
st.markdown(STIL, unsafe_allow_html=True)

# --- FIREBASE BAŞLATMA ---
if not firebase_admin._apps:
    secret_path = "/etc/secrets/firebase-key.json"
    local_path = "firebase-key.json"
    path_to_use = secret_path if os.path.exists(secret_path) else (local_path if os.path.exists(local_path) else None)
    if path_to_use:
        with open(path_to_use, 'r') as f: cred = credentials.Certificate(json.load(f))
        firebase_admin.initialize_app(cred)
    else: st.error("Firebase anahtarı bulunamadı!"); st.stop()

db = firestore.client()

def update_activity(uid):
    db.collection("users").document(uid).update({"son_aktif": firestore.SERVER_TIMESTAMP})

# --- OTURUM YÖNETİMİ ---
if "user_logged_in" not in st.session_state: st.session_state.user_logged_in = False
if "messages" not in st.session_state: st.session_state.messages = []
if "page" not in st.session_state: st.session_state.page = "main"

# --- GİRİŞ EKRANI ---
if not st.session_state.user_logged_in:
    st.title("🦁 Aslan Parçası V16.5")
    email = st.text_input("📧 E-posta:")
    password = st.text_input("🔑 Şifre:", type="password")
    if st.button("Giriş Yap"):
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
        res = requests.post(url, json={"email": email, "password": password, "returnSecureToken": True})
        if res.status_code == 200:
            uid = res.json()['localId']
            st.session_state.user_data = {"uid": uid}
            st.session_state.user_logged_in = True
            update_activity(uid)
            st.rerun()
    st.stop()

# --- YÖNETİCİ SAYFASI ---
if st.session_state.page == "admin":
    st.title("🛡️ Kullanıcı Yönetim Merkezi")
    if st.button("⬅️ Geri Dön"): st.session_state.page = "main"; st.rerun()
    users = db.collection("users").stream()
    for u in users:
        data = u.to_dict()
        email = data.get("email")
        col1, col2 = st.columns([0.8, 0.2])
        col1.code(f"İsim: {data.get('isim')}\nE-posta: {email}\nŞifre: {data.get('sifre_yedek', 'Yok')}")
        if col2.button("🗑️ SİL", key=email):
            st.session_state.silinecek_user = u.id
    
    if "silinecek_user" in st.session_state:
        st.warning(f"Bu hesabı silmek istediğinize emin misiniz? (Kalıcı İşlem)")
        if st.button("EVET, EMİNİM"):
            db.collection("users").document(st.session_state.silinecek_user).delete()
            del st.session_state.silinecek_user
            st.rerun()
    st.stop()

# --- ANA EKRAN ---
uid = st.session_state.user_data['uid']
update_activity(uid)
user_ref = db.collection("users").document(uid)
user_doc = user_ref.get().to_dict()
is_kurucu = user_doc.get('email') == KURUCU_EMAIL

st.markdown(f"<style>.stApp {{ background: {user_doc.get('tema', list(TEMALAR.values())[0])} !important; }}</style>", unsafe_allow_html=True)

with st.sidebar:
    if is_kurucu and st.button("🛠️ YÖNETİCİ PANELİ"): st.session_state.page = "admin"; st.rerun()
    if st.button("🧹 Sohbeti Temizle"): st.session_state.messages = []; st.rerun()
    if st.button("🚪 Çıkış Yap"): st.session_state.clear(); st.rerun()

st.title("🤖 Aslan Parçası V16.5")
for m in st.session_state.messages:
    if m["role"] == "assistant":
        st.markdown(f'''<div class="assistant-box"><img src="{AVATAR_URL}" class="avatar"><div class="header-box">Aslan Parçası</div><div>{m["content"]}</div></div>''', unsafe_allow_html=True)
    else:
        st.markdown(f'''<div class="user-box"><div class="header-box">{user_doc.get('isim')}</div><div>{m["content"]}</div><img src="{USER_AVATAR}" class="avatar"></div>''', unsafe_allow_html=True)

def ai_cevap(mesajlar):
    sistem = f"Sen 'Aslan Parçası'. {'Kurucun Ayaz Kaplan sensin.' if is_kurucu else ''} Kullanıcı: {user_doc.get('isim')}."
    payload = {"model": MODEL, "messages": [{"role": "system", "content": sistem}] + mesajlar}
    headers = {"Authorization": f"Bearer {os.environ.get('API_KEY')}"}
    try: return requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload).json()['choices'][0]['message']['content']
    except: return "Sistem yorgun, Reis."

if "my_input" in st.session_state and st.session_state.my_input:
    st.session_state.messages.append({"role": "user", "content": st.session_state.my_input})
    st.session_state.messages.append({"role": "assistant", "content": ai_cevap(st.session_state.messages)})
    st.session_state.my_input = ""
    st.rerun()

st.text_area("Mesajını yaz:", key="my_input")
if st.button("🚀 Gönder"): st.rerun()
