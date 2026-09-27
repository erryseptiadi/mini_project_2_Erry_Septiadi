import os

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
from pathlib import Path
from PIL import Image


from rag_chatbot import (
    KNOWLEDGE_DIR,
    SYSTEM_PROMPT_PATH,
    TOP_K,
    buat_model,
    muat_dokumen,
    bangun_vectorstore,
    muat_system_prompt,
    buat_rag_chain,
)


# ============================================================
# 1. PENGATURAN HALAMAN
# ============================================================
# Wajib jadi perintah Streamlit pertama: judul tab browser dan ikonnya.

st.set_page_config(
    page_title="Asisten Sadar Lemari",
    page_icon=":material/gavel:",
)

# ============================================================
# 2. CEK API KEY
# ============================================================
# Di laptop, GROQ_API_KEY dibaca dari file .env.
# Di Streamlit Cloud, GROQ_API_KEY diisi lewat menu Secrets, dan Streamlit
# otomatis menjadikannya environment variable. Jadi kode yang sama ini
# jalan di dua tempat tanpa perlu diubah.

load_dotenv()
if not os.getenv("GROQ_API_KEY"):
    st.error(
        "GROQ_API_KEY belum diisi. Cek file .env (di laptop) "
        "atau menu Secrets (di Streamlit Cloud)."
    )
    st.stop()

# ============================================================
# 3. SIAPKAN MESIN CHATBOT (sekali saja, lalu disimpan)
# ============================================================
# Streamlit menjalankan ulang SELURUH file ini dari atas setiap kali
# pengguna berinteraksi (misalnya mengirim pertanyaan).
# @st.cache_resource membuat fungsi di bawah ini cukup dijalankan SEKALI.
# Hasilnya disimpan, lalu dipakai ulang, sehingga dokumen tidak dimuat
# ulang dan vector store tidak dibangun ulang di setiap pertanyaan.

@st.cache_resource(show_spinner="Menyiapkan chatbot, mohon tunggu sebentar...")
def siapkan_chatbot():
    model = buat_model()
    dokumen = muat_dokumen(KNOWLEDGE_DIR)
    vectorstore = bangun_vectorstore(dokumen)
    retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})
    system_prompt = muat_system_prompt(SYSTEM_PROMPT_PATH)
    return buat_rag_chain(retriever, model, system_prompt)


rag_chain = siapkan_chatbot()


# ============================================================
# 4. BUKU CATATAN PERCAKAPAN
# ============================================================
# st.session_state adalah tempat menyimpan data yang tidak ikut hilang
# saat file ini dijalankan ulang. Di sini dipakai untuk mencatat riwayat
# percakapan: siapa yang bicara ("user" atau "assistant") dan isinya.
# Sama saja dengan menjaga percakapan terus muncul di atas chat baru

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

# ============================================================
# 5. TAMPILAN
# ============================================================
import streamlit as st

