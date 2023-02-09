import Fillable from "./Fillable.js"
import WaterTank from "./WaterTank.js";
import WaterPipe from "./WaterPipe.js";


const canvas = document.getElementById('canvas');
const width = canvas.width;
const height = canvas.height;
const NUMBER_OF_TANKS = 4;
const ctx = canvas.getContext('2d');

let fillLevel = 0; // between 0 and 1	

const drawScene = () => {

	// Tanks
	for (let i = 0; i < NUMBER_OF_TANKS; i++) {
        console.log("here")
		let dx = 120; 
		let change_in_x = (dx * i);
		ctx.fillStyle = 'grey';
		ctx.fillRect(30 + change_in_x, 50, 100, 200);
	}

	// Water Tanks
	for (let i = 0; i < NUMBER_OF_TANKS; i++) {
		let dx = 120; 
		let change_in_x = (dx * i);
		ctx.fillStyle = 'black';
		ctx.fillRect(50 + change_in_x, 110, 50, 100);
	}

	// Roofs
	for (let i = 0; i < NUMBER_OF_TANKS; i++) {
		let dx = 120;
		let change_in_x = (dx * i) 
		ctx.beginPath();
		ctx.moveTo(30 + change_in_x, 250);
		ctx.lineTo(80 + change_in_x, 300);
		ctx.lineTo(130 + change_in_x, 250);
		ctx.closePath();
		ctx.strokeStyle = 'black';
		ctx.fillStyle = 'grey';
		ctx.fill();
		ctx.stroke();
	}

	// Animation 
	const pipes = []
	const tanks = []
	const tankHeight = 100;
	const tankFillHeight = tankHeight * fillLevel;

	// Fill height from 0 to 1 
	const height = 100;
	const fillHeight = height * fillLevel;	
	
	// Four water pipes
	for (let i = 0; i < NUMBER_OF_TANKS; i++) {
		let change_in_x = 120;

		tanks.push(
			new WaterTank(50 + (change_in_x * i), 210, 50, -100 + tankFillHeight, '#afeeee', ctx),
		);

		pipes.push(
			// Start from the (y coordinate - fillHeight), slowly increases and height is
			new Fillable(110 + (change_in_x * i) , 220, 120, 20,  '#2F4F4F', ctx), 
			// new Fillable(150 + (change_in_x * i) , 180, 80, 20, 'purple'), 
			new WaterPipe(110 + (change_in_x * i) , 220 - fillHeight, 20, fillHeight , "#afeeee", ctx),
			new Fillable(110 + (change_in_x * i), 120, 20, 100, '#000000', ctx),
		);
		
	}
	
	for (let i = 0 ; i < tanks.length; i++ ) {
		tanks[i].render();
	}
	
	for (let i = 0 ; i < pipes.length; i++ ) {
		pipes[i].render();
	}

		
}

const renderLoop = () => {
	ctx.clearRect(0, 0, width, height);
	drawScene();
	fillLevel += 0.002;
	console.log(fillLevel);
	if (fillLevel > 1) { fillLevel = 0;}
	requestAnimationFrame(renderLoop);
};

renderLoop();