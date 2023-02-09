import Fillable from "./Fillable.js"

export default class WaterTank extends Fillable {
	constructor(x, y, w, h, colour, fillHeight, ctx) {
		super(x, y, w, h, colour, ctx);
		this.fillHeight = fillHeight;
		console.log(colour)
	}

	render() {
		this.ctx.fillStyle = this.colour;
		this.ctx.fillRect(this.x, this.y, this.w, this.h);
	}
} 