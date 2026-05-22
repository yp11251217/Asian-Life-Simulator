# Asian Child Life Simulator (Steven He Inspired)

```python
import streamlit as st
import random

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="Asian Child Life Simulator",
    page_icon="📚",
    layout="centered"
)

# =====================================
# SESSION STATE
# =====================================
if "initialized" not in st.session_state:
    st.session_state.age = 6
    st.session_state.grade = 1
    st.session_state.intelligence = 50
    st.session_state.happiness = 50
    st.session_state.energy = 100
    st.session_state.social = 50
    st.session_state.money = 0
    st.session_state.achievement = "Failure"
    st.session_state.message = "You are born into an Asian household."
    st.session_state.initialized = True

# =====================================
# STYLING
# =====================================
st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 50px;
    font-weight: bold;
    color: #d62828;
}

.subtitle {
    text-align: center;
    color: gray;
    margin-bottom: 30px;
}

.stat-box {
    background-color: #f1f1f1;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 10px;
}

.message-box {
    background-color: #fff3cd;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #ffe69c;
    margin-top: 20px;
    font-size: 20px;
}

.big-text {
    font-size: 24px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# TITLE
# =====================================
st.markdown(
    "<div class='main-title'>📚 Asian Child Life Simulator</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Steven He Inspired Simulator</div>",
    unsafe_allow_html=True
)

# =====================================
# STATS
# =====================================
st.subheader("📊 Your Stats")

col1, col2 = st.columns(2)

with col1:
    st.metric("Age", st.session_state.age)
    st.metric("Grade", st.session_state.grade)
    st.metric("Intelligence", st.session_state.intelligence)
    st.metric("Energy", st.session_state.energy)

with col2:
    st.metric("Happiness", st.session_state.happiness)
    st.metric("Social Life", st.session_state.social)
    st.metric("Money", f"${st.session_state.money}")
    st.metric("Achievement", st.session_state.achievement)

# =====================================
# MESSAGE
# =====================================
st.markdown(
    f"<div class='message-box'>{st.session_state.message}</div>",
    unsafe_allow_html=True
)

# =====================================
# FUNCTIONS
# =====================================
def check_status():

    if st.session_state.intelligence >= 200:
        st.session_state.achievement = "Doctor"

    elif st.session_state.intelligence >= 170:
        st.session_state.achievement = "Engineer"

    elif st.session_state.intelligence >= 140:
        st.session_state.achievement = "Accountant"

    elif st.session_state.intelligence < 60:
        st.session_state.achievement = "Disappointment"

    if st.session_state.happiness <= 0:
        st.session_state.message = "You are emotionally damaged from too much homework."

# =====================================
# ACTIONS
# =====================================
st.subheader("🎮 Actions")

col1, col2 = st.columns(2)

# =====================================
# STUDY
# =====================================
with col1:

    if st.button("📖 Study 12 Hours"):

        gain = random.randint(8, 20)

        st.session_state.intelligence += gain
        st.session_state.energy -= 15
        st.session_state.happiness -= 10

        st.session_state.message = (
            f"You studied for 12 hours. +{gain} intelligence. "
            "Parents say: Why not 13 hours?"
        )

        check_status()
        st.rerun()

# =====================================
# PIANO
# =====================================
with col2:

    if st.button("🎹 Practice Piano"):

        st.session_state.intelligence += 5
        st.session_state.happiness -= 5
        st.session_state.energy -= 10

        st.session_state.message = (
            "You practiced piano for competition. "
            "Neighbor kid plays better."
        )

        check_status()
        st.rerun()

# =====================================
# MATH
# =====================================
col3, col4 = st.columns(2)

with col3:

    if st.button("➗ Extra Math Homework"):

        st.session_state.intelligence += 12
        st.session_state.energy -= 20
        st.session_state.happiness -= 12

        st.session_state.message = (
            "You completed 900 math questions. "
            "Still not enough."
        )

        check_status()
        st.rerun()

# =====================================
# PLAY GAMES
# =====================================
with col4:

    if st.button("🎮 Play Video Games"):

        st.session_state.happiness += 15
        st.session_state.social += 5
        st.session_state.energy += 5

        chance = random.randint(1, 10)

        if chance <= 4:
            st.session_state.message = (
                "EMOTIONAL DAMAGE! Parents caught you gaming."
            )

            st.session_state.happiness -= 20

        else:
            st.session_state.message = (
                "You secretly played games without getting caught."
            )

        check_status()
        st.rerun()

# =====================================
# SLEEP
# =====================================
if st.button("😴 Sleep"):

    st.session_state.energy += 30
    st.session_state.happiness += 5

    if st.session_state.energy > 100:
        st.session_state.energy = 100

    st.session_state.message = (
        "You slept peacefully... until parents wake you up for more studying."
    )

    check_status()
    st.rerun()

# =====================================
# AGE UP
# =====================================
st.markdown("---")

if st.button("🎂 Next Year"):

    st.session_state.age += 1
    st.session_state.grade += 1

    st.session_state.energy -= 10

    event = random.choice([
        "You got compared to cousin again.",
        "Parents ask why you not doctor yet.",
        "You got 99%. Parents ask where 1% went.",
        "You attend another tutoring center.",
        "Grandma says you too skinny.",
        "Parents say failure is not option.",
        "You won math competition.",
        "You got another homework packet.",
    ])

    st.session_state.message = event

    # Random stat changes
    st.session_state.intelligence += random.randint(1, 8)
    st.session_state.happiness -= random.randint(1, 5)

    # Clamp stats
    st.session_state.happiness = max(0, st.session_state.happiness)
    st.session_state.energy = max(0, st.session_state.energy)

    check_status()

    st.rerun()

# =====================================
# GAME OVER
# =====================================
if st.session_state.age >= 30:

    st.markdown("---")
    st.subheader("🏆 Final Result")

    if st.session_state.intelligence >= 200:
        st.success("You became a legendary doctor. Parents finally proud.")

    elif st.session_state.intelligence >= 170:
        st.success("You became an engineer. Parents accept you.")

    elif st.session_state.intelligence >= 140:
        st.warning("You became accountant. Acceptable.")

    else:
        st.error("EMOTIONAL DAMAGE! You became disappointment.")

    st.stop()

# =====================================
# FOOTER
# =====================================
st.markdown("---")
st.caption("Inspired by Steven He comedy videos")
```

## Run the game

```bash
pip install streamlit
streamlit run app.py
```
