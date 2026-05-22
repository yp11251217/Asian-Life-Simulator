import streamlit as st
import random
import time

# -----------------------------
# INIT GAME STATE
# -----------------------------
if "player_pos" not in st.session_state:
    st.session_state.player_pos = 0

if "teacher_pos" not in st.session_state:
    st.session_state.teacher_pos = -8

if "level" not in st.session_state:
    st.session_state.level = 1

if "question" not in st.session_state:
    st.session_state.question = None

if "answer" not in st.session_state:
    st.session_state.answer = None

if "weapon" not in st.session_state:
    st.session_state.weapon = None

if "damage" not in st.session_state:
    st.session_state.damage = 0

if "message" not in st.session_state:
    st.session_state.message = ""


# -----------------------------
# MATH QUESTION GENERATOR
# -----------------------------
def factorial(n):
    return 1 if n == 0 else n * factorial(n - 1)

def generate_question(level):
    if level == 1:
        n = random.randint(5, 8)
        r = random.randint(2, 4)
        q = f"How many permutations of {n} items taken {r}?"
        a = factorial(n) // factorial(n - r)

    elif level == 2:
        n = random.randint(6, 10)
        r = random.randint(2, 5)
        q = f"How many combinations of {n} items taken {r}?"
        a = factorial(n) // (factorial(r) * factorial(n - r))

    else:
        n = random.randint(6, 9)
        r = random.randint(2, 5)
        q = f"In how many ways can {r} items be arranged from {n} items?"
        a = factorial(n) // factorial(n - r)

    return q, a


# -----------------------------
# WEAPONS (AI PROGRESSION REWARD)
# -----------------------------
def get_weapon():
    weapons = [
        ("Pencil Sword ✏️", 2),
        ("Notebook Shield 📒", 3),
        ("Protractor Blade 📐", 5),
        ("Calculator Cannon 🔢", 7),
        ("Final Exam Laser 💥", 12),
    ]
    return random.choice(weapons)


# -----------------------------
# AI TEACHER BEHAVIOR
# -----------------------------
def teacher_ai_speed():
    distance = st.session_state.player_pos - st.session_state.teacher_pos

    # AI gets more aggressive when close
    if distance > 15:
        return random.uniform(0.5, 1.0)
    elif distance > 8:
        return random.uniform(1.0, 1.5)
    else:
        return random.uniform(1.5, 2.5)


def move_teacher():
    speed = teacher_ai_speed()
    st.session_state.teacher_pos += speed


def move_player(correct=True):
    if correct:
        st.session_state.player_pos += 3
    else:
        st.session_state.player_pos += 0.5


# -----------------------------
# GAME LOGIC
# -----------------------------
def next_question():
    q, a = generate_question(st.session_state.level)
    st.session_state.question = q
    st.session_state.answer = a


def check_answer(user_input):
    try:
        user_input = int(user_input)
    except:
        st.session_state.message = "❌ Invalid input!"
        return

    correct = user_input == st.session_state.answer

    if correct:
        st.session_state.message = "✅ Correct! You run forward!"
        move_player(True)

        weapon, dmg = get_weapon()
        st.session_state.weapon = weapon
        st.session_state.damage = dmg

        st.session_state.level += 1

    else:
        st.session_state.message = "❌ Wrong! Teacher is accelerating!"
        move_player(False)
        st.session_state.teacher_pos += 2  # rage boost

    move_teacher()


# -----------------------------
# VISUAL CHASE ANIMATION
# -----------------------------
def render_chase():
    length = 30
    track = ["⬜"] * length

    player_index = min(max(int(st.session_state.player_pos), 0), length - 1)
    teacher_index = min(max(int(st.session_state.teacher_pos), 0), length - 1)

    track[teacher_index] = "👨‍🏫"
    track[player_index] = "🏃"

    return "".join(track)


def danger_level():
    dist = st.session_state.player_pos - st.session_state.teacher_pos
    if dist < 5:
        return "🔴 EXTREME DANGER"
    elif dist < 10:
        return "🟠 DANGER"
    else:
        return "🟢 SAFE"


# -----------------------------
# UI
# -----------------------------
st.title("🏫🔥 AI Teacher Chase: Permutation Escape Game")

st.write("Answer correctly to outrun the AI teacher!")

st.markdown("### 🏃 Chase Track")
st.code(render_chase())

st.markdown(f"### {danger_level()}")

st.write(f"📍 Player Position: {st.session_state.player_pos:.1f}")
st.write(f"👨‍🏫 Teacher Position: {st.session_state.teacher_pos:.1f}")
st.write(f"📊 Level: {st.session_state.level}")

# win/lose conditions
if st.session_state.teacher_pos >= st.session_state.player_pos:
    st.error("💀 The teacher caught you!")
    st.stop()

if st.session_state.player_pos >= 30:
    st.success("🎉 You escaped the school!")
    st.stop()

# -----------------------------
# QUESTION SYSTEM
# -----------------------------
if st.session_state.question is None:
    next_question()

st.subheader("🧠 Question")
st.write(st.session_state.question)

user_input = st.text_input("Answer:")

if st.button("Submit"):
    check_answer(user_input)
    next_question()
    st.rerun()

st.write(st.session_state.message)

# -----------------------------
# WEAPON DISPLAY
# -----------------------------
if st.session_state.weapon:
    st.markdown(f"🔫 Weapon: **{st.session_state.weapon}** (Damage {st.session_state.damage})")

# -----------------------------
# FINAL ATTACK MODE
# -----------------------------
if st.session_state.level > 5:
    st.markdown("## 🔥 Teacher Rage Mode Activated")

    if st.button("Attack Teacher"):
        st.session_state.teacher_pos -= st.session_state.damage / 2
        st.success(f"You attacked with {st.session_state.weapon}!")
        st.rerun()
