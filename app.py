import streamlit as st
import requests
import os
import firebase_admin
from firebase_admin import credentials, auth
from duckduckgo_search import DDGS
from datetime import datetime, timedelta

# --- FIREBASE BAŞLATMA ---
if not firebase_admin._apps:
    # Render'da "GOOGLE_APPLICATION_CREDENTIALS" ortam değişkenini kullandığını varsayıyorum
    # Eğer localde çalışıyorsan 'firebase-key.json' dosyasının yerinde olduğundan emin ol.
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred)

# --- AYARLAR ---
API_KEY = os.environ.get("API_KEY")
MODEL = "anthropic/claude-3-haiku"
NIHAI_SIFRE = "NiHAi_-kuRucU-AyAz"
AVATAR_URL = "https://i.imgur.com/3EfO8Ae.jpeg"
USER_AVATAR = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
DOSYA_ADI = "sarki_id.txt"
MOD_DOSYASI = "mod_id.txt"
ISIM_DOSYASI = "isim_id.txt"
TEMA_KURUCU = "tema_kurucu.txt"
TEMA_MISAFIR = "tema_misafir.txt"

# --- OTURUM YÖNETİMİ ---
if "user_logged_in" not in st.session_state: st.session_state.user_logged_in = False

# --- FONKSİYONLAR ---
def kaydet(dosya, deger):
    with open(dosya, "w") as f: f.write(deger.strip())

def oku(dosya):
    if os.path.exists(dosya):
        with open(dosya, "r") as f: return f.read().strip()
    return ""

def sil(dosya):
    if os.path.exists(dosya): os.remove(dosya)

def web_ara(sorgu):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(sorgu, max_results=3))
            return "Güncel bilgiler: " + "\n".join([r['body'] for r in results])
    except: return "İnternete erişemiyorum Reis."

# --- FIREBASE GİRİŞ EKRANI ---
if not st.session_state.user_logged_in:
    st.title("🦁 Aslan Parçası V16.4 - Giriş")
    email = st.text_input("📧 E-posta:")
    password = st.text_input("🔑 Şifre (Sadece kayıt için):", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Giriş Yap"):
            try:
                # Firebase'de e-posta kontrolü
                user = auth.get_user_by_email(email)
                st.session_state.user_logged_in = True
                kaydet(MOD_DOSYASI, "Kurucu")
                st.rerun()
            except:
                st.error("❌ Kullanıcı bulunamadı!")
    with col2:
        if st.button("Kayıt Ol"):
            try:
                auth.create_user(email=email, password=password)
                st.success("✅ Kayıt başarılı! Giriş yapabilirsin.")
            except Exception as e:
                st.error(f"❌ Kayıt hatası: {e}")
    st.stop()

st.set_page_config(page_title="Aslan Parçası V16.4", page_icon="🦁")

# --- MOD YÖNETİMİ ---
mod = "Kurucu" # Firebase ile giren herkes şimdilik kurucu modunda
if "messages" not in st.session_state: st.session_state.messages = []
if "input_key" not in st.session_state: st.session_state.input_key = 0
if "ayaz_yetkili" not in st.session_state: st.session_state.ayaz_yetkili = False
if "admin_panel_open" not in st.session_state: st.session_state.admin_panel_open = False

def get_theme_data(mod):
    assistant_box_bg = "rgba(30, 30, 30, 0.9)"
    themes = {
        "Aslan İni": ("linear-gradient(to bottom, #1a1a00, #000000)", "white"),
        "Kraliyet": ("linear-gradient(to bottom, #2c0000, #000000)", "white"),
        "Uzay": ("linear-gradient(to bottom, #1a0033, #000000)", "white")
    }
    return assistant_box_bg, themes

with st.sidebar:
    st.success("✅ Firebase Modu Aktif")
    if st.button("🚪 Çıkış Yap"): 
        sil(MOD_DOSYASI); sil(ISIM_DOSYASI); st.session_state.user_logged_in = False; st.rerun()
    
    kayitli_isim = oku(ISIM_DOSYASI) or "Mehmet Reis"
    secim = st.selectbox("👤 Kimsin Reis?", ["Mehmet Reis", "Ayaz Reis"], index=["Mehmet Reis", "Ayaz Reis"].index(kayitli_isim))
    
    if secim == "Ayaz Reis":
        if not st.session_state.ayaz_yetkili:
            gizli_sifre = st.text_input("👑 Ayaz Reis Şifresi:", type="password")
            if st.button("Doğrula"):
                if gizli_sifre == NIHAI_SIFRE: st.session_state.ayaz_yetkili = True; kaydet(ISIM_DOSYASI, "Ayaz Reis"); st.rerun()
                else: st.error("❌ Hatalı Şifre!")
            isim = "Mehmet Reis"
        else: isim = "Ayaz Reis"
    else: st.session_state.ayaz_yetkili = False; kaydet(ISIM_DOSYASI, "Mehmet Reis"); isim = "Mehmet Reis"

    assistant_box_bg, theme_map = get_theme_data(mod)
    tema_secimi = st.selectbox("Arka Plan:", list(theme_map.keys()))
    bg_color, text_color = theme_map[tema_secimi]
    
    if st.button("🔄 Sohbeti Temizle"): st.session_state.messages = []; st.rerun()

# --- STYLE VE MAIN KISMI AYNI KALDI ---
st.markdown(f"""<style>.stApp {{ background: {bg_color}; color: {text_color} !important; }} .assistant-box {{ background-color: {assistant_box_bg}; padding: 15px; border-radius: 10px; border-left: 5px solid gold; margin-bottom: 10px; }} .user-box {{ background-color: rgba(128, 128, 128, 0.2); padding: 15px; border-radius: 10px; margin-bottom: 10px; text-align: right; }}</style>""", unsafe_allow_html=True)

st.title("🤖 Aslan Parçası V16.4")

def ai_cevap(mesaj_gecmisi, isim, kullanici_mesaji):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    talimat = f"Sen Aslan Parçası adlı asistansın. {isim} ile konuşuyorsun."
    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json={"model": MODEL, "messages": [{"role": "system", "content": talimat}] + mesaj_gecmisi[-6:]})
        return res.json()['choices'][0]['message']['content']
    except: return "Sistem meşgul, Reis."

for m in st.session_state.messages:
    if m["role"] == "assistant": st.markdown(f'<div class="assistant-box">{m["content"]}</div>', unsafe_allow_html=True)
    else: st.markdown(f'<div class="user-box">{m["content"]}</div>', unsafe_allow_html=True)

user_input = st.text_area("Mesajını yaz:", height=100)
if st.button("🚀 Gönder"):
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        cevap = ai_cevap(st.session_state.messages, isim, user_input)
        st.session_state.messages.append({"role": "assistant", "content": cevap})
        st.rerun()
 
