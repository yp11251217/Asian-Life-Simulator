import streamlit as st
import random

# =========================================================
# SETUP
# =========================================================
st.set_page_config(page_title="GTA Mario Life Sim", page_icon="🗺️", layout="centered")

# =========================================================
# INIT STATE
# =========================================================
def init():
    defaults = {
        "x": 5,
        "y": 5,
        "iq": 50,
        "happiness": 50,
        "stress": 20,
        "energy": 100,
        "money": 0,
        "message": "You spawned in the world.",
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

# =========================================================
# WORLD SETTINGS (GRID MAP)
# =========================================================
WORLD_SIZE = 11

zones = {
    (5, 5): "🏠 Home",
    (2, 2): "🏫 School",
    (8, 2): "📚 Tuition",
    (2, 8): "🌳 Park",
    (8, 8): "🏙️ City",
}

# =========================================================
# MOVE SYSTEM
# =========================================================
def move(dx, dy):
    st.session_state.x = max(0, min(WORLD_SIZE - 1, st.session_state.x + dx))
    st.session_state.y = max(0, min(WORLD_SIZE - 1, st.session_state.y + dy))

    st.session_state.energy -= 1

    st.session_state.message = "You moved."

# =========================================================
# CURRENT LOCATION DETECTION
# =========================================================
def get_zone():
    return zones.get((st.session_state.x, st.session_state.y), "🟫 Street")

# =========================================================
# BACKGROUND STYLE (FAKE GAME LOOK)
# =========================================================
st.markdown("""
<style>
body {
    background-color: #1e1e2f;
    color: white;
}

.game-title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #ffd166;
}

.map {
    font-family: monospace;
    font-size: 18px;
    line-height: 18px;
    text-align: center;
    background: #111;
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# TITLE
# =========================================================
st.markdown("<div class='game-title'>🗺️ GTA MARIO LIFE SIM</div>", unsafe_allow_html=True)

st.write("Location:", get_zone())
st.write(st.session_state.message)

# =========================================================
# RENDER GRID MAP (MARIO STYLE)
# =========================================================
def draw_map():
    grid = ""

    for y in range(WORLD_SIZE):
        for x in range(WORLD_SIZE):

            if x == st.session_state.x and y == st.session_state.y:
                grid += "🧍"
            elif (x, y) in zones:
                grid += "🏠"
            else:
                grid += "⬜"
        grid += "\n"

    return grid

st.markdown("### 🗺️ World Map")
st.text(draw_map())

# =========================================================
# MOVEMENT CONTROLS
# =========================================================
st.markdown("### 🎮 Controls")

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("⬅️"):
        move(-1, 0)
        st.rerun()

    if st.button("⬇️"):
        move(0, 1)
        st.rerun()

with c2:
    if st.button("⬆️"):
        move(0, -1)
        st.rerun()

with c3:
    if st.button("➡️"):
        move(1, 0)
        st.rerun()

# =========================================================
# ACTIONS BASED ON LOCATION
# =========================================================
zone = get_zone()

st.markdown("### 🎮 Actions")

if zone == "🏠 Home":
    if st.button("📖 Study"):
        st.session_state.iq += 5
        st.session_state.stress += 5
        st.session_state.message = "You studied at home. Pressure increased."
        st.rerun()

    if st.button("😴 Sleep"):
        st.session_state.energy += 20
        st.session_state.message = "You slept at home."
        st.rerun()

elif zone == "🏫 School":
    if st.button("📝 Exam"):
        st.session_state.iq += 10
        st.session_state.stress += 15
        st.session_state.message = "You took an exam. Pain increased."
        st.rerun()

elif zone == "📚 Tuition":
    if st.button("📚 Extra Study"):
        st.session_state.iq += 15
        st.session_state.stress += 20
        st.session_state.message = "Tuition class activated: EMOTIONAL DAMAGE."
        st.rerun()

elif zone == "🌳 Park":
    if st.button("😌 Relax"):
        st.session_state.happiness += 20
        st.session_state.stress -= 10
        st.session_state.message = "You feel slightly human again."
        st.rerun()

elif zone == "🏙️ City":
    if st.button("💼 Work Job"):
        st.session_state.money += 50
        st.session_state.stress += 15
        st.session_state.message = "You worked in the city."

# =========================================================
# STATS
# =========================================================
st.markdown("---")

c1, c2, c3, c4 = st.columns(4)
c1.metric("IQ", st.session_state.iq)
c2.metric("Happy", st.session_state.happiness)
c3.metric("Stress", st.session_state.stress)
c4.metric("Energy", st.session_state.energy)

# =========================================================
# END GAME
# =========================================================
if st.session_state.iq > 200:
    st.success("Doctor Ending Unlocked")
elif st.session_state.iq < 40:
    st.error("EMOTIONAL DAMAGE ENDING 💀")
