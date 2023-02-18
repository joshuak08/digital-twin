import { Fillable } from "./Fillable.js"
import { waterBG } from "./AnimController.js"

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
        this.tak = 0
        this.waterChange1 = 0.5

        let differences = []
        let json_list = (Object.entries(this.json_list_simdata))
        let next_snapshot_data = json_list.filter(fields => fields[1]["pk"] === ("tank"+tankNum) && fields[1]["fields"]["snapshots"] === this.valueIdx).map(fields => fields[1]["fields"]["waterLevel"])
        let current_snapshot_data = json_list.filter(fields => fields[1]["pk"] === ("tank"+tankNum) && fields[1]["fields"]["snapshots"] === this.valueIdx-1).map(fields => fields[1]["fields"]["waterLevel"])
        let current_difference = Math.abs(current_snapshot_data-next_snapshot_data)
        for (let tankNum = 0; tankNum < 4; tankNum++ ){
            differences.push(scada_controller.change_rate_tank((this.valueIdx-1), tankNum))
        }
        this.water_change = current_difference/(Math.max(...differences))/2

        // compare tank,snap1 - tank,snap2 for all tanks
	}

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