import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Mini Survival Minecraft", layout="wide")

st.title("🌍 Mini Survival Minecraft (Day/Night + Mobs + Resources)")

html_game = """
<!DOCTYPE html>
<html>
<head>
<style>
body {
  margin: 0;
  background: black;
  font-family: Arial;
  color: white;
}

#ui {
  position: fixed;
  top: 10px;
  left: 10px;
  background: rgba(0,0,0,0.6);
  padding: 10px;
  border-radius: 10px;
}

canvas {
  display: block;
  margin: auto;
  background: #87CEEB;
}
</style>
</head>

<body>

<div id="ui">
  <div>🪵 Wood: <span id="wood">0</span></div>
  <div>🪨 Stone: <span id="stone">0</span></div>
  <div>🌗 Time: <span id="time">Day</span></div>
</div>

<canvas id="game" width="800" height="600"></canvas>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const tile = 20;
const cols = canvas.width / tile;
const rows = canvas.height / tile;

// player
let player = { x: 20, y: 15 };

// inventory
let wood = 0;
let stone = 0;

// world storage (chunked infinite-like)
let world = {};

// mobs
let mobs = [];

// time system
let time = 0; // 0-100
let isNight = false;

function key(x, y) {
  return x + "," + y;
}

// procedural block generator
function generate(x, y) {
  let h = Math.sin(x * 0.1) * 5 + Math.cos(y * 0.1) * 5;

  if (h > 3) return "stone";
  if (h > 0) return "wood";
  return "grass";
}

function getBlock(x, y) {
  const k = key(x, y);
  if (!world[k]) world[k] = generate(x, y);
  return world[k];
}

function setBlock(x, y, v) {
  world[key(x,y)] = v;
}

// draw world
function draw() {
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      let wx = x + player.x - Math.floor(cols/2);
      let wy = y + player.y - Math.floor(rows/2);

      let b = getBlock(wx, wy);

      if (b === "grass") ctx.fillStyle = "#3cb043";
      if (b === "wood") ctx.fillStyle = "#8B5A2B";
      if (b === "stone") ctx.fillStyle = "#808080";

      ctx.fillRect(x*tile, y*tile, tile, tile);
    }
  }

  // player
  ctx.fillStyle = "red";
  ctx.fillRect(cols/2*tile, rows/2*tile, tile, tile);

  // mobs
  ctx.fillStyle = "purple";
  mobs.forEach(m => {
    let dx = m.x - player.x + cols/2;
    let dy = m.y - player.y + rows/2;
    ctx.fillRect(dx*tile, dy*tile, tile, tile);
  });

  // darkness overlay
  if (isNight) {
    ctx.fillStyle = "rgba(0,0,0,0.4)";
    ctx.fillRect(0,0,canvas.width,canvas.height);
  }
}

// movement
document.addEventListener("keydown", e => {
  let nx = player.x;
  let ny = player.y;

  if (e.key === "w") ny--;
  if (e.key === "s") ny++;
  if (e.key === "a") nx--;
  if (e.key === "d") nx++;

  let block = getBlock(nx, ny);

  // collect resources
  if (block === "wood") wood++;
  if (block === "stone") stone++;

  setBlock(nx, ny, "grass");

  player.x = nx;
  player.y = ny;
});

// spawn mobs at night
function spawnMobs() {
  mobs = [];
  for (let i = 0; i < 5; i++) {
    mobs.push({
      x: player.x + (Math.random()*20-10),
      y: player.y + (Math.random()*20-10)
    });
  }
}

// mob AI
function updateMobs() {
  mobs.forEach(m => {
    if (m.x < player.x) m.x++;
    if (m.x > player.x) m.x--;
    if (m.y < player.y) m.y++;
    if (m.y > player.y) m.y--;

    // collision = "damage"
    if (Math.abs(m.x-player.x)<1 && Math.abs(m.y-player.y)<1) {
      wood = Math.max(0, wood-1);
      stone = Math.max(0, stone-1);
    }
  });
}

// day/night cycle
function updateTime() {
  time += 0.05;

  if (time > 100) time = 0;

  if (time < 50) {
    isNight = false;
    document.getElementById("time").innerText = "Day";
  } else {
    if (!isNight) spawnMobs();
    isNight = true;
    document.getElementById("time").innerText = "Night";
  }
}

// loop
function loop() {
  updateTime();
  updateMobs();
  draw();

  document.getElementById("wood").innerText = wood;
  document.getElementById("stone").innerText = stone;

  requestAnimationFrame(loop);
}

loop();
</script>

</body>
</html>
"""

components.html(html_game, height=750)
