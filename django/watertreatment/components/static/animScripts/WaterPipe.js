import Fillable from "./Fillable.js"

export default class WaterPipe extends Fillable {
	constructor(x, y, w, h, colour, fillHeight, ctx) {
		super(x, y, w, h, colour, ctx);
		this.fillHeight = fillHeight;
	}

	render() {
		this.ctx.fillStyle = this.colour;
		this.ctx.fillRect(this.x, this.y, this.w, this.h);
	}
} 
