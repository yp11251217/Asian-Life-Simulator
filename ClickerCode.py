import streamlit as st
import random
import time

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(page_title="Asian Life Simulator", layout="centered")

WORLD_SIZE = 11

PRESSURE_INTERVAL = 180
PRESSURE_DURATION = 120

# =========================================================
# STYLE
# =========================================================
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        background-color: #0e1117;
        color: white;
    }

    .stButton>button {
        border-radius: 10px;
        border: 1px solid #444;
        background: #1e1e1e;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# INIT
# =========================================================
def init():
    defaults = {
        "x": 5,
        "y": 5,

        "iq": 50,
        "stress": 20,
        "happiness": 50,
        "money": 0,
        "grade": 70,

        # survival stats
        "hunger": 100,
        "hp": 100,

        "message": "You were born into the system 🏫",

        # pressure system
        "pressure_active": False,
        "last_pressure_time": time.time(),
        "pressure_start_time": 0,
        "pressure_type": None,

        # food positions
        "food": [
            (1, 1), (3, 7), (6, 2), (9, 9), (2, 8)
        ],
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
# CLAMP
# =========================================================
def clamp():
    st.session_state.iq = max(0, min(200, st.session_state.iq))
    st.session_state.stress = max(0, min(200, st.session_state.stress))
    st.session_state.happiness = max(0, min(100, st.session_state.happiness))
    st.session_state.grade = max(0, min(200, st.session_state.grade))

    st.session_state.hunger = max(0, min(100, st.session_state.hunger))
    st.session_state.hp = max(0, min(100, st.session_state.hp))

# =========================================================
# MOVE
# =========================================================
def move(dx, dy):
    st.session_state.x = max(0, min(WORLD_SIZE - 1, st.session_state.x + dx))
    st.session_state.y = max(0, min(WORLD_SIZE - 1, st.session_state.y + dy))

    st.session_state.stress += 1
    st.session_state.hunger -= 1
    st.session_state.message = "You moved."

    check_food()

# =========================================================
# FOOD PICKUP
# =========================================================
def check_food():
    pos = (st.session_state.x, st.session_state.y)

    if pos in st.session_state.food:
        st.session_state.food.remove(pos)
        heal = random.randint(10, 30)

        st.session_state.hunger += heal
        st.session_state.hp += heal // 2

        st.session_state.message = f"🍜 You ate food (+{heal} hunger)"
        st.rerun()

# =========================================================
# ZONE
# =========================================================
def get_zone():
    return zones.get((st.session_state.x, st.session_state.y), "🟫 Street")

# =========================================================
# PRESSURE SYSTEM
# =========================================================
def update_pressure_system():
    now = time.time()

    if not st.session_state.pressure_active:
        if now - st.session_state.last_pressure_time >= PRESSURE_INTERVAL:
            st.session_state.pressure_active = True
            st.session_state.pressure_start_time = now

            st.session_state.pressure_type = random.choice([
                "📚 Exam Week",
                "🧑‍🏫 Tuition Overload",
                "👨‍👩‍👧 Parental Expectations",
            ])

            st.session_state.message = f"⚠️ {st.session_state.pressure_type} started!"

    else:
        if now - st.session_state.pressure_start_time >= PRESSURE_DURATION:
            st.session_state.pressure_active = False
            st.session_state.last_pressure_time = now
            st.session_state.pressure_type = None

# =========================================================
# EFFECTS LOOP
# =========================================================
def apply_effects():
    if st.session_state.pressure_active:
        st.session_state.stress += 0.5

    # hunger decay (core survival loop)
    st.session_state.hunger -= 0.2

    # HP logic
    if st.session_state.hunger < 20:
        st.session_state.hp -= 0.5

    if st.session_state.hunger <= 0:
        st.session_state.hp -= 1

    # pressure effects
    if st.session_state.pressure_type == "📚 Exam Week":
        st.session_state.iq += 0.2
        st.session_state.grade += 0.3

    elif st.session_state.pressure_type == "🧑‍🏫 Tuition Overload":
        st.session_state.iq += 0.3
        st.session_state.stress += 0.4

    elif st.session_state.pressure_type == "👨‍👩‍👧 Parental Expectations":
        st.session_state.happiness -= 0.3
        st.session_state.stress += 0.6

# =========================================================
# MAP
# =========================================================
def draw_map():
    grid = ""

    for y in range(WORLD_SIZE):
        for x in range(WORLD_SIZE):

            if (x, y) == (st.session_state.x, st.session_state.y):
                grid += "🧍"

            elif (x, y) in st.session_state.food:
                grid += "🍜"

            elif (x, y) in zones:
                grid += "🏫"

            else:
                grid += "⬜"

        grid += "\n"

    return grid

# =========================================================
# STAT CARD
# =========================================================
def stat_card(title, value, color):
    return f"""
    <div style="
        background:#1e1e1e;
        padding:12px;
        border-radius:12px;
        text-align:center;
        border:1px solid {color};
    ">
        <div style="color:#aaa">{title}</div>
        <div style="font-size:22px;font-weight:bold">{value}</div>
    </div>
    """

# =========================================================
# GAME LOOP
# =========================================================
update_pressure_system()
apply_effects()
clamp()

# =========================================================
# TITLE
# =========================================================
st.markdown(
    """
    <div style="text-align:center;padding:18px;background:#111;border-radius:15px">
        <h1>🎓 Asian Life Simulator</h1>
        <p style="color:#aaa">Now with survival mechanics</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# STATUS
# =========================================================
st.subheader(f"📍 {get_zone()}")

st.write(st.session_state.message)

# =========================================================
# SURVIVAL HUD
# =========================================================
st.markdown("### ❤️ Survival Stats")

c1, c2 = st.columns(2)
c1.progress(st.session_state.hunger / 100)
c2.progress(st.session_state.hp / 100)

st.write(f"🍗 Hunger: {int(st.session_state.hunger)}")
st.write(f"❤️ HP: {int(st.session_state.hp)}")

# =========================================================
# MAP
# =========================================================
st.markdown(f"<pre style='background:#111;padding:12px;border-radius:10px'>{draw_map()}</pre>", unsafe_allow_html=True)

# =========================================================
# MOVEMENT
# =========================================================
st.markdown("### 🧭 Move")

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
st.markdown("### 🎮 Actions")

zone = get_zone()

if zone == "🏠 Home":
    if st.button("😴 Rest"):
        st.session_state.hp += 5
        st.session_state.hunger -= 2
        st.rerun()

elif zone == "🏫 School":
    if st.button("📝 Study"):
        st.session_state.grade += 3
        st.session_state.stress += 2
        st.rerun()

elif zone == "📚 Tuition":
    if st.button("📚 Grind"):
        st.session_state.iq += 5
        st.session_state.hunger -= 5
        st.session_state.stress += 6
        st.rerun()

elif zone == "🌳 Park":
    if st.button("😌 Relax"):
        st.session_state.happiness += 10
        st.session_state.hunger -= 2
        st.rerun()

elif zone == "🏙️ City":
    if st.button("💼 Job"):
        earn = random.randint(20, 80)
        st.session_state.money += earn
        st.session_state.hunger -= 5
        st.rerun()

# =========================================================
# STATS HUD
# =========================================================
st.markdown("---")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(stat_card("🧠 IQ", round(st.session_state.iq), "#4CAF50"), unsafe_allow_html=True)
with c2:
    st.markdown(stat_card("😰 Stress", round(st.session_state.stress), "#FF4B4B"), unsafe_allow_html=True)
with c3:
    st.markdown(stat_card("😊 Happiness", round(st.session_state.happiness), "#FFD700"), unsafe_allow_html=True)
with c4:
    st.markdown(stat_card("📊 Grade", round(st.session_state.grade), "#00BFFF"), unsafe_allow_html=True)

st.metric("💰 Money", round(st.session_state.money))

# =========================================================
# ENDINGS
# =========================================================
st.markdown("---")

if st.session_state.hp <= 0:
    st.error("💀 TOTAL FAILURE ENDING")

elif st.session_state.happiness <= 5:
    st.warning("😐 EMOTIONAL DAMAGE ENDING")

elif st.session_state.grade >= 150:
    st.success("🎓 TOP STUDENT ENDING")

elif st.session_state.money >= 500:
    st.success("💼 FINANCIAL STABILITY ENDING")
