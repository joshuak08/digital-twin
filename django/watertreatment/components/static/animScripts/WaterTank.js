import {Fillable} from './Fillable.js';
import {waterBG} from './AnimController.js';

export class WaterTank extends Fillable {
  constructor(xCoord, yCoord, waterWidth, waterHeight, colour, ctx_layer2, tank_num, scada_controller) {
    super(xCoord, yCoord, waterWidth, waterHeight, colour);

    // this.currentLevel = (initialLevel- y)/((y+h)-y) // initiallevel normalised to within pixel height of tank
    this.json_list_simdata = JSON.parse(JSON.parse(document.getElementById('all_SimData').textContent));
    this.json_list = Object.entries(this.json_list_simdata);
    this.valueIdx = 0;
    this.valuesArr = Object.entries(this.json_list_simdata).filter((fields) => fields[1]['pk'] === (tank_num)).map((fields) => fields[1]['fields']['water_vol']);
    this.currentLevel = this.valuesArr[0];
    this.ctx_layer2 = ctx_layer2;
    this.ctx_layer2.fillStyle = colour;
    this.scada_controller = scada_controller;
    this.tank_num = tank_num;
    this.differences = [];
    this.water_change = 0;

    this.particulate_range = 500000;
    this.progress = 0;
    this.progress_rate = 0;
    this.num_of_changes;

    this.current_particulate = 0;
    this.next_particulate = 0;

    this.water_rate_update();
    this.counter = 0;
  }

  water_rate_update() {
    // code for getting flow rates to sync so the next snapshot is reached simultaneously
    this.differences = [];
    // const next_snapshot_data_water_vol = this.json_list.filter((fields) => fields[1]['pk'] === (this.tank_num) && fields[1]['fields']['snap_num'] === this.valueIdx).map((fields) => fields[1]['fields']['water_vol']);
    // const current_snapshot_data_water_vol = this.json_list.filter((fields) => fields[1]['pk'] === (this.tank_num) && fields[1]['fields']['snap_num'] === this.valueIdx-1).map((fields) => fields[1]['fields']['water_vol']);
    // const current_difference = Math.abs(current_snapshot_data_water_vol-next_snapshot_data_water_vol);
    const current_difference = this.scada_controller.change_rate_tank((this.valueIdx), this.tank_num);

    for (let tank_num = 0; tank_num < 4; tank_num++ ) {
      this.differences.push(this.scada_controller.change_rate_tank((this.valueIdx-1), tank_num));
    }

    this.water_change = current_difference/(Math.max(...this.differences))/2;
  }

  // colour stuff
  hex_to_rgba_formatted(colour) {// colour, alpha = 1
    const [r, g, b] = colour.match(/\w\w/g).map((x) => parseInt(x, 16));
    return [r, g, b];
  }

  format_rgba = (colour) => {
    return `rgba(${colour.r},${colour.g},${colour.b},${colour.a})`;
  };

  interpolate_colour(progress) {
    const [r1, g1, b1] = this.hex_to_rgba_formatted('#047a47');// '#ADD8E6'
    const [r2, g2, b2] = this.hex_to_rgba_formatted('#ADD8E6');// '#047a47'
    return this.format_rgba({
      r: Math.round(((r1 * progress) + (r2 * (1.0-progress)))),
      g: Math.round(((g1 * progress) + (g2 * (1.0-progress)))),
      b: Math.round(((b1 * progress) + (b2 * (1.0-progress)))),
      a: 1,
    });
  }

  update_water_colour() {
    // const percent_range = 100;
    // this.progress = ((particulate * percent_range) / particulate_range)/100.0; // scales particulate to (0-100) range
    this.progress += this.progress_rate;
    // console.log(this.progress)

    return String(this.interpolate_colour(this.progress));
  }

  progress_rate_update() {
    // const water_range = Math.abs(this.currentLevel - this.valuesArr[this.valueIdx]);
    const old_particulate = this.scada_controller.get_particulate_level(this.valueIdx-1, this.tank_num);
    const new_particulate = this.scada_controller.get_particulate_level(this.valueIdx, this.tank_num);
    // console.log("counter", this.counter, "index:",this.valueIdx-1)
    console.log(old_particulate, new_particulate);
    const old_progess = ((old_particulate) * 100)/this.particulate_range;
    const new_progress = ((new_particulate) * 100)/this.particulate_range;

    const pos_neg = (old_particulate <= new_particulate) ? 1 : -1;
    // NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
    this.progress_rate = ((Math.abs(old_progess-new_progress)/this.num_of_changes * pos_neg)/100.0);
    // console.log("progress:",this.progress.toFixed(2),"progress_rate:",this.progress_rate, "num of changes:",this.num_of_changes, "pos/neg:", pos_neg)
  }

  draw() {
    if (this.valueIdx < this.valuesArr.length) {
      // if the next snapshot water level value is reached move onto the next snapshot
      if (Math.abs(this.currentLevel - this.valuesArr[this.valueIdx]) < 0.00000000001) {
        this.currentLevel = this.valuesArr[this.valueIdx];
        this.valueIdx += 1;
        this.water_rate_update();
        this.num_of_changes = (Math.abs(this.currentLevel - this.valuesArr[this.valueIdx]))/this.water_change;
        // this.counter +=1
        this.progress_rate_update(this.water_change);
        // console.log("progress rate:", this.progress*100)
        // if the current water level is greater than the next water level decrease by the calculated rate of change
      } else if (this.currentLevel > this.valuesArr[this.valueIdx]) {
        this.currentLevel -= this.water_change;
        // if the current water level is less than the next water le   vel decrease by the calculated rate of change
      } else if (this.currentLevel < this.valuesArr[this.valueIdx]) {
        this.currentLevel += this.water_change;
      }
      // TODO: UPDATE WATER COLOUR HERE
      waterBG(this.tank_num, this.update_water_colour());
      // waterBG(this.tank_num)
      // if the current snapshot isn't the last update then animate by drawing the water height (this is done via a black square to give illusion of water level dipping/increasing)

      this.ctx_layer2.fillRect(this.x, this.y, this.w, this.h - this.currentLevel);

      // calls the scada screen controller to sync the current water level of tank with the current water level data displayed on the scada screen
      // TODO: REMOVE REDUNDANT ATTRIBUTES
      this.scada_controller.draw(this.tank_num, (this.valueIdx-1), ['component name : '+'tank ' + this.tank_num, 'live water vol: '+ this.currentLevel.toFixed(2), 'live particulate level:'+ this.particulate_range*(this.progress.toFixed(1))]);
    }
    // console.log(this.progress, this.progress_rate)
  }
}
