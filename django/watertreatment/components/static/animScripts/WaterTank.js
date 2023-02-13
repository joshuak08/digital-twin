import { Fillable } from "./Fillable.js"
import { waterBG } from "./AnimController.js"

export class WaterTank extends Fillable{
    constructor(TLCoord, y, waterWidth, waterHeight, colour, ctx_layer2, tankNum, valuesArr) {
		super(TLCoord, y, waterWidth, waterHeight, colour);
        // this.currentLevel = (initialLevel- y)/((y+h)-y) // initiallevel normalised to within pixel height of tank
        this.valueIdx = 1;
        this.valueArr = valuesArr;
        this.currentLevel = valuesArr[0];
        this.ctx_layer2 = ctx_layer2;
        this.ctx_layer2.fillStyle = colour;
        this.tankNum = tankNum;

	};

    draw(){
        // reactangle hegiht
        let x = 60 + this.tankNum*200;
        let y = 210;
        let width = 80;
        let height = 153;

        if (this.currentLevel > this.valueArr[this.valueIdx]){
            this.currentLevel -= 0.5;
        } else if (this.currentLevel < this.valueArr[this.valueIdx]){
            this.currentLevel += 0.5;
        } else if (this.currentLevel === this.valueArr[this.valueIdx]) {
            console.log(this.currentLevel);
            this.currentLevel = this.valueArr[this.valueIdx];
            this.valueIdx += 1;
        }

        waterBG(this.tankNum)
        this.ctx_layer2.fillRect(x,y,width, height - this.currentLevel);
    }
}