export default class Fillable {
	constructor(x, y, w, h, colour, ctx) {
		this.x = x; 
		this.y = y;
		this.w = w;
		this.h = h;
		this.colour = colour;
        this.ctx = ctx;
	}

	render() {
		this.ctx.strokeStyle = this.colour;
		this.ctx.lineWidth = 3;
		this.ctx.strokeRect(this.x, this.y, this.w, this.h);
	}
}