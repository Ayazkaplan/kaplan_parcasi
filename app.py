import streamlit as st
import requests
import os
import json
import firebase_admin
from firebase_admin import credentials, auth, firestore
from duckduckgo_search import DDGS
from datetime import datetime, timedelta

# --- FIREBASE BAŞLATMA ---
if not firebase_admin._apps:
    secret_path = "/etc/secrets/firebase-key.json"
    local_path = "firebase-key.json"
    path_to_use = secret_path if os.path.exists(secret_path) else (local_path if os.path.exists(local_path) else None)
    
    if path_to_use:
        with open(path_to_use, 'r') as f:
            key_dict = json.load(f)
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred)
    else:
        st.error("Firebase anahtarı bulunamadı!")
        st.stop()

db = firestore.client()

# --- AYARLAR VE DOSYA İŞLEMLERİ ---
API_KEY = os.environ.get("API_KEY")
MODEL = "anthropic/claude-3-haiku"
DOSYA_ADI, MOD_DOSYASI = "sarki_id.txt", "mod_id.txt"

def kaydet(dosya, deger): 
    with open(dosya, "w") as f: f.write(deger.strip())

def oku(dosya): 
    return open(dosya, "r").read().strip() if os.path.exists(dosya) else ""

# --- OTURUM YÖNETİMİ ---
if "user_logged_in" not in st.session_state: st.session_state.user_logged_in = False
if "user_name" not in st.session_state: st.session_state.user_name = "Mehmet Reis"

if not st.session_state.user_logged_in:
    st.title("🦁 Aslan Parçası V16.4")
    email = st.text_input("📧 E-posta:")
    password = st.text_input("🔑 Şifre:", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Giriş Yap"):
            try:
                user = auth.get_user_by_email(email)
                user_doc = db.collection("users").document(user.uid).get()
                st.session_state.user_logged_in = True
                st.session_state.user_name = user_doc.to_dict().get("isim", "Mehmet Reis") if user_doc.exists else "Mehmet Reis"
                st.rerun()
            except: st.error("❌ Hata! E-posta veya şifre yanlış.")
    with col2:
        if st.button("Kayıt Ol"):
            try:
                auth.create_user(email=email, password=password)
                st.success("✅ Kayıt başarılı!")
            except Exception as e: st.error(f"❌ Hata: {e}")
    st.stop()

# --- ANA EKRAN ---
st.set_page_config(page_title="Aslan Parçası V16.4", page_icon="🦁")

with st.sidebar:
    st.success(f"✅ Hoş geldin, {st.session_state.user_name}")
    if st.button("🚪 Çıkış Yap"): 
        st.session_state.user_logged_in = False; st.rerun()
    
    kayitli_id = oku(DOSYA_ADI)
    yeni_id = st.text_input("YouTube ID:", value=kayitli_id)
    if st.button("💾 Kaydet"): kaydet(DOSYA_ADI, yeni_id); st.rerun()
    if kayitli_id: st.markdown(f'<iframe width="100%" height="150" src="https://www.youtube.com/embed/{kayitli_id}" frameborder="0"></iframe>', unsafe_allow_html=True)

# --- SOHBET ---
if "messages" not in st.session_state: st.session_state.messages = []
st.title("🤖 Aslan Parçası V16.4")

def ai_cevap(mesaj_gecmisi, isim, mesaj):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    talimat = f"Sen Aslan Parçası'sın. {isim} ile konuşuyorsun."
    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json={"model": MODEL, "messages": [{"role": "system", "content": talimat}] + mesaj_gecmisi[-6:]})
        return res.json()['choices'][0]['message']['content']
    except: return "Sistem meşgul Reis."

for m in st.session_state.messages:
    st.chat_message(m["role"]).markdown(m["content"])

if user_input := st.chat_input("Mesajını yaz..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    cevap = ai_cevap(st.session_state.messages, st.session_state.user_name, user_input)
    st.session_state.messages.append({"role": "assistant", "content": cevap})
    st.rerun()
 
