import {Fillable} from './Fillable.js';
import {waterBG} from './AnimController.js';

export class WaterTank extends Fillable {
  constructor(xCoord, yCoord, waterWidth, waterHeight, colour, ctx_layer2, tankNum, scada_controller) {
    super(xCoord, yCoord, waterWidth, waterHeight, colour);

    // this.currentLevel = (initialLevel- y)/((y+h)-y) // initiallevel normalised to within pixel height of tank
    this.json_list_simdata = JSON.parse(JSON.parse(document.getElementById('all_SimData').textContent));
    this.json_list = Object.entries(this.json_list_simdata);
    this.valueIdx = 1;
    this.valuesArr = Object.entries(this.json_list_simdata).filter(fields => fields[1]['pk'] === (tankNum)).map((fields) => fields[1]['fields']['water_vol']);
    this.currentLevel = this.valuesArr[0];
    this.ctx_layer2 = ctx_layer2;
    this.ctx_layer2.fillStyle = colour;
    this.scada_controller = scada_controller;
    this.tankNum = tankNum;
    this.differences = [];
    this.water_change = 0;

    this.water_rate_update()
  }

  water_rate_update(){
    console.log("herw")
    // code for getting flow rates to sync so the next snapshot is reached simultaneously
    let next_snapshot_data_water_vol = this.json_list.filter((fields) => fields[1]['pk'] === (this.tankNum) && fields[1]['fields']['snap_num'] === this.valueIdx).map((fields) => fields[1]['fields']['water_vol']);
    let current_snapshot_data_water_vol = this.json_list.filter((fields) => fields[1]['pk'] === (this.tankNum) && fields[1]['fields']['snap_num'] === this.valueIdx-1).map((fields) => fields[1]['fields']['water_vol']);
    // console.log(json_list.filter((fields) => fields[1]['pk'] === (tankNum) && fields[1]['fields']['snap_num'] === this.valueIdx-1))
    const current_difference = Math.abs(current_snapshot_data_water_vol-next_snapshot_data_water_vol);

    for (let tankNum = 0; tankNum < 4; tankNum++ ) {
      this.differences.push(this.scada_controller.change_rate_tank((this.valueIdx-1), tankNum));
    }

    this.water_change = current_difference/(Math.max(...this.differences))/2;
  }

  //TODO:
  update_water_colour(colour){
    this.ctx_layer2.fillstyle = colour;
  }

  draw() {
    // if the next snapshot water level value is reached move onto the next snapshot
    if (Math.abs(this.currentLevel - this.valuesArr[this.valueIdx]) < 0.00000000001) {
      this.currentLevel = this.valuesArr[this.valueIdx];
      this.valueIdx += 1;
      this.diffrences = [];
      this.water_rate_update();
      // if the current water level is greater than the next water level decrease by the calculated rate of change
    } else if (this.currentLevel > this.valuesArr[this.valueIdx]) {
      this.currentLevel -= this.water_change;
      // if the current water level is less than the next water le   vel decrease by the calculated rate of change
    } else if (this.currentLevel < this.valuesArr[this.valueIdx]) {
      this.currentLevel += this.water_change;
    }
    // if the current snapshot isn't the last update the animation by drawing the water height (this is done via a black square to give illusion of water level dipping/increasing)
    if (this.valueIdx <= this.valuesArr.length) {
      waterBG(this.tankNum);
      this.ctx_layer2.fillRect(this.x, this.y, this.w, this.h - this.currentLevel);

      // calls the scada screen controller to sync the current water level of tank with the current water level data displayed on the scada screen
      // this.scada_controller.draw(('tank'+ this.tankNum), (this.valueIdx-1), ['component name : '+'tank' + this.tankNum, 'current water lvl : '+ this.currentLevel.toFixed(2), 'valuesArr :' + this.valuesArr]);
      this.scada_controller.draw(this.tankNum, (this.valueIdx-1), ['component name : '+'tank' + this.tankNum, 'current water lvl : '+ this.currentLevel.toFixed(2), 'valuesArr :' + this.valuesArr]);

    }
  }
}
