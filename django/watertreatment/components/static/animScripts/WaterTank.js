import {Fillable} from './Fillable.js';
import {waterBG} from './AnimController.js';
import {end_anim} from './AnimController.js';

export class WaterTank extends Fillable {
  constructor(xCoord, yCoord, waterWidth, waterHeight, colour, ctx_layer2, tank_num, scada_controller, json_list_simdata, starting_progress, testing=false) {
    super(xCoord, yCoord, waterWidth, waterHeight, colour);
    // tank attributes
    this.tank_numIdx = tank_num;
    this.idx_offset = 9; // offset of tank id from tank index in tank array
    this.tank_ID = tank_num + this.idx_offset; // tank id in db
    this.tanks = [];
    // value attributse
    this.json_list_simdata = (json_list_simdata); // snapshot json in array
    this.valueIdx = 1; // next value in array index
    this.valuesArr = json_list_simdata.filter((fields) => fields[1]['pk'] === (this.tank_ID)).map((fields) => (fields[1]['fields']['water_vol']*163/56)); // water vols for tank in db
    this.backwashArr = json_list_simdata.filter((fields) => fields[1]['pk'] === (this.tank_ID)).map((fields) => (fields[1]['fields']['backwash']));
    this.currentLevel = this.valuesArr[0];
    // canvas attributes
    this.ctx_layer2 = ctx_layer2; // the animation layer
    this.colour = colour; // dark grey
    this.scada_controller = scada_controller;
    this.differences = [];
    // drawing value attributes
    this.water_change = 0; // how much the water should change after each loop
    this.particulate_range = 11340000;
    this.progress = this.round_precision(starting_progress, 10**10);
    this.progress_rate = 0; // rate of change of particulate
    this.num_of_changes = 0; // number of times the water vol is updated
    this.num_of_prev_chngs = 0;
    // rate of change and synchroniser attributes
    this.counter = 0; // counter to keep updating water volumes in correct order
    this.increment = 0.1;
    this.testing = testing;
    this.end = false;
    this.testoutput = [];
  }
  // does setup for tanks
  setup_tank(tank_arr) {
    this.tanks = tank_arr;
    this.update_water_rate();
    this.num_of_changes = this.water_change ? (Math.abs(this.currentLevel - this.valuesArr[this.valueIdx])) / parseFloat(this.water_change) : 0;
    this.update_progress_rate();
  }

  get_particulate_level(snapshot_num, tank_num) {
    return this.json_list_simdata.filter((fields) => fields[1]['pk'] === (tank_num) && fields[1]['fields']['snap_num'] === snapshot_num)[0][1]['fields']['particulate'];
  }

  // returns the differences between the current and next snapshot water levels in tanks
  change_rate_tank(next_snap_num, tankNum) {
    const json_list = this.json_list_simdata;
    // filter for next snapshots and current snapshot | (id integer, snap_num integer, water_vol integer, particulate integer, backwash boolean)
    const next_snapshot_data = json_list.filter((fields) => fields[1]['pk'] === (tankNum) && fields[1]['fields']['snap_num'] === next_snap_num).map((fields) => fields[1]['fields']['water_vol']);
    const current_snapshot_data = json_list.filter((fields) => fields[1]['pk'] === (tankNum) && fields[1]['fields']['snap_num'] === next_snap_num-1).map((fields) => fields[1]['fields']['water_vol']);
    const scaled_next = next_snapshot_data;
    const scaled_curr = current_snapshot_data;
    return Math.abs(scaled_curr - scaled_next)* 163/56.0;
  }

  round_precision(number, decimal_precision=10**13) {
    return Math.round(number*decimal_precision)/decimal_precision;
  }
  // code for getting flow rates to sync so the next snapshot is reached simultaneously
  update_water_rate() {
    this.differences = [];
    const current_difference = (this.change_rate_tank(this.valueIdx, this.tank_ID)); // difference in curr water level to next snap
    this.water_change = this.round_precision(current_difference * this.increment);
  }
  // ==========colour stuff==========
  hex_to_rgba_formatted(colour) {// colour, alpha = 1
    const [r, g, b] = colour.match(/\w\w/g).map((x) => parseInt(x, 16));
    return [r, g, b];
  }
  // turns rgba into valid input for context fillstyle
  format_rgba(colour) {
    return `rgba(${colour.r},${colour.g},${colour.b},${colour.a})`;
  };
  // takes value and converts it into a mix of 2 colours specified
  interpolate_colour(progress) {
    const [r1, g1, b1] = this.hex_to_rgba_formatted('#047a47');// sewage green
    const [r2, g2, b2] = this.hex_to_rgba_formatted('#ADD8E6');// water blue

    return this.format_rgba({
      r: Math.round(((r1 * progress) + (r2 * (1.0-progress)))),
      g: Math.round(((g1 * progress) + (g2 * (1.0-progress)))),
      b: Math.round(((b1 * progress) + (b2 * (1.0-progress)))),
      a: 1,
    });
  }

  update_water_colour() {
    this.progress += this.progress_rate;
  }

  get_current_colour() {
    return String(this.interpolate_colour(this.progress));
  }
  // ===================================
  update_progress_rate() {
    if (!this.end) {
      const old_particulate = this.get_particulate_level(this.valueIdx - 1, this.tank_ID);
      const new_particulate = this.get_particulate_level(this.valueIdx, this.tank_ID);
      this.progress_rate = this.round_precision((new_particulate - old_particulate) / parseFloat(this.particulate_range) * this.increment);
    }
  }

