import { Fillable } from "./Fillable.js"
import { waterBG } from "./AnimController.js"
import { ScadaController } from "./ScadaController.js";

export class WaterTank extends Fillable{
    constructor(TLCoord, y, waterWidth, waterHeight, colour, ctx_layer2, tankNum, scada_controller) {
		super(TLCoord, y, waterWidth, waterHeight, colour);

        // this.currentLevel = (initialLevel- y)/((y+h)-y) // initiallevel normalised to within pixel height of tank
        this.json_list_simdata = JSON.parse(JSON.parse(document.getElementById('all_SimData').textContent));
        this.valueIdx = 1;
        this.valuesArr = (Object.entries(this.json_list_simdata)).filter(fields => fields[1]["pk"] === ("tank" + (tankNum))).map(fields => fields[1]["fields"]["waterLevel"])
        this.currentLevel = this.valuesArr[0];
        this.ctx_layer2 = ctx_layer2;
        this.ctx_layer2.fillStyle = colour;
        this.scada_controller = scada_controller
        this.tankNum = tankNum
	};

    draw(){
        // rectangle height
        let x = 60 + this.tankNum*200;
        let y = 210;
        let width = 80;
        let height = 153;

        if (this.currentLevel > this.valuesArr[this.valueIdx]){
            this.currentLevel -= 0.5;

        } else if (this.currentLevel < this.valuesArr[this.valueIdx]){
            this.currentLevel += 0.5;

        } else if (this.valueIdx > this.valuesArr.length){

        }
        else if (this.currentLevel === this.valuesArr[this.valueIdx]) {
            this.currentLevel = this.valuesArr[this.valueIdx];
            this.valueIdx += 1;
        }

        waterBG(this.tankNum)
        this.ctx_layer2.fillRect(x,y,width, height - this.currentLevel);
        // draws scada stuff
        this.scada_controller.draw(("tank"+(this.valueIdx)), (this.valueIdx), ["current water lvl : "+this.currentLevel, "component name : "+"tank" + this.tankNum, "valuesArr :" + this.valuesArr])

    }
}