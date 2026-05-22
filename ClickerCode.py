import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Chicken Game Dashboard", layout="wide")

st.title("🐔 Chicken Cross the Road — Dashboard Edition (Final)")

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

#status {
    text-align: center;
    font-size: 22px;
    margin-top: 10px;
}

#score {
    text-align: center;
    font-size: 18px;
    color: #2ecc71;
}

#controls {
    text-align: center;
    margin-top: 15px;
}

button {
    padding: 10px 18px;
    font-size: 16px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    background: #2ecc71;
    color: black;
}
button:hover {
    background: #27ae60;
}
</style>
</head>

<body>

<div id="status">Running...</div>
<div id="score">Score: 0</div>

<div id="controls">
    <button onclick="restartGame()">🔄 Restart</button>
</div>

<div id="game"></div>

<script>

const width = 7;
const height = 10;

let chicken, cars, gameOver, score;

function initGame() {
    chicken = {x: 3, y: 9};
    cars = [];
    gameOver = false;
    score = 0;

    for (let i = 0; i < 5; i++) {
        cars.push({
            x: Math.floor(Math.random() * width),
            y: Math.floor(Math.random() * height)
        });
    }

    document.getElementById("status").innerHTML = "Running...";
    updateScore();
    draw();
}

function draw() {
    const game = document.getElementById("game");
    game.innerHTML = "";

    for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {

            let cell = document.createElement("div");
            cell.className = "cell";

            if (chicken.x === x && chicken.y === y) {
                cell.innerHTML = "🐔";
                cell.style.background = "#2ecc71";
            }

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

function updateCars() {
    cars.forEach(c => {
        c.y += 1;

        if (c.y >= height) {
            c.y = 0;
            c.x = Math.floor(Math.random() * width);
        }
    });
}

function checkCollision() {
    for (let c of cars) {
        if (c.x === chicken.x && c.y === chicken.y) {
            gameOver = true;
            document.getElementById("status").innerHTML = "💥 GAME OVER";
        }
    }
}

function updateScore() {
    document.getElementById("score").innerHTML = "Score: " + score;
}

function loop() {
    if (gameOver) return;

    updateCars();
    checkCollision();
    draw();
}

setInterval(loop, 400);

// controls
document.addEventListener("keydown", function(e) {
    if (gameOver) return;

    if (e.code === "Space") {
        chicken.y -= 1;
        score += 10;
        updateScore();
    }

    if (e.code === "ArrowLeft") {
        if (chicken.x > 0) chicken.x -= 1;
    }

    if (e.code === "ArrowRight") {
        if (chicken.x < width - 1) chicken.x += 1;
    }
});

// restart button
function restartGame() {
    initGame();
}

// start game
initGame();

</script>

</body>
</html>
"""

components.html(html_code, height=900)
