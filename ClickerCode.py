import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Minecraft Survival Pro", layout="wide")

st.title("⛏️ Minecraft Survival Pro (Hotbar + Crafting + Mobs + Caves)")

components.html(r"""
<!DOCTYPE html>
<html>
<head>
<style>
body { margin:0; background:#000; font-family:Arial; color:white; }

#ui {
  position:fixed;
  top:10px; left:10px;
  background:rgba(0,0,0,0.6);
  padding:10px;
  border-radius:10px;
  font-size:14px;
}

#hotbar {
  position:fixed;
  bottom:10px;
  left:50%;
  transform:translateX(-50%);
  display:flex;
  gap:6px;
}

.slot {
  width:50px; height:50px;
  background:#333;
  border:2px solid #666;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:11px;
}

canvas { display:block; margin:auto; background:#87CEEB; }
</style>
</head>

<body>

<div id="ui">
❤️ HP: <span id="hp">100</span><br>
🍗 Hunger: <span id="hunger">100</span><br>
🪵 Wood: <span id="wood">0</span>
🪨 Stone: <span id="stone">0</span><br>
🌗 Time: <span id="time">Day</span>
</div>

<div id="hotbar">
  <div class="slot" id="s0">Hand</div>
  <div class="slot" id="s1">Axe</div>
  <div class="slot" id="s2">Sword</div>
  <div class="slot" id="s3">Torch</div>
  <div class="slot" id="s4">Craft</div>
</div>

<canvas id="game" width="800" height="600"></canvas>

<script>
const c = document.getElementById("game");
const ctx = c.getContext("2d");

const T = 20;
const W = c.width/T;
const H = c.height/T;

// player
let p = {x:50,y:50,hp:100,hunger:100};
let inv = {wood:0, stone:0};
let hotbar = 0;

// world
let world = {};
let torches = [];

// mobs
let mobs = [];

// time
let time = 0;
let night = false;

function k(x,y){ return x+","+y; }

// caves + terrain
function gen(x,y){
  let n = Math.sin(x*0.08)+Math.cos(y*0.08);

  if (y > 60 + n*5) return "stone";
  if (y > 55 + n*3) return "dirt";
  if (Math.random() < 0.01 && y > 55) return "cave";
  return "grass";
}

function get(x,y){
  if(!world[k(x,y)]) world[k(x,y)] = gen(x,y);
  return world[k(x,y)];
}

function set(x,y,v){ world[k(x,y)] = v; }

// draw
function draw(){
  for(let y=0;y<H;y++){
    for(let x=0;x<W;x++){

      let wx = p.x + x - W/2;
      let wy = p.y + y - H/2;

      let b = get(wx,wy);

      let dark = night ? 0.6 : 0;

      if(b=="grass") ctx.fillStyle="#3cb043";
      if(b=="stone") ctx.fillStyle="#777";
      if(b=="dirt") ctx.fillStyle="#8B5A2B";
      if(b=="cave") ctx.fillStyle="#111";

      ctx.fillRect(x*T,y*T,T,T);

      ctx.fillStyle=`rgba(0,0,0,${dark})`;
      ctx.fillRect(x*T,y*T,T,T);
    }
  }

  // torches light
  torches.forEach(t=>{
    let dx = t.x - p.x + W/2;
    let dy = t.y - p.y + H/2;

    for(let i=-5;i<=5;i++){
      for(let j=-5;j<=5;j++){
        let dist = Math.sqrt(i*i+j*j);
        if(dist<5){
          ctx.fillStyle=`rgba(255,200,100,${0.3-(dist*0.05)})`;
          ctx.fillRect((dx+i)*T,(dy+j)*T,T,T);
        }
      }
    }
  });

  // player
  ctx.fillStyle="red";
  ctx.fillRect(W/2*T,H/2*T,T,T);

  // mobs
  ctx.fillStyle="purple";
  mobs.forEach(m=>{
    let dx = m.x - p.x + W/2;
    let dy = m.y - p.y + H/2;
    ctx.fillRect(dx*T,dy*T,T,T);
  });
}

// movement (ARROW KEYS)
document.addEventListener("keydown", e=>{
  let nx=p.x, ny=p.y;

  if(e.key==="ArrowUp") ny--;
  if(e.key==="ArrowDown") ny++;
  if(e.key==="ArrowLeft") nx--;
  if(e.key==="ArrowRight") nx++;

  let b = get(nx,ny);

  if(b==="stone") inv.stone++;
  if(b==="dirt") inv.wood++;

  set(nx,ny,"grass");

  p.x=nx; p.y=ny;
});

// hotbar
document.addEventListener("keydown", e=>{
  if(e.key>="0" && e.key<="4") hotbar = parseInt(e.key);
});

// crafting
function craft(){
  if(inv.wood>=3){
    inv.wood-=3;
    document.getElementById("s1").style.background="gold";
  }
}

// place torch
document.addEventListener("keydown", e=>{
  if(e.key===" "){
    torches.push({x:p.x,y:p.y});
  }
});

// mobs AI (simple pathfinding)
function spawnMobs(){
  mobs=[];
  for(let i=0;i<6;i++){
    mobs.push({x:p.x+Math.random()*20-10,y:p.y+Math.random()*20-10});
  }
}

function moveMobs(){
  mobs.forEach(m=>{
    let dx = p.x - m.x;
    let dy = p.y - m.y;

    if(Math.abs(dx)>Math.abs(dy)){
      m.x += dx>0?0.3:-0.3;
    } else {
      m.y += dy>0?0.3:-0.3;
    }

    if(Math.abs(m.x-p.x)<1 && Math.abs(m.y-p.y)<1){
      p.hp -= 1;
    }
  });
}

// day night
function timeUpdate(){
  time += 0.1;
  if(time>100) time=0;

  if(time<50){
    night=false;
    document.getElementById("time").innerText="Day";
  } else {
    if(!night) spawnMobs();
    night=true;
    document.getElementById("time").innerText="Night";
  }

  if(p.hunger>0) p.hunger-=0.02;
  else p.hp-=0.05;
}

// UI
function ui(){
  document.getElementById("hp").innerText=Math.floor(p.hp);
  document.getElementById("hunger").innerText=Math.floor(p.hunger);
  document.getElementById("wood").innerText=inv.wood;
  document.getElementById("stone").innerText=inv.stone;
}

// loop
function loop(){
  timeUpdate();
  moveMobs();
  draw();
  ui();
  requestAnimationFrame(loop);
}

loop();
</script>

</body>
</html>
""", height=800)
