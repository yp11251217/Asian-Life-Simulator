import streamlit as st
import time
import json
from pathlib import Path

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Cookie Clicker",
    page_icon="🍪",
    layout="centered"
)

SAVE_FILE = "cookie_save.json"

# -----------------------------
# SAVE / LOAD
# -----------------------------
def load_game():
    if Path(SAVE_FILE).exists():
        with open(SAVE_FILE, "r") as f:
            return json.load(f)

    return {
        "cookies": 0,
        "cookies_per_click": 1,
        "auto_clickers": 0,
        "farms": 0,
        "last_tick": time.time()
    }

def save_game():
    data = {
        "cookies": st.session_state.cookies,
        "cookies_per_click": st.session_state.cookies_per_click,
        "auto_clickers": st.session_state.auto_clickers,
        "farms": st.session_state.farms,
        "last_tick": time.time()
    }

    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

# -----------------------------
# INITIALIZE SESSION
# -----------------------------
if "initialized" not in st.session_state:
    game = load_game()

    st.session_state.cookies = game["cookies"]
    st.session_state.cookies_per_click = game["cookies_per_click"]
    st.session_state.auto_clickers = game["auto_clickers"]
    st.session_state.farms = game["farms"]
    st.session_state.last_tick = game["last_tick"]

    st.session_state.initialized = True

# -----------------------------
# PASSIVE INCOME
# -----------------------------
now = time.time()
elapsed = now - st.session_state.last_tick

income_per_second = (
    st.session_state.auto_clickers * 1 +
    st.session_state.farms * 5
)

st.session_state.cookies += income_per_second * elapsed
st.session_state.last_tick = now

# -----------------------------
# STYLING
# -----------------------------
st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 60px;
    font-weight: bold;
}

.cookie-display {
    text-align: center;
    font-size: 42px;
    margin-bottom: 20px;
}

div.stButton > button:first-child {
    font-size: 80px;
    border-radius: 50%;
    height: 180px;
    width: 180px;
    border: none;
    background-color: #d2691e;
    transition: 0.1s;
}

div.stButton > button:first-child:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown(
    "<div class='main-title'>🍪 Cookie Clicker</div>",
    unsafe_allow_html=True
)

st.markdown(
    f"<div class='cookie-display'>{int(st.session_state.cookies)} Cookies</div>",
    unsafe_allow_html=True
)

# -----------------------------
# COOKIE BUTTON
# -----------------------------
c1, c2, c3 = st.columns([1,2,1])

with c2:
    if st.button("🍪"):
        st.session_state.cookies += st.session_state.cookies_per_click
        save_game()
        st.rerun()

# -----------------------------
# INFO
# -----------------------------
st.write(f"Cookies Per Click: {st.session_state.cookies_per_click}")
st.write(f"Passive Income: {income_per_second}/sec")

# -----------------------------
# SHOP
# -----------------------------
st.subheader("🛒 Shop")

# AUTO CLICKER
auto_cost = 50 + (st.session_state.auto_clickers * 20)

if st.button(f"Buy Auto Clicker ({auto_cost})"):
    if st.session_state.cookies >= auto_cost:
        st.session_state.cookies -= auto_cost
        st.session_state.auto_clickers += 1
        save_game()
        st.rerun()

# FARM
farm_cost = 250 + (st.session_state.farms * 100)

if st.button(f"Buy Farm ({farm_cost})"):
    if st.session_state.cookies >= farm_cost:
        st.session_state.cookies -= farm_cost
        st.session_state.farms += 1
        save_game()
        st.rerun()

# CLICK UPGRADE
upgrade_cost = 100 + (st.session_state.cookies_per_click * 50)

if st.button(f"Upgrade Click Power ({upgrade_cost})"):
    if st.session_state.cookies >= upgrade_cost:
        st.session_state.cookies -= upgrade_cost
        st.session_state.cookies_per_click += 1
        save_game()
        st.rerun()

# -----------------------------
# AUTO SAVE
# -----------------------------
save_game()

# -----------------------------
# OPTIONAL AUTO REFRESH
# -----------------------------
st.caption("Refresh page occasionally to update passive income.")
