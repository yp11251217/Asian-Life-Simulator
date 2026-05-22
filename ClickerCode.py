import streamlit as st
import streamlit.components.v1 as components
import random
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Chicken Cross", layout="centered")

WIDTH = 7
HEIGHT = 12


def init_game():
    return {
        "chicken_x": WIDTH // 2,
        "chicken_y": HEIGHT - 1,
        "cars": [(random.randint(0, WIDTH - 1), y) for y in range(2, HEIGHT - 2, 2)],
        "game_over": False,
        "win": False,
        "score": 0,
    }


if "game" not in st.session_state:
    st.session_state.game = init_game()

game = st.session_state.game

# Auto refresh (game loop)
st_autorefresh(interval=600, key="game_loop")

st.title("🐔 Chicken Cross the Road (SPACEBAR EDITION)")

# -----------------------------
# SPACEBAR CONTROL (HTML + JS)
# -----------------------------
components.html("""
<script>
document.addEventListener('keydown', function(event) {
    if (event.code === 'Space') {
        fetch('/_stcore/stream', {
            method: 'POST',
            body: JSON.stringify({action: "forward"})
        });
    }
});
</script>

<div style="text-align:center;color:gray;">
Press <b>SPACEBAR</b> to move forward ⬆️
</div>
""", height=80)


# -----------------------------
# MOVE CHICKEN ON SPACE PRESS
# -----------------------------
if st.session_state.get("move_forward"):
    game["chicken_y"] -= 1
    st.session_state["move_forward"] = False


# -----------------------------
# MOVE CAR LOGIC
# -----------------------------
new_cars = []
for x, y in game["cars"]:
    y += 1
    if y >= HEIGHT:
        y = 0
        x = random.randint(0, WIDTH - 1)
    new_cars.append((x, y))
game["cars"] = new_cars


# -----------------------------
# COLLISION DETECTION
# -----------------------------
for cx, cy in game["cars"]:
    if cx == game["chicken_x"] and cy == game["chicken_y"]:
        game["game_over"] = True

# Win condition
if game["chicken_y"] < 0:
    game["win"] = True


# -----------------------------
# RENDER GRID (HTML)
# -----------------------------
def render():
    html = """
    <div style="
        display:grid;
        grid-template-columns: repeat(7, 50px);
        gap:2px;
        justify-content:center;
        margin-top:20px;
        font-size:24px;
    ">
    """

    for y in range(HEIGHT):
        for x in range(WIDTH):

            bg = "#f5f5f5"
            content = ""

            if (x, y) == (game["chicken_x"], game["chicken_y"]):
                content = "🐔"
                bg = "#b6ffb6"

            elif (x, y) in game["cars"]:
                content = "🚗"
                bg = "#ff8a8a"

            html += f"""
            <div style="
                width:50px;height:50px;
                background:{bg};
                display:flex;
                align-items:center;
                justify-content:center;
                border:1px solid #ddd;">
                {content}
            </div>
            """

    html += "</div>"
    return html


# -----------------------------
# GAME STATUS
# -----------------------------
if game["game_over"]:
    st.error("💥 Game Over! The chicken got hit by a car.")
elif game["win"]:
    st.success("🎉 You crossed the road safely!")
else:
    st.info("Use SPACEBAR to move forward. Avoid cars 🚗")


# -----------------------------
# SHOW GAME
# -----------------------------
components.html(render(), height=650)


# -----------------------------
# RESET
# -----------------------------
if st.button("🔄 Restart"):
    st.session_state.game = init_game()
    st.rerun()
