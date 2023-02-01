const canvas = document.getElementById('canvas');
const width = canvas.width;
const height = canvas.height;
const NUMBER_OF_TANKS = 4;
const NUMBER_OF_PIPES = 3;
const ctx = canvas.getContext('2d');

class Pipe {
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

class WaterPipe extends Pipe {
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
		// ctx.fillStyle = 'Black';
		// ctx.fillRect(30 + change_in_x, 50, 100, 200);
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
		ctx.fill();
		ctx.stroke();
	}

	// Filling pipe
	// ctx.fillStyle = "#afeeee";
	// ctx.fillRect(110, 210 - fillHeight, 18, fillHeight);
	
	// All pipes
	let pipes = []
	let waterPipes = []
	
	// Three pipes
	for (let i = 0; i < NUMBER_OF_PIPES; i++) {
		let change_in_x = 120;
		pipes.push(
			new Pipe(130 + (change_in_x * i) , 180, 20, 20, 'blue'), 
			new Pipe(150 + (change_in_x * i) , 180, 80, 20, 'purple'), 
		);
	}
	
	let height = 100;
	let fillHeight = height * fillLevel;
	// const waterPipe = new WaterPipe(110, 210 - fillHeight, 18, fillHeight , "#afeeee");
	
	// Four pipes
	for (let i = 0; i < NUMBER_OF_TANKS; i++) {
		let change_in_x = 120;
		pipes.push(
			new WaterPipe(110 + (change_in_x * i) , 210 - fillHeight, 20, fillHeight , "#afeeee"),
			new Pipe(110 + (change_in_x * i), 110, 20, 100, '#000000')
		);
	}
	
	
	for (let i = 0 ; i < pipes.length; i++ ) {
		pipes[i].render();
	}
		
}

const renderLoop = () => {
	// Render background
	ctx.clearRect(0, 0, width, height);
	
	drawScene();
	
	fillLevel += 0.005;
	console.log(fillLevel);
	if (fillLevel > 1) { fillLevel = 0;}
	
	requestAnimationFrame(renderLoop);
};

renderLoop();