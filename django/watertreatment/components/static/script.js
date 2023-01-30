const canvas = document.getElementById('canvas');
// Tanks
const ctx = canvas.getContext('2d');
ctx.fillStyle = 'grey';
ctx.fillRect(30, 50, 100, 200);
ctx.fillRect(150, 50, 100, 200);
ctx.fillRect(270, 50, 100, 200);
ctx.fillRect(390, 50, 100, 200);

// Roofs
for (let i = 0; i < 4; i++) {
	let dx = 120;
	change_in_x = (dx * i) 
	ctx.beginPath();
	ctx.moveTo(30 + change_in_x, 250);
	ctx.lineTo(80 + change_in_x, 300);
	ctx.lineTo(130 + change_in_x, 250);
	ctx.closePath();
	ctx.fillStyle = 'grey';
	ctx.fill();
	ctx.stroke();
}

// Grey pipes
ctx.strokeStlye = 'grey';
ctx.strokeRect(130, 180, 20, 20);
ctx.strokeRect(250, 180, 20, 20);
ctx.strokeRect(370, 180, 20, 20);

// Blue pipes
const ctx2 = canvas.getContext("2d");
ctx2.strokeStyle = "blue";
ctx.strokeRect(110, 110, 20, 100);
ctx.strokeRect(230, 110, 20, 100);
ctx.strokeRect(350, 110, 20, 100);
ctx.strokeRect(470, 110, 20, 100);

// Purple pipes
const ctx3 = canvas.getContext("2d");
ctx3.strokeStyle = "purple";
ctx3.strokeRect(150, 180, 80, 20);
ctx3.strokeRect(270, 180, 80, 20);
ctx3.strokeRect(390, 180, 80, 20);