import streamlit as st
import requests
import os

# AYARLAR
API_KEY = "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"
MODEL = "meta-llama/llama-3.3-70b-instruct"
KURUCU_SIFRESI = "KAPLAN_REIS_74"

st.set_page_config(page_title="Aslan Parçası V9.4", page_icon="🤖")

st.title("🤖 Aslan Parçası V9.4")

# Şifre Kontrolü (Sidebar)
with st.sidebar:
    sifre = st.text_input("🔑 Şifre (Kurucuysan gir):", type="password")
    mod = "Kurucu" if sifre == KURUCU_SIFRESI else "Misafir"
    st.write(f"Mod: **{mod}**")

# Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Geçmişi Ekrana Yaz
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Yapay Zeka Cevap Fonksiyonu
def ai_cevap(kullanici_mesaj):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "https://localhost",
        "X-Title": "Aslan Parcasi",
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Sen Ayaz Reis'in asistanısın. Sadece Türkçe konuş. Doğal ve günlük konuş."},
            {"role": "user", "content": kullanici_mesaj}
        ]
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        data = response.json()
        return data['choices'][0]['message']['content'].strip()
    except:
        return "Bağlantı hatası oluştu."

# Mesaj alma
if prompt := st.chat_input("Mesajını yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        cevap = ai_cevap(prompt)
        st.markdown(cevap)
    st.session_state.messages.append({"role": "assistant", "content": cevap})
