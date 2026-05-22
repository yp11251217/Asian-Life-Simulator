import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Chicken Arcade Game", layout="wide")

st.title("🐔 Chicken Cross the Road — Scoring Edition")

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
    padding: 10px 16px;
    margin: 5px;
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
    <button onclick="moveLeft()">⬅️ Left</button>
    <button onclick="moveRight()">➡️ Right</button>
    <button onclick="restartGame()">🔄 Restart</button>
</div>

<div id="game"></div>

<script>

const width = 7;
const height = 10;

let chicken, cars, gameOver;
let score;
let seconds = 0;

// init game
function initGame() {
    chicken = {x: 3, y: 9};
    cars = [];
    gameOver = false;
    score = 0;
    seconds = 0;

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

// draw grid
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

            for (let c of cars) {
                if (c.x === x && c.y === y) {
                    cell.innerHTML = "🚗";
                    cell.style.background = "#e74c3c";
                }
            }

            game.appendChild(cell);
        }
    }
}

// move cars toward chicken
function updateCars() {
    for (let c of cars) {
        c.y += 1;

        if (c.y >= height) {
            c.y = 0;
            c.x = Math.floor(Math.random() * width);
        }
    }
}

// check collision (death)
function checkCollision() {
    for (let c of cars) {
        if (c.x === chicken.x && c.y === chicken.y) {
            gameOver = true;
            document.getElementById("status").innerHTML = "💥 GAME OVER";
        }
    }
}

// adjacency bonus: +100 if car is next to chicken
function checkAdjacentBonus() {
    for (let c of cars) {
        let dx = Math.abs(c.x - chicken.x);
        let dy = Math.abs(c.y - chicken.y);

        // adjacent (up, down, left, right, or diagonal)
        if (dx <= 1 && dy <= 1 && !(dx === 0 && dy === 0)) {
            score += 100;
        }
    }
}

// score update
function updateScore() {
    document.getElementById("score").innerHTML = "Score: " + score;
}

// game loop
function loop() {
    if (gameOver) return;

    updateCars();
    checkCollision();
    checkAdjacentBonus();

    draw();
    updateScore();
}

setInterval(loop, 400);

// +10 every 5 seconds
setInterval(() => {
    if (!gameOver) {
        score += 10;
        seconds++;
        updateScore();
    }
}, 5000);

// controls (buttons only)
function moveLeft() {
    if (gameOver) return;
    if (chicken.x > 0) chicken.x--;
}

function moveRight() {
    if (gameOver) return;
    if (chicken.x < width - 1) chicken.x++;
}

function restartGame() {
    initGame();
}

// start
initGame();

</script>

</body>
</html>
"""

components.html(html_code, height=900)
