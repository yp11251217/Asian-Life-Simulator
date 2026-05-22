import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Chicken Dashboard Game", layout="wide")

st.title("🐔 Chicken Cross the Road — HTML Dashboard Game")

html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
body {
    font-family: Arial;
    background: #111;
    color: white;
}

#game {
    display: grid;
    grid-template-columns: repeat(7, 60px);
    gap: 3px;
    justify-content: center;
    margin-top: 20px;
}

.cell {
    width: 60px;
    height: 60px;
    background: #222;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    border-radius: 6px;
}

.info {
    text-align: center;
    margin-top: 10px;
    color: #aaa;
}

#status {
    text-align: center;
    font-size: 22px;
    margin-top: 10px;
}
</style>
</head>

<body>

<div class="info">
Press <b>SPACEBAR</b> to move forward ⬆️ | Avoid 🚗 cars
</div>

<div id="status">Running...</div>

<div id="game"></div>

<script>

const width = 7;
const height = 10;

let chicken = {x: 3, y: 9};
let cars = [];
let gameOver = false;

// spawn cars
for (let i = 0; i < 4; i++) {
    cars.push({
        x: Math.floor(Math.random() * width),
        y: Math.floor(Math.random() * height)
    });
}

// render grid
function draw() {
    const game = document.getElementById("game");
    game.innerHTML = "";

    for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {

            let cell = document.createElement("div");
            cell.className = "cell";

            // chicken
            if (chicken.x === x && chicken.y === y) {
                cell.innerHTML = "🐔";
                cell.style.background = "#2ecc71";
            }

            // cars
            cars.forEach(c => {
                if (c.x === x && c.y === y) {
                    cell.innerHTML = "🚗";
                    cell.style.background = "#e74c3c";
                }
            });

            game.appendChild(cell);
        }
    }
}

// move cars down
function updateCars() {
    cars.forEach(c => {
        c.y += 1;
        if (c.y >= height) {
            c.y = 0;
            c.x = Math.floor(Math.random() * width);
        }
    });
}

// collision detection
function checkCollision() {
    for (let c of cars) {
        if (c.x === chicken.x && c.y === chicken.y) {
            gameOver = true;
            document.getElementById("status").innerHTML = "💥 GAME OVER";
        }
    }
}

// win condition
function checkWin() {
    if (chicken.y < 0) {
        gameOver = true;
        document.getElementById("status").innerHTML = "🎉 YOU WIN!";
    }
}

// game loop
function loop() {
    if (gameOver) return;

    updateCars();
    checkCollision();
    checkWin();
    draw();
}

setInterval(loop, 500);

// spacebar control
document.addEventListener("keydown", function(e) {
    if (e.code === "Space" && !gameOver) {
        chicken.y -= 1;
    }
});

draw();

</script>

</body>
</html>
"""

components.html(html_code, height=800)
