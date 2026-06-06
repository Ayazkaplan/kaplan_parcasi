import streamlit as st
import requests
import os

# Render'dan API anahtarını alıyoruz
API_KEY = os.environ.get("API_KEY")
MODEL = "meta-llama/llama-3.3-70b-instruct"
KURUCU_SIFRESI = "KAPLAN_REIS_74"

st.set_page_config(page_title="Aslan Parçası V9.4", page_icon="🤖")

st.title("🤖 Aslan Parçası V9.4")

# Şifre Kontrolü
with st.sidebar:
    sifre = st.text_input("🔑 Şifre (Kurucuysan gir):", type="password")
    mod = "Kurucu" if sifre == KURUCU_SIFRESI else "Misafir"
    st.write(f"Mod: **{mod}**")

# Mesaj geçmişini tutan yapı
if "messages" not in st.session_state:
    st.session_state.messages = []

# Geçmişi ekrana yazdır
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def ai_cevap(kullanici_mesaj):
    if not API_KEY:
        return "Hata: API anahtarı tanımlanmadı."
        
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "https://aslan-parcasi-widget.onrender.com",
        "X-Title": "Aslan Parcasi",
    }
    # Sistem talimatını daha net ve hatasız yazması için güncelledik
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Sen Ayaz Reis'in asistanısın. Her zaman düzgün, Türkçe dil bilgisi kurallarına uygun, nazik ve profesyonel cevaplar ver. Asla yazım hatası yapma ve harfleri büyük-küçük karıştırma."},
            {"role": "user", "content": kullanici_mesaj}
        ]
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        data = response.json()
        if 'choices' in data:
            return data['choices'][0]['message']['content'].strip()
        else:
            return f"API Hatası: {data}"
    except Exception as e:
        return f"Bağlantı hatası: {str(e)}"

# Mesaj girişi ve yanıt alma
if prompt := st.chat_input("Mesajını yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        cevap = ai_cevap(prompt)
        st.markdown(cevap)
    st.session_state.messages.append({"role": "assistant", "content": cevap})
