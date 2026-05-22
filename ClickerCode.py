import streamlit as st
import random
import time

# =========================================================
# SETUP
# =========================================================
st.set_page_config(page_title="Asian Life Simulator", layout="centered")

WORLD_SIZE = 11

PRESSURE_INTERVAL = 180   # every 3 minutes
PRESSURE_DURATION = 120   # 2 minutes

# =========================================================
# INIT STATE
# =========================================================
def init():
    defaults = {
        "x": 5,
        "y": 5,

        "iq": 50,
        "stress": 20,
        "happiness": 50,
        "money": 0,

        "grade": 70,  # academic performance score

        "message": "You were born into the system 🏫",

        # pressure system
        "pressure_active": False,
        "last_pressure_time": time.time(),
        "pressure_start_time": 0,
        "pressure_type": None,
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

# =========================================================
# ZONES
# =========================================================
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

    st.session_state.stress += 1
    st.session_state.message = "You moved."

# =========================================================
# ZONE DETECTION
# =========================================================
def get_zone():
    return zones.get((st.session_state.x, st.session_state.y), "🟫 Street")

# =========================================================
# PRESSURE EVENT SYSTEM (CORE GAME LOOP)
# =========================================================
def update_pressure_system():
    now = time.time()

    # START PRESSURE EVENT
    if not st.session_state.pressure_active:
        if now - st.session_state.last_pressure_time >= PRESSURE_INTERVAL:

            st.session_state.pressure_active = True
            st.session_state.pressure_start_time = now

            st.session_state.pressure_type = random.choice([
                "📚 Exam Week",
                "🧑‍🏫 Tuition Overload",
                "👨‍👩‍👧 Parental Expectations",
            ])

            st.session_state.message = f"⚠️ {st.session_state.pressure_type} has started!"

    # END PRESSURE EVENT
    else:
        if now - st.session_state.pressure_start_time >= PRESSURE_DURATION:
            st.session_state.pressure_active = False
            st.session_state.last_pressure_time = now
            st.session_state.pressure_type = None
            st.session_state.message = "Pressure period ended. You can breathe again."

# =========================================================
# PRESSURE EFFECTS (THIS IS THE "GAMEPLAY")
# =========================================================
def apply_pressure_effects():
    if not st.session_state.pressure_active:
        return

    p = st.session_state.pressure_type

    # passive stress increase
    st.session_state.stress += 0.3

    if p == "📚 Exam Week":
        st.session_state.iq += 0.2
        st.session_state.stress += 0.2
        st.session_state.grade += 0.3

    elif p == "🧑‍🏫 Tuition Overload":
        st.session_state.iq += 0.4
        st.session_state.money -= 0.1
        st.session_state.stress += 0.5

    elif p == "👨‍👩‍👧 Parental Expectations":
        st.session_state.stress += 0.7
        st.session_state.happiness -= 0.3

# =========================================================
# ACTIONS BY ZONE
# =========================================================
def actions():
    zone = get_zone()

    st.markdown("### 🎮 Actions")

    if zone == "🏠 Home":
        if st.button("😴 Rest"):
            st.session_state.happiness += 5
            st.session_state.stress -= 5
            st.session_state.message = "You rested at home."
            st.rerun()

        if st.button("📖 Self Study"):
            st.session_state.iq += 2
            st.session_state.stress += 3
            st.session_state.grade += 1
            st.session_state.message = "You studied alone."
            st.rerun()

    elif zone == "🏫 School":
        if st.button("📝 Attend Class"):
            st.session_state.grade += 3
            st.session_state.stress += 2
            st.session_state.message = "You attended school."
            st.rerun()

    elif zone == "📚 Tuition":
        if st.button("📚 Extra Study"):
            st.session_state.iq += 5
            st.session_state.stress += 6
            st.session_state.grade += 4
            st.session_state.message = "Tuition grind activated."
            st.rerun()

    elif zone == "🌳 Park":
        if st.button("😌 Relax"):
            st.session_state.happiness += 10
            st.session_state.stress -= 10
            st.session_state.message = "You recovered mentally."
            st.rerun()

    elif zone == "🏙️ City":
        if st.button("💼 Part-time Job"):
            earn = random.randint(20, 80)
            st.session_state.money += earn
            st.session_state.stress += 5
            st.session_state.happiness -= 2
            st.session_state.message = f"You earned ${earn}"
            st.rerun()

# =========================================================
# MAP
# =========================================================
def draw_map():
    grid = ""

    for y in range(WORLD_SIZE):
        for x in range(WORLD_SIZE):

            if x == st.session_state.x and y == st.session_state.y:
                grid += "🧍"

            elif st.session_state.pressure_active and random.random() < 0.02:
                grid += "⚠️"

            elif (x, y) in zones:
                grid += "🏫"

            else:
                grid += "⬜"

        grid += "\n"

    return grid

# =========================================================
# GAME LOOP
# =========================================================
update_pressure_system()
apply_pressure_effects()

# =========================================================
# UI
# =========================================================
st.title("🎓 Asian Life Simulator")

st.subheader(f"📍 Location: {get_zone()}")
st.write(st.session_state.message)

if st.session_state.pressure_active:
    st.error(f"⚠️ ACTIVE: {st.session_state.pressure_type}")
else:
    st.success("🙂 Normal life period")

st.text(draw_map())

# =========================================================
# CONTROLS
# =========================================================
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
# ACTIONS
# =========================================================
actions()

# =========================================================
# STATS
# =========================================================
st.markdown("---")

c1, c2, c3, c4 = st.columns(4)
c1.metric("🧠 IQ", round(st.session_state.iq))
c2.metric("😰 Stress", round(st.session_state.stress))
c3.metric("😊 Happiness", round(st.session_state.happiness))
c4.metric("📊 Grade", round(st.session_state.grade))

st.metric("💰 Money", round(st.session_state.money))

# =========================================================
# ENDINGS
# =========================================================
if st.session_state.grade >= 150:
    st.success("🎓 Top Student Ending Unlocked")

elif st.session_state.stress >= 120:
    st.error("💥 Burnout Ending")

elif st.session_state.happiness <= 10:
    st.warning("😐 Empty Life Ending")

elif st.session_state.money >= 500:
    st.success("💼 Financial Stability Ending")
