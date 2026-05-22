import streamlit as st
import random

# =========================================================
# SETUP
# =========================================================
st.set_page_config(page_title="2D Life Game", layout="centered")

WORLD_SIZE = 15
VIEW_SIZE = 7  # camera window size

zones = {
    (5, 5): "🏠 Home",
    (2, 2): "🏫 School",
    (10, 3): "📚 Tuition",
    (3, 10): "🌳 Park",
    (12, 12): "🏙️ City",
}

zone_icons = {
    "🏠 Home": "🏠",
    "🏫 School": "🏫",
    "📚 Tuition": "📚",
    "🌳 Park": "🌳",
    "🏙️ City": "🏙️",
}

# =========================================================
# INIT STATE
# =========================================================
def init():
    defaults = {
        "x": 7,
        "y": 7,
        "iq": 50,
        "happiness": 50,
        "stress": 20,
        "energy": 100,
        "money": 0,
        "message": "Spawned in world 🌍",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

# =========================================================
# MOVEMENT
# =========================================================
def move(dx, dy):
    if st.session_state.energy <= 0:
        st.session_state.message = "Too tired to move 😴"
        return

    st.session_state.x = max(0, min(WORLD_SIZE - 1, st.session_state.x + dx))
    st.session_state.y = max(0, min(WORLD_SIZE - 1, st.session_state.y + dy))

    st.session_state.energy -= 1
    st.session_state.message = f"Moved to ({st.session_state.x}, {st.session_state.y})"

# =========================================================
# ZONE DETECTION
# =========================================================
def get_zone(x, y):
    return zones.get((x, y), "🟫 Street")

# =========================================================
# CAMERA VIEW (IMPORTANT FOR GAME FEEL)
# =========================================================
def get_view():
    half = VIEW_SIZE // 2
    cx, cy = st.session_state.x, st.session_state.y

    min_x = max(0, cx - half)
    max_x = min(WORLD_SIZE - 1, cx + half)
    min_y = max(0, cy - half)
    max_y = min(WORLD_SIZE - 1, cy + half)

    return min_x, max_x, min_y, max_y

# =========================================================
# RENDER MAP
# =========================================================
def draw_map():
    min_x, max_x, min_y, max_y = get_view()

    grid = ""

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):

            if x == st.session_state.x and y == st.session_state.y:
                grid += "🧍"
            elif (x, y) in zones:
                grid += zone_icons[zones[(x, y)]]
            else:
                grid += "⬜"
        grid += "\n"

    return grid

# =========================================================
# UI
# =========================================================
st.title("🗺️ 2D Life Game (Streamlit Edition)")

st.subheader(f"📍 Location: {get_zone(st.session_state.x, st.session_state.y)}")
st.write(st.session_state.message)

st.markdown("### 🗺️ World")
st.text(draw_map())

# =========================================================
# CONTROLS (GAMEPAD STYLE)
# =========================================================
st.markdown("### 🎮 Controls")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⬅️ Left"):
        move(-1, 0)
        st.rerun()

    if st.button("⬇️ Down"):
        move(0, 1)
        st.rerun()

with col2:
    if st.button("⬆️ Up"):
        move(0, -1)
        st.rerun()

with col3:
    if st.button("➡️ Right"):
        move(1, 0)
        st.rerun()

# =========================================================
# ACTIONS
# =========================================================
zone = get_zone(st.session_state.x, st.session_state.y)

st.markdown("### ⚡ Actions")

if zone == "🏠 Home":
    if st.button("😴 Sleep"):
        st.session_state.energy += 30
        st.session_state.message = "You recovered energy"
        st.rerun()

elif zone == "🏫 School":
    if st.button("📝 Study"):
        st.session_state.iq += 10
        st.session_state.stress += 10
        st.session_state.message = "Studying hard..."
        st.rerun()

elif zone == "🌳 Park":
    if st.button("😌 Relax"):
        st.session_state.happiness += 20
        st.session_state.stress -= 10
        st.session_state.message = "You feel better"
        st.rerun()

elif zone == "🏙️ City":
    if st.button("💼 Work"):
        earn = random.randint(20, 80)
        st.session_state.money += earn
        st.session_state.stress += 10
        st.session_state.message = f"You earned ${earn}"
        st.rerun()

# =========================================================
# STATS
# =========================================================
st.markdown("---")

c1, c2, c3, c4 = st.columns(4)
c1.metric("IQ", st.session_state.iq)
c2.metric("Happiness", st.session_state.happiness)
c3.metric("Stress", st.session_state.stress)
c4.metric("Energy", st.session_state.energy)

# =========================================================
# ENDINGS
# =========================================================
if st.session_state.iq >= 150:
    st.success("🧠 GENIUS ENDING UNLOCKED")
elif st.session_state.stress >= 120:
    st.error("💀 BURNOUT ENDING")
elif st.session_state.energy <= 0:
    st.error("😴 YOU PASSED OUT")
