import {Fillable} from './Fillable.js';
import {waterBG} from './AnimController.js';

export class WaterTank extends Fillable {
  constructor(xCoord, yCoord, waterWidth, waterHeight, colour, ctx_layer2, tankNum, scada_controller) {
    super(xCoord, yCoord, waterWidth, waterHeight, colour);

    // this.currentLevel = (initialLevel- y)/((y+h)-y) // initiallevel normalised to within pixel height of tank
    this.json_list_simdata = JSON.parse(JSON.parse(document.getElementById('all_SimData').textContent));
    this.json_list = Object.entries(this.json_list_simdata);
    this.valueIdx = 1;
    this.valuesArr = Object.entries(this.json_list_simdata).filter((fields) => fields[1]['pk'] === (tankNum)).map((fields) => fields[1]['fields']['water_vol']);
    this.currentLevel = this.valuesArr[0];
    this.ctx_layer2 = ctx_layer2;
    this.ctx_layer2.fillStyle = colour;
    this.scada_controller = scada_controller;
    this.tankNum = tankNum;
    this.differences = [];
    this.water_change = 0;

    this.water_rate_update();
  }

  water_rate_update() {
    // code for getting flow rates to sync so the next snapshot is reached simultaneously
    this.diffrences = [];
    const next_snapshot_data_water_vol = this.json_list.filter((fields) => fields[1]['pk'] === (this.tankNum) && fields[1]['fields']['snap_num'] === this.valueIdx).map((fields) => fields[1]['fields']['water_vol']);
    const current_snapshot_data_water_vol = this.json_list.filter((fields) => fields[1]['pk'] === (this.tankNum) && fields[1]['fields']['snap_num'] === this.valueIdx-1).map((fields) => fields[1]['fields']['water_vol']);
    const current_difference = Math.abs(current_snapshot_data_water_vol-next_snapshot_data_water_vol);

    for (let tankNum = 0; tankNum < 4; tankNum++ ) {
      this.differences.push(this.scada_controller.change_rate_tank((this.valueIdx-1), tankNum));
    }

    this.water_change = current_difference/(Math.max(...this.differences))/2;
  }

  // TODO:
  hex_to_rgba_formatted(colour) {// colour, alpha = 1
    // let colour = "#046d7a"
    const [r, g, b] = colour.match(/\w\w/g).map((x) => parseInt(x, 16));
    return [r, g, b, 1];
  }

  format_rgba = (colour) => {
    return `rgba(${colour.r},${colour.g},${colour.b},${colour.a})`;
  };

  interpolate_colour(progress) {
    const [r1, g1, b1, a1] = this.hex_to_rgba_formatted('#047a47');//'#ADD8E6'
    const [r2, g2, b2, a2] = this.hex_to_rgba_formatted('#ADD8E6');//'#047a47'
    return this.format_rgba({
      r: Math.round(((r1 * progress) + (r2 * (1.0-progress)))),
      g: Math.round(((g1 * progress) + (g2 * (1.0-progress)))),
      b: Math.round(((b1 * progress) + (b2 * (1.0-progress)))),
      a: 1,
      // a: Math.round((a1 + a2) * progress),
    });
  }

  update_water_colour(particulate) {
    const particulate_range = 500000;
    const percent_range = 100;
    const progress = ((particulate * percent_range) / particulate_range)/100.0; // scales particulate to (0-100) range
    console.log(progress);
    return String(this.interpolate_colour(progress));
  }

  draw() {
    // if the next snapshot water level value is reached move onto the next snapshot
    if (Math.abs(this.currentLevel - this.valuesArr[this.valueIdx]) < 0.00000000001) {
      this.currentLevel = this.valuesArr[this.valueIdx];
      this.valueIdx += 1;
      this.water_rate_update();
      // if the current water level is greater than the next water level decrease by the calculated rate of change
    } else if (this.currentLevel > this.valuesArr[this.valueIdx]) {
      this.currentLevel -= this.water_change;
      // if the current water level is less than the next water le   vel decrease by the calculated rate of change
    } else if (this.currentLevel < this.valuesArr[this.valueIdx]) {
      this.currentLevel += this.water_change;
    }
    // TODO: UPDATE WATER COLOUR HERE
    waterBG(this.tankNum, this.update_water_colour(this.scada_controller.get_particulate_level(this.valueIdx-1)));
    // if the current snapshot isn't the last update then animate by drawing the water height (this is done via a black square to give illusion of water level dipping/increasing)
    if (this.valueIdx <= this.valuesArr.length) {
      this.ctx_layer2.fillRect(this.x, this.y, this.w, this.h - this.currentLevel);

      // calls the scada screen controller to sync the current water level of tank with the current water level data displayed on the scada screen
      // TODO: REMOVE REDUNDANT ATTRIBUTES
      this.scada_controller.draw(this.tankNum, (this.valueIdx-1), ['component name : '+'tank' + this.tankNum, 'current water lvl : '+ this.currentLevel.toFixed(2), 'valuesArr :' + this.valuesArr]);
    }
  }
}
