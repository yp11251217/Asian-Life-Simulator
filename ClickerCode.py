import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Geometry Dash Streamlit", layout="wide")

st.title("🎮 Geometry Dash (Streamlit HTML Edition)")
st.write("Press SPACE or click to jump. Avoid obstacles!")

game_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    body { margin:0; overflow:hidden; background:#111; }
    canvas { background:#111; display:block; margin:auto; }
    #score {
        position: absolute;
        top: 10px;
        left: 10px;
        color: white;
        font-family: Arial;
        font-size: 18px;
    }
</style>
</head>
<body>
<div id="score">Score: 0</div>
<canvas id="game" width="900" height="400"></canvas>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let player = {
    x: 80,
    y: 300,
    w: 30,
    h: 30,
    dy: 0,
    gravity: 0.8,
    jumpPower: -12,
    grounded: false
};

let obstacles = [];
let frame = 0;
let score = 0;
let gameOver = false;

function spawnObstacle() {
    obstacles.push({
        x: 900,
        y: 320,
        w: 30 + Math.random()*20,
        h: 30,
        speed: 6
    });
}

function resetGame() {
    player.y = 300;
    player.dy = 0;
    obstacles = [];
    score = 0;
    frame = 0;
    gameOver = false;
}

function jump() {
    if (player.grounded) {
        player.dy = player.jumpPower;
        player.grounded = false;
    }
}

document.addEventListener("keydown", e => {
    if (e.code === "Space") jump();
    if (e.code === "KeyR") resetGame();
});

document.addEventListener("click", jump);

function update() {
    if (gameOver) return;

    frame++;
    score = Math.floor(frame / 5);
    document.getElementById("score").innerText = "Score: " + score;

    // gravity
    player.dy += player.gravity;
    player.y += player.dy;

    if (player.y + player.h >= 350) {
        player.y = 350 - player.h;
        player.dy = 0;
        player.grounded = true;
    }

    // spawn obstacles
    if (frame % 90 === 0) spawnObstacle();

    // move obstacles
    for (let i = 0; i < obstacles.length; i++) {
        obstacles[i].x -= obstacles[i].speed;

        // collision
        if (
            player.x < obstacles[i].x + obstacles[i].w &&
            player.x + player.w > obstacles[i].x &&
            player.y < obstacles[i].y + obstacles[i].h &&
            player.y + player.h > obstacles[i].y
        ) {
            gameOver = true;
        }
    }

    obstacles = obstacles.filter(o => o.x + o.w > 0);
}

function draw() {
    ctx.clearRect(0,0,canvas.width,canvas.height);

    // ground
    ctx.fillStyle = "#333";
    ctx.fillRect(0, 350, 900, 50);

    // player
    ctx.fillStyle = "#00ffcc";
    ctx.fillRect(player.x, player.y, player.w, player.h);

    // obstacles
    ctx.fillStyle = "#ff4444";
    for (let o of obstacles) {
        ctx.fillRect(o.x, o.y, o.w, o.h);
    }

    // game over
    if (gameOver) {
        ctx.fillStyle = "white";
        ctx.font = "40px Arial";
        ctx.fillText("GAME OVER", 320, 200);
        ctx.font = "20px Arial";
        ctx.fillText("Press R to restart", 340, 240);
    }
}

function loop() {
    update();
    draw();
    requestAnimationFrame(loop);
}

loop();
</script>
</body>
</html>
"""

components.html(game_html, height=450)
