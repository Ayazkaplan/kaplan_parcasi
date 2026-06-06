import streamlit as st
import requests

# AIza anahtarını buraya koyduk
API_KEY = "AIzaSyCZXEoUCgJCQN9dGJ1A-w4l_xbV1tqb_yY"

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
        # v1beta yerine doğrudan v1 kullanıyoruz, bu anahtarınla en uyumlu olan bu
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        
        headers = {'Content-Type': 'application/json'}
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                answer = data['candidates'][0]['content']['parts'][0]['text']
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error(f"Hata Kodu {response.status_code}: {response.json()}")
        except Exception as e:
            st.error(f"Bağlantı Hatası: {e}")
