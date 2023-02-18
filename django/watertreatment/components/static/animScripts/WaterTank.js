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
        this.water_change = 0.5
        this.tak = 0

	};

    draw(){
        // rectangle height
        let x = 60 + this.tankNum*200;
        let y = 210;
        let width = 80;
        let height = 153;

        if (this.currentLevel > this.valuesArr[this.valueIdx]){
            this.currentLevel -= this.water_change;

        } else if (this.currentLevel < this.valuesArr[this.valueIdx]){
            this.currentLevel += this.water_change;

        } else if (this.currentLevel === this.valuesArr[this.valueIdx]) {
            this.currentLevel = this.valuesArr[this.valueIdx];
            this.valueIdx += 1;
        }

        if (this.valueIdx <= this.valuesArr.length){
            waterBG(this.tankNum)
            this.ctx_layer2.fillRect(x,y,width, height - this.currentLevel);
            // draws scada stuff
            this.scada_controller.draw(("tank"+this.tankNum), (this.valueIdx-1), ["component name : "+"tank" + this.tankNum,"current water lvl : "+this.currentLevel,  "valuesArr :" + this.valuesArr])
        }
    }
}