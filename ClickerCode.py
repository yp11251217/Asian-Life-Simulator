import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Swipe Chicken Game", layout="wide")

st.title("🐔 Chicken Cross Road — Swipe Edition (Mobile Ready)")

html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
body {
    font-family: Arial;
    background: #111;
    color: white;
    margin: 0;
    touch-action: none;
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

#status, #score {
    text-align: center;
    font-size: 20px;
    margin-top: 8px;
}

#score {
    color: #2ecc71;
}

#hint {
    text-align: center;
    color: #888;
    font-size: 14px;
    margin-top: 5px;
}

button {
    display: block;
    margin: 10px auto;
    padding: 10px 16px;
    border: none;
    border-radius: 8px;
    background: #2ecc71;
    cursor: pointer;
}
</style>
</head>

<body>

<div id="status">Running...</div>
<div id="score">Score: 0</div>
<div id="hint">Swipe left/right anywhere to move 🐔</div>

<button onclick="restartGame()">🔄 Restart</button>

<div id="game"></div>

<script>

const width = 7;
const height = 10;

let chicken, cars, gameOver;
let score = 0;
let touchStartX = 0;

// INIT GAME
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

// DRAW GRID
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

// MOVE CARS DOWN
function updateCars() {
    for (let c of cars) {
        c.y += 1;

        if (c.y >= height) {
            c.y = 0;
            c.x = Math.floor(Math.random() * width);
        }
    }
}

// COLLISION
function checkCollision() {
    for (let c of cars) {
        if (c.x === chicken.x && c.y === chicken.y) {
            gameOver = true;
            document.getElementById("status").innerHTML = "💥 GAME OVER";
        }
    }
}

// ADJACENT BONUS
function checkAdjacentBonus() {
    for (let c of cars) {
        let dx = Math.abs(c.x - chicken.x);
        let dy = Math.abs(c.y - chicken.y);

        if (dx <= 1 && dy <= 1 && !(dx === 0 && dy === 0)) {
            score += 100;
        }
    }
}

// SCORE UPDATE
function updateScore() {
    document.getElementById("score").innerHTML = "Score: " + score;
}

// GAME LOOP
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
        updateScore();
    }
}, 5000);

// SWIPE CONTROLS
document.addEventListener("touchstart", function(e) {
    touchStartX = e.changedTouches[0].screenX;
});

document.addEventListener("touchend", function(e) {
    if (gameOver) return;

    let touchEndX = e.changedTouches[0].screenX;
    let diff = touchEndX - touchStartX;

    if (Math.abs(diff) < 30) return; // ignore small swipes

    if (diff > 0) {
        moveRight();
    } else {
        moveLeft();
    }
});

// mouse drag support (desktop testing)
document.addEventListener("mousedown", e => touchStartX = e.screenX);
document.addEventListener("mouseup", e => {
    if (gameOver) return;

    let diff = e.screenX - touchStartX;

    if (Math.abs(diff) < 30) return;

    if (diff > 0) moveRight();
    else moveLeft();
});

// MOVEMENT
function moveLeft() {
    if (chicken.x > 0) chicken.x--;
}

function moveRight() {
    if (chicken.x < width - 1) chicken.x++;
}

// RESTART
function restartGame() {
    initGame();
}

// START
initGame();

</script>

</body>
</html>
"""

components.html(html_code, height=900)