# Inject CSS untuk Tampilan UI/UX Modern & Kekinian
st.markdown("""
    <style>
    /* 1. Import Font Modern (Plus Jakarta Sans) */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* 2. Style Gelembung Chat User (Aksen Oranye Brand) */
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #241A15 !important; /* Touch/tint oranye gelap */
        border: 1px solid #E86C38 !important;   /* Border oranye khas Sadar Lemari */
        border-radius: 18px 18px 4px 18px !important;
        padding: 12px 16px !important;
        margin-bottom: 12px !important;
    }

    /* 3. Style Gelembung Chat Asisten (Clean & Modern) */
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background-color: #1A1D24 !important;
        border: 1px solid #2A2F3A !important;
        border-radius: 18px 18px 18px 4px !important;
        padding: 14px 18px !important;
        margin-bottom: 16px !important;
    }

    /* 4. Kustomisasi Chat Input Field */
    .stChatInputContainer textarea {
        background-color: #1E2228 !important;
        color: #F3F4F6 !important;
        border-radius: 14px !important;
        border: 1px solid #343A46 !important;
        font-size: 0.95rem !important;
    }
    
    .stChatInputContainer textarea:focus {
        border-color: #E97435 !important; /* Focus ring warna oranye */
        box-shadow: 0 0 8px rgba(232, 108, 56, 0.3) !important;
    }

    .sari-header-title {
        color: #F5F5F5;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 34px;
        font-weight: 700;
        line-height: 1.2;
        margin: 0 0 8px;
    }

    .sari-header-title span {
        color: #E97435;
    }

    .sari-header-subtitle {
        color: #C7C7C7;
        font-size: 15px;
        line-height: 1.55;
        margin: 0;
    }

    /* 5. Styling Tombol Quick Prompts */
    div.stButton > button {
        background-color: #1E2228 !important;
        color: #E0E0E0 !important;
        border: 1px solid #2D323C !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        text-align: left !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important;
    }
    
    div.stButton > button:hover {
        border-color: #E97435 !important;
        color: #E97435 !important;
        background-color: #252A32 !important;
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# from pathlib import Path
# from PIL import Image

ASSETS_DIR = Path(__file__).parent / "assets"
ICON_PATH = ASSETS_DIR / "icon_sl.png"
USER_ICON_PATH = ASSETS_DIR / "user_talk.png"
LOGO_PATH = ASSETS_DIR / "logo_sl.png"
TALK_PATH = ASSETS_DIR / "user_talk.png"

icon_image = Image.open(ICON_PATH) if ICON_PATH.exists() else "🧵"
user_icon_image = Image.open(USER_ICON_PATH) if USER_ICON_PATH.exists() else "👤"

with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=250)

    if st.button("MULAI OBROLAN BARU 💬"):
            st.session_state.riwayat = []
    
    st.caption("🔒 Jawaban berbasis dokumen internal resmi Sadar Lemari.")


    st.header("TENTANG SADAR LEMARI")
    st.write(
        "Inisiatif sosial dan lingkungan untuk pengelolaan limbah tekstil secara bertanggung jawab, sekaligus mengajak kita lebih bijak dalam memiliki dan menggunakan pakaian."
    )

    # --- MAIN CHAT AREA ---
col1, col2 = st.columns([1, 6])
with col1:
    if ICON_PATH.exists():
        st.image(str(ICON_PATH), width=68)
with col2:
    st.markdown(
        """
        <div class="sari-header-title">HAI! AKU <span>ASRI</span> 👋</div>
        <p class="sari-header-subtitle">
            Asisten virtual Sadar Lemari yang siap jadi teman ngobrol kamu seputar Sadar Lemari,
            pengelolaan limbah tekstil, dan sirkular ekonomi. Yuk, tanya Asri! 🌱♻️
        </p>
        """,
        unsafe_allow_html=True,
    )


# Salam pembuka, selalu tampil paling atas.
st.markdown("#### **💬 Mau tanya apa, Kak?**")
col1, col2 = st.columns(2)
with col1:
    if st.button("📦 Gimana cara drop-off atau kirim pakaian?"):
        st.session_state.selected_prompt = "Bagaimana cara mengirim pakaian ke Sadar Lemari?"
    if st.button("👕 Limbah Tekstil apa saja yang diterima?"):
        st.session_state.selected_prompt = "Pakaian tidak layak pakai, celana dalam, bisa diterima Sadar Lemari?"
with col2:
    if st.button("📍 Drop Point Sadar Lemari ada di mana aja?"):
        st.session_state.selected_prompt = "Lokasi drop point Sadar Lemari?"
    if st.button("🌏 Apa aja dampak limbah tekstil bagi lingkungan?"):
        st.session_state.selected_prompt = "Dampak Lingkungan Limbah Tekstil?" 

# Render Chat History
for msg in st.session_state.riwayat:
    avatar = user_icon_image if msg["role"] == "user" else icon_image
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["isi"])

# ============================================================
# 6. TANYA JAWAB
# ============================================================

pertanyaan_chat = st.chat_input("💬 TANYA ASRI...")
pertanyaan = st.session_state.pop("selected_prompt", None) or pertanyaan_chat

if pertanyaan:
    # Tampilkan pertanyaan, lalu catat ke buku catatan.
    with st.chat_message("user", avatar=user_icon_image):
        st.markdown(pertanyaan)
    st.session_state.riwayat.append({"role": "user", "isi": pertanyaan})

    # Minta jawaban ke mesin RAG. .stream() + st.write_stream() membuat
    # jawaban muncul bertahap, kata demi kata, seperti sedang diketik.
    with st.chat_message("assistant", avatar=icon_image):
        with st.spinner("Bestie! Tunggu ya..."):
            jawaban = st.write_stream(rag_chain.stream(pertanyaan))
    st.session_state.riwayat.append({"role": "assistant", "isi": jawaban})

# Auto scroll
    html_scroll = """
        <div data-chat-turn="__CHAT_TURN__"></div>
        <script>
        const scrollToChatBottom = () => {
            const parentDocument = window.parent.document;
            const target = parentDocument.querySelector(
                '[data-testid="stAppScrollToBottomContainer"]'
            );
            target?.scrollTo({ top: target.scrollHeight, behavior: 'smooth' });
        };
        requestAnimationFrame(() => requestAnimationFrame(scrollToChatBottom));
        setTimeout(scrollToChatBottom, 250);
        </script>
        """
    components.html(
        html_scroll.replace("__CHAT_TURN__", str(len(st.session_state.riwayat))),
        height=0,
    )