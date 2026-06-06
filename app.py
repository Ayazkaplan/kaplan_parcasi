import streamlit as st
import requests

# Anahtarını buraya yapıştır
API_KEY = "AIzaSyCZXEoUCgJCQN9dGJ1A-w4l_xbV1tqb_yY"

st.set_page_config(page_title="ASLAN PARÇASI", layout="centered")
st.title("🤖 ASLAN PARÇASI V8.9")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Reis bir şey de..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # MODEL İSMİ: gemini-1.5-flash
        # URL: v1beta üzerinden doğrudan bağlanıyoruz
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                answer = response.json()['candidates'][0]['content']['parts'][0]['text']
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error(f"Hata Kodu: {response.status_code}")
                st.write("Detay:", response.json())
        except Exception as e:
            st.error(f"Bağlantı Hatası: {e}")
