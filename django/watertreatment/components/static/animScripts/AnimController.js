import {WaterTank} from './WaterTank.js';
import {ScadaController} from './ScadaController.js';

// ============ constant values ============//
const ctx_layer1 = document.getElementById('canvas_layer1').getContext('2d');
const ctx_layer2 = document.getElementById('canvas_layer2_anim').getContext('2d');
const scada1CTX = document.getElementById('scada1').getContext('2d');
const scada2CTX = document.getElementById('scada2').getContext('2d');
const scada3CTX = document.getElementById('scada3').getContext('2d');
const scada4CTX = document.getElementById('scada4').getContext('2d');
const contexts = [scada1CTX, scada2CTX, scada3CTX, scada4CTX];

const layer1Width = 800;
const layer1Height = 600;

const tankY = layer1Height/3;
const tankX = ((layer1Width/4)/2)/2;

const tankWidth = 2*tankX;
const tankHeight = 180;
const bottomTankY = tankY+tankHeight;

const offsetBetweenTanks = (layer1Width/4);
const pipeWidth = 12;

const tanks = [];
// ==========================================//
function drawTankShape(ctx, bottomTankY, triangleTipOffset, xCoord, yCoord, width, height, fillStyle1, fillStyle2){
  ctx.fillStyle = fillStyle1;
  ctx.fillRect(xCoord, yCoord, width, height);
  ctx.fillStyle = fillStyle2;
  ctx.beginPath();
  ctx.moveTo(xCoord, bottomTankY);
  ctx.lineTo(xCoord + width, bottomTankY);
  ctx.lineTo((2*xCoord + width)/2, bottomTankY + triangleTipOffset);
  ctx.closePath();
  ctx.fill();
}

// draws grey pipes connected to tanks
function IOpipes(tankNum) {
  const pipeX = tankX + offsetBetweenTanks*tankNum + tankWidth/2 - pipeWidth/2;
  const pipeHeight = 50;
  const pipeY = tankY-pipeHeight;

  ctx_layer1.fillRect(pipeX, pipeY, pipeWidth, pipeHeight);// pipes on top
  ctx_layer1.fillRect(pipeX, pipeY+pipeHeight+tankHeight, pipeWidth, pipeHeight);// pipes below

  if (tankNum === 0 ) {
    ctx_layer1.fillRect(pipeX, pipeY, 700, pipeWidth);
    ctx_layer1.fillRect(pipeX, pipeY+2*pipeHeight+tankHeight, 700, pipeWidth);
    ctx_layer1.font = '12px Arial';
    ctx_layer1.fillStyle = 'white';
    ctx_layer1.fillText('input pipe', pipeX+645, pipeY+10);
    ctx_layer1.fillText('output pipe', pipeX+638, pipeY+10+tankHeight+2*pipeHeight);
    ctx_layer1.fillStyle = '#5A5A5A';
  }
}

// draws grey tank background
function tankBG(tankNum) {
  const xCoord = tankX+offsetBetweenTanks*tankNum
  drawTankShape(ctx_layer1, bottomTankY, 20, xCoord, tankY, tankWidth, tankHeight, '#5A5A5A', '#5A5A5A');
}

// draws water background and initialises the tank objects and scada objects
export function waterBG(tankNum) {
  const xCoord = tankX + offsetBetweenTanks*tankNum + 10; // 50 + 200 *tankNum + 10
  const waterWidth = tankWidth - 20;
  const waterHeight = tankHeight - 17;
  const bottomWaterY = tankY + 10 + waterHeight;

  drawTankShape(ctx_layer2, bottomWaterY, 15, xCoord, tankY+10, waterWidth, waterHeight, 'lightBlue', '#C2B280')

  const scada_controller = new ScadaController(contexts[tankNum]);
  tanks.push(new WaterTank(xCoord, tankY + 10, waterWidth, waterHeight, '#303030', ctx_layer2, tankNum, scada_controller));
}

// creates background for 4 tanks
function drawBG() {
  ctx_layer1.fillStyle = '#5A5A5A';
  for (let tankNum = 0; tankNum < 4; tankNum++ ) {
    tankBG(tankNum);
    waterBG(tankNum); // this one also initialises tank and scada controller objects
    IOpipes(tankNum);
  }
}

// animation loop
function animate() {
  // makes the tanks draw on canvases
  for (let tankNum=0; tankNum<4; tankNum++) {
    tanks[tankNum].draw();
  }
  requestAnimationFrame(animate);
}

drawBG();
animate();


