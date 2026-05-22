import streamlit as st
import random

# =========================================================
# GTA-STYLE LIFE SIMULATOR (MAP VERSION)
# =========================================================

st.set_page_config(page_title="Life Simulator GTA Map", page_icon="🗺️", layout="centered")

# =========================================================
# INIT STATE
# =========================================================
def init():
    defaults = {
        "location": "Home",
        "age": 6,
        "grade": 1,
        "intelligence": 50,
        "happiness": 50,
        "energy": 100,
        "stress": 20,
        "money": 0,
        "reputation": 0,
        "inventory": [],
        "message": "You wake up at home. Expectations await.",
        "unlocked": {
            "Home": True,
            "School": True,
            "Tuition Center": False,
            "Park": False,
            "Mall": False,
            "City": False
        },
        "day": 1
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

# =========================================================
# MAP SYSTEM
# =========================================================
MAP = {
    "Home": {
        "desc": "Strict household. Study or suffer emotional damage.",
        "study": (10, -10, 5),
        "sleep": (20, 5, 0)
    },
    "School": {
        "desc": "Competitive school environment.",
        "study": (15, -5, 10),
        "exam": (25, -15, 20)
    },
    "Tuition Center": {
        "desc": "Extra classes because 'not enough'.",
        "study": (20, -10, 15)
    },
    "Park": {
        "desc": "Rare happiness zone.",
        "relax": (10, 20, -10)
    },
    "Mall": {
        "desc": "Spend money for temporary happiness.",
        "shop": (0, 15, 0)
    },
    "City": {
        "desc": "Late game unlocked area.",
        "job": (30, -10, 25)
    }
}

# =========================================================
# UI
# =========================================================
st.title("🗺️ GTA: Academic Life Edition")

st.write(f"Location: {st.session_state.location}")
st.write(st.session_state.message)

# =========================================================
# MAP DISPLAY
# =========================================================
st.subheader("📍 Map")

cols = st.columns(3)
locations = list(MAP.keys())

for i, loc in enumerate(locations):
    col = cols[i % 3]
    locked = not st.session_state.unlocked.get(loc, False)

    with col:
        if locked:
            st.button(f"🔒 {loc}", disabled=True)
        else:
            if st.button(f"📍 {loc}"):
                st.session_state.location = loc
                st.session_state.message = f"You moved to {loc}"
                st.rerun()

# =========================================================
# ACTIONS
# =========================================================
st.subheader("🎮 Actions")

loc = st.session_state.location
area = MAP[loc]

col1, col2, col3 = st.columns(3)

if "study" in area:
    if col1.button("📖 Study"):
        iq, hap, stress = area["study"]
        st.session_state.intelligence += iq
        st.session_state.happiness += hap
        st.session_state.stress += stress
        st.session_state.message = "You studied. Expectations increased."
        st.rerun()

if "sleep" in area:
    if col2.button("😴 Rest"):
        e, h, s = area["sleep"]
        st.session_state.energy += e
        st.session_state.happiness += h
        st.session_state.stress += s
        st.session_state.message = "You rested."
        st.rerun()

if "relax" in area:
    if col2.button("😴 Relax"):
        e, h, s = area["relax"]
        st.session_state.energy += e
        st.session_state.happiness += h
        st.session_state.stress += s
        st.session_state.message = "You relaxed at the park."
        st.rerun()

if "exam" in area:
    if col3.button("📝 Exam"):
        iq, hap, stress = area["exam"]
        st.session_state.intelligence += iq
        st.session_state.happiness += hap
        st.session_state.stress += stress
        st.session_state.message = "Exam completed. Emotional damage increased."
        st.rerun()

if "shop" in area:
    if col3.button("🛍️ Shop"):
        st.session_state.happiness += 15
        st.session_state.money -= 10
        st.session_state.message = "You bought temporary happiness."
        st.rerun()

if "job" in area:
    if col3.button("💼 Work"):
        st.session_state.money += 50
        st.session_state.stress += 20
        st.session_state.message = "You worked a stressful job."
        st.rerun()

# =========================================================
# NEXT DAY PROGRESSION
# =========================================================
st.markdown("---")

if st.button("🎂 Next Day"):
    st.session_state.day += 1
    st.session_state.energy -= 5

    st.session_state.message = random.choice([
        "Parents compare you to cousin.",
        "Extra tutoring added.",
        "You feel burnout.",
        "Another strict day passed.",
        "You survive."
    ])

    if st.session_state.intelligence > 80:
        st.session_state.unlocked["Tuition Center"] = True
    if st.session_state.intelligence > 120:
        st.session_state.unlocked["Park"] = True
    if st.session_state.intelligence > 150:
        st.session_state.unlocked["Mall"] = True
    if st.session_state.intelligence > 180:
        st.session_state.unlocked["City"] = True

    st.rerun()

# =========================================================
# STATS
# =========================================================
st.markdown("---")

c1, c2, c3, c4 = st.columns(4)
c1.metric("IQ", st.session_state.intelligence)
c2.metric("Happy", st.session_state.happiness)
c3.metric("Stress", st.session_state.stress)
c4.metric("Money", st.session_state.money)

# =========================================================
# ENDINGS
# =========================================================
if st.session_state.intelligence > 200:
    st.success("Doctor ending unlocked")
elif st.session_state.intelligence > 170:
    st.success("Engineer ending unlocked")
elif st.session_state.intelligence < 60:
    st.error("EMOTIONAL DAMAGE ENDING")
