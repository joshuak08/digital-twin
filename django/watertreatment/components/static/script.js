const canvas = document.getElementById('canvas');
const width = canvas.width;
const height = canvas.height;
const NUMBER_OF_TANKS = 4;
const NUMBER_OF_PIPES = 3;
const ctx = canvas.getContext('2d');

class Fillable {
	constructor(x, y, w, h, colour) {
		this.x = x;
		this.y = y;
		this.w = w;
		this.h = h;
		this.colour = colour;
	}

	render() {
		ctx.strokeStyle = this.colour;
		ctx.lineWidth = 3;
		ctx.strokeRect(this.x, this.y, this.w, this.h);
	}
}

class WaterPipe extends Fillable {
	constructor(x, y, w, h, colour, fillHeight) {
		super(x, y, w, h, colour);
		this.fillHeight = fillHeight;
	}

	render() {
		ctx.fillStyle = this.colour;
		ctx.fillRect(this.x, this.y, this.w, this.h);
	}
} 

class WaterTank extends Fillable {
	constructor(x, y, w, h, colour, fillHeight) {
		super(x, y, w, h, colour);
		this.fillHeight = fillHeight;
	}

	render() {
		ctx.fillStyle = this.colour;
		ctx.fillRect(this.x, this.y, this.w, this.h);
	}
} 

let fillLevel = 0; // between 0 and 1	

const drawScene = () => {

	// Tanks
	for (let i = 0; i < NUMBER_OF_TANKS; i++) {
		let dx = 120; 
		change_in_x = (dx * i);
		ctx.fillStyle = 'grey';
		ctx.fillRect(30 + change_in_x, 50, 100, 200);
	}

	// Water Tanks
	for (let i = 0; i < NUMBER_OF_TANKS; i++) {
		let dx = 120; 
		change_in_x = (dx * i);
		ctx.fillStyle = 'black';
		ctx.fillRect(50 + change_in_x, 100, 50, 100);
	}

	// Roofs
	for (let i = 0; i < NUMBER_OF_TANKS; i++) {
		let dx = 120;
		change_in_x = (dx * i) 
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
	
	const pipes = []
	const tanks = []
	const tankHeight = 100;
	const tankFillHeight = tankHeight * fillLevel;

	// Three pipes
	for (let i = 0; i < NUMBER_OF_PIPES; i++) {
		let change_in_x = 120;
		pipes.push(
			new Fillable(130 + (change_in_x * i) , 180, 20, 20, 'blue'), 
			new Fillable(150 + (change_in_x * i) , 180, 80, 20, 'purple'), 
		);
	}

	// Fill height from 0 to 1 
	const height = 100;
	const fillHeight = height * fillLevel;	
	
	// Four water pipes
	for (let i = 0; i < NUMBER_OF_TANKS; i++) {
		let change_in_x = 120;
		tanks.push(
			new WaterTank(50 + (change_in_x * i), 210, 50, -100 + tankFillHeight, '#afeeee'),
		);
		pipes.push(
			// Start from the (y coordinate - fillHeight), slowly increases and height is
			new WaterPipe(110 + (change_in_x * i) , 210 - fillHeight, 20, fillHeight , "#afeeee"),
			new Fillable(110 + (change_in_x * i), 110, 20, 100, '#000000'),
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
	// Render background
	ctx.clearRect(0, 0, width, height);
	drawScene();
	fillLevel += 0.002;
	console.log(fillLevel);
	if (fillLevel > 1) { fillLevel = 0;}
	
	requestAnimationFrame(renderLoop);
};

renderLoop();