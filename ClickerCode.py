import streamlit as st
import time
import random

st.set_page_config(page_title="Neon Reaction Game", page_icon="⚡", layout="centered")

# ---- Styling ----
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
}
.stApp {
    background: transparent;
    color: white;
}
.game-card {
    background: rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
    backdrop-filter: blur(10px);
}
.title {
    font-size: 40px;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, #00ffe0, #ff00ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.sub {
    text-align:center;
    opacity: 0.8;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---- State ----
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "waiting" not in st.session_state:
    st.session_state.waiting = False
if "score" not in st.session_state:
    st.session_state.score = []
if "color" not in st.session_state:
    st.session_state.color = "red"

# ---- UI ----
st.markdown("<div class='game-card'>", unsafe_allow_html=True)
st.markdown("<div class='title'>⚡ Neon Reaction Game</div>", unsafe_allow_html=True)
st.markdown("<div class='sub'>Click as fast as you can when it turns GREEN</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)


def start_game():
    st.session_state.waiting = True
    st.session_state.color = "red"
    st.session_state.start_time = None
    st.session_state.delay = random.uniform(1.5, 4.0)
    st.session_state.trigger_time = time.time() + st.session_state.delay


def click_button():
    now = time.time()
    if st.session_state.start_time is None:
        st.session_state.score.append("Too early ❌")
    else:
        reaction = now - st.session_state.start_time
        st.session_state.score.append(f"{reaction:.3f} sec ⚡")
    st.session_state.waiting = False
    st.session_state.start_time = None


with col1:
    if st.button("Start 🚀"):
        start_game()

with col2:
    if st.button("Click ⚡", disabled=not st.session_state.waiting):
        click_button()

# ---- Game logic ----
if st.session_state.waiting:
    now = time.time()
    if st.session_state.start_time is None and now >= st.session_state.trigger_time:
        st.session_state.start_time = time.time()
        st.session_state.color = "green"

# ---- Visual indicator ----
color = st.session_state.color
st.markdown(
    f"""
    <div style='margin-top:20px; height:120px; border-radius:20px;
    background:{color}; display:flex; align-items:center; justify-content:center;
    font-size:24px; font-weight:bold;'>
    {"CLICK NOW! ⚡" if color=="green" else "WAIT..."}
    </div>
    """,
    unsafe_allow_html=True
)

# ---- Scoreboard ----
st.markdown("### Score History")
if st.session_state.score:
    for s in st.session_state.score[-8:][::-1]:
        st.write(s)
else:
    st.write("No scores yet")

st.markdown("</div>", unsafe_allow_html=True)