  // checks the elegibility of progressing on to next water vol depending on if identical values are present
  elegibility_duplicate_val() {
    let elegibility = true;
    if ((this.valuesArr[this.valueIdx-1] === this.valuesArr[this.valueIdx])) {
      for (let tank_num = 0; tank_num < 4; tank_num++) {
        elegibility = elegibility && (this.counter < Math.max(...this.tanks.map((tank) => tank.counter))); // if all other tanks are ahead on counter move up
      } // this is to catch any other case of duplicate values that do not occur in all tanks
    }
    return elegibility;
  }

  elegibility_all_duplicate() {
    let elegibility = true;
    for (let tank_num = 0; tank_num < 4; tank_num++) { // checks if the next value of all tanks are identical to previous value
      const tank = this.tanks[tank_num];
      elegibility = elegibility && (tank.valuesArr[this.valueIdx-1] === tank.valuesArr[tank.valueIdx]);
    }

    if (elegibility === true) {
      const target_progress = this.get_particulate_level(this.valueIdx, this.tank_ID) / parseFloat(this.particulate_range);
      if (this.testing === true) {
        this.update_water_colour();
      }
      // this accounts for duplicates values at the start as there is no previous number of changes
      this.num_of_changes = this.valueIdx-1 ? this.num_of_prev_chngs : 163;
      // update water colour while duplicate value particulate aren't the same
      if (!(Math.abs(this.progress - target_progress) > 0.0000001)) {
        this.progress = target_progress;
        this.calc_helper();
      }
    }
    return elegibility;
  }

  check_update_elegibility() {
    // this checks if values are really close but not identical
    return (Math.abs(this.currentLevel - this.valuesArr[this.valueIdx]) < 0.0000000001);
  }

  // this moves along the simulation animation also updates water rate
  calc_helper() {
    this.counter += 1;
    // ensures current progress and water levels are correct due to floating point addition being weird e.g. 0.1 + 0.2 = 0.30000000000000004
    this.currentLevel = this.valuesArr[this.valueIdx];
    this.progress = this.get_particulate_level(this.valueIdx, this.tank_ID) / parseFloat(this.particulate_range);

    if (this.testing) { // if testing store current values at boundary
      this.testoutput.push([this.round_precision(this.currentLevel* 56 / 163.0, 10 ** 2), this.progress*this.particulate_range, this.tank_ID, this.valueIdx]);
    };
    this.valueIdx += ((this.valueIdx < this.valuesArr.length-1)? 1 : this.testing ? this.end=1 : end_anim());

    this.update_water_rate();
    this.num_of_prev_chngs = this.num_of_changes;
    this.num_of_changes = this.water_change ? (Math.abs(this.currentLevel - this.valuesArr[this.valueIdx])) / parseFloat(this.water_change) : 0;
  }

  calculate_rates() {
    this.update_water_colour();
    if (this.valueIdx < this.valuesArr.length) {
      if (!this.elegibility_all_duplicate()) {
        // if the next snapshot water level value is reached move onto the next snapshot
        if (this.elegibility_duplicate_val() && this.check_update_elegibility() ) {
          this.calc_helper();
          // if the current water level is greater than the next water level decrease by the calculated rate of change
        } else if (this.currentLevel > this.valuesArr[this.valueIdx]) {
          this.currentLevel -= this.water_change;
          // if the current water level is less than the next water level decrease by the calculated rate of change
        } else if (this.currentLevel < this.valuesArr[this.valueIdx]) {
          this.currentLevel += this.water_change;
        }
      }
    }
  }

  draw() {
    // draws frames of the tanks with changes applied
    waterBG(this.tank_numIdx, this.get_current_colour());
    // if the current snapshot isn't the last update then animate by drawing the water height (this is done via a black square to give illusion of water level dipping/increasing)
    this.ctx_layer2.fillStyle = this.colour;
    this.ctx_layer2.fillRect(this.x, this.y, this.w, this.h - this.currentLevel); // (this.h is the maximum water height)
    // calls the scada screen controller to sync the current water level of tank with the current water level data displayed on the scada screen
    this.scada_controller.draw(this.tank_ID, (this.valueIdx), ['Component: ' + 'Tank ' + this.tank_ID, 'Live Water Volume: ' + (this.currentLevel*56/163.0).toFixed(2) + ' m³', 'Live Particulate: ' + (this.particulate_range * this.progress).toFixed() + ' mg', 'Snapshot no: '+(this.valueIdx-1)+'->'+this.valueIdx, '――――――――――――――']);

    this.ctx_layer2.font = '13px Impact';
    this.ctx_layer2.clearRect(this.x+this.w+13, this.h-this.currentLevel+this.y-20, 50, 40);
    this.ctx_layer2.fillText((this.currentLevel*56/163.0).toFixed(2)+'m³', this.x+this.w+15, this.h-this.currentLevel+this.y+5);

    if (this.backwashArr[this.valueIdx - 1] === true) {
      this.ctx_layer2.font = '15px Impact';
      this.ctx_layer2.fillStyle = 'red';
      this.ctx_layer2.fillText('BACKWASH', this.x + 6, this.y + 15);
    }
  }
}

