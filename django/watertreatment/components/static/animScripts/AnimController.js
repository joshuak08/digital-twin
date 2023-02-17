import { WaterTank } from "./WaterTank.js"
// import { draw } from "./ScadaController.js"
import { ScadaController } from "./ScadaController.js";

//============ constant values ============//
const ctx_layer1 = document.getElementById("canvas_layer1").getContext("2d");
const ctx_layer2 = document.getElementById("canvas_layer2_anim").getContext("2d");

const box1 = document.getElementById("scada1").getContext("2d");
const box2 = document.getElementById("scada2").getContext("2d");
const box3 = document.getElementById("scada3").getContext("2d");
const box4 = document.getElementById("scada4").getContext("2d");


const layer1Width = 800;
const layer1Height = 600;

const tankY = layer1Height/3;
const tankX = (layer1Width/4)/2/2;

const tankWidth = 2*tankX;
const bottomTankY = tankY+170;

const offsetBetweenTanks = (layer1Width/4);

const tankValues=[153, 57, 0, 35, 0, 153];
const pipeWidth = 12;

let tanks = []
let boxes = [box1,box2,box3,box4]
//==========================================//
//draws grey pipes connected to tanks
function IOpipes(tankNum){
    let pipeX = tankX + offsetBetweenTanks*tankNum + tankX - pipeWidth/2
    let pipeHeight = 50
    let pipeY = tankY-pipeHeight
    //pipes ontop
    ctx_layer1.fillRect(pipeX, pipeY, pipeWidth, pipeHeight);
    //pipes below
    ctx_layer1.fillRect(pipeX, pipeY+pipeHeight+170, pipeWidth, pipeHeight);

    if (tankNum === 0 ){
        ctx_layer1.fillRect(pipeX, pipeY, 700, pipeWidth);
        ctx_layer1.fillRect(pipeX, pipeY+2*pipeHeight+170, 700, pipeWidth);
        ctx_layer1.font = "12px Arial";
        ctx_layer1.fillStyle = "white";
        ctx_layer1.fillText("input pipe", pipeX+645, pipeY+10);
        ctx_layer1.fillText("output pipe", pipeX+638, pipeY+10+170+2*pipeHeight);
        ctx_layer1.fillStyle = "#5A5A5A";
    }
}

//draws grey tank background
function tankBG(tankNum){
    //draw square part of tank (grey)
    ctx_layer1.fillRect(tankX + offsetBetweenTanks*tankNum, tankY, 2*tankX, 170); //x, y, sizex, sizey
    //draw triangle part of tank (grey)
    let tankTopLeftCoord = tankX + offsetBetweenTanks*tankNum;
    ctx_layer1.beginPath();
    ctx_layer1.moveTo(tankTopLeftCoord, bottomTankY);
    ctx_layer1.lineTo(tankTopLeftCoord + tankWidth, bottomTankY);
    ctx_layer1.lineTo((2*tankTopLeftCoord + tankWidth)/2, bottomTankY + 20);
    ctx_layer1.closePath();
    ctx_layer1.fill();
}

//draws water background
export function waterBG(tankNum){
    let TLCoord = tankX + offsetBetweenTanks*tankNum + 10; // 50 + 200 *tankNum + 10
    let waterWidth = 2*tankX - 20;
    let waterHeight = 170 - 17;
    let BTTank = tankY + 10 + waterHeight;

    // water for tanks (lightBlue)
    ctx_layer2.fillStyle = 'lightBlue'
    ctx_layer2.fillRect(TLCoord, tankY + 10, waterWidth, waterHeight);
    // triangle water (lightBlue)
    ctx_layer2.fillStyle = '#C2B280'
    ctx_layer2.beginPath();
    ctx_layer2.moveTo(TLCoord, BTTank);
    ctx_layer2.lineTo(TLCoord + 2*tankX - 20, BTTank);
    ctx_layer2.lineTo((TLCoord + TLCoord + 2*tankX - 20)/2, BTTank + 15);
    ctx_layer2.closePath();
    ctx_layer2.fill();
    // initialise water animation objects
    tanks.push(new WaterTank(TLCoord, tankY + 10, waterWidth, waterHeight, '#303030', ctx_layer2, tankNum, tankValues));
}

//creates background for 4 tanks 
function drawBG(){
    ctx_layer1.fillStyle = '#5A5A5A';
    for (let tankNum = 0; tankNum < 4; tankNum++ ){
        tankBG(tankNum);
        waterBG(tankNum);
        IOpipes(tankNum)
    }
}

function animate(){
    for (let tankNum=0; tankNum<4; tankNum++) {tanks[tankNum].draw();}
    requestAnimationFrame(animate)
}

drawBG();
animate();


