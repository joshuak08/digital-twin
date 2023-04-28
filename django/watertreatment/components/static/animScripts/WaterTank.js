import {Fillable} from './Fillable.js';
import {waterBG} from './AnimController.js';

export class WaterTank extends Fillable {
  constructor(xCoord, yCoord, waterWidth, waterHeight, colour, ctx_layer2, tank_num, scada_controller) {
    super(xCoord, yCoord, waterWidth, waterHeight, colour);

    this.tank_numIdx = tank_num;
    this.idx_offset = 9; // offset of tank id from tank index in tank array
    this.tank_ID = tank_num + this.idx_offset; // tank id in db
    this.tanks = [];

    this.json_list_simdata = JSON.parse(JSON.parse(document.getElementById('all_SimData').textContent)); // raw json data from db
    this.json_list = Object.entries(this.json_list_simdata); // snapshot json in array
    this.valueIdx = 1; // next value in array index
    this.valuesArr = Object.entries(this.json_list_simdata).filter((fields) => fields[1]['pk'] === (this.tank_ID)).map((fields) => (fields[1]['fields']['water_vol']*163/56)); // water vols for tank in db
    this.backwashArr = Object.entries(this.json_list_simdata).filter((fields) => fields[1]['pk'] === (this.tank_ID)).map((fields) => (fields[1]['fields']['backwash']));
    this.currentLevel = this.valuesArr[0];

    this.ctx_layer2 = ctx_layer2; // the animation layer
    this.colour = colour; // dark grey
    this.scada_controller = scada_controller;
    this.waterWidth = waterWidth;
    this.waterHeight = waterHeight;
    this.differences = [];

    this.water_change = 0; // how much the water should change after each loop
    this.particulate_range = 500000;
    this.progress = 0; // how much the particulate is progressing towards the next particulate level in db
    this.progress_rate = 0; // rate of change of particulate
    this.num_of_changes = 0; // number of times the water vol is updated

    this.counter = 0; // counter to keep updating water volumes in correct order
  }
  // does setup for tanks
  setup_tank(tank_arr) {
    this.tanks = tank_arr;
    this.water_rate_update();
    this.num_of_changes = this.water_change ? (Math.abs(this.currentLevel - this.valuesArr[this.valueIdx])) / parseFloat(this.water_change) : 0;
    this.progress_rate_update();
  }
  // code for getting flow rates to sync so the next snapshot is reached simultaneously
  water_rate_update() {
    this.differences = [];
    const current_difference = (this.scada_controller.change_rate_tank(this.valueIdx, this.tank_ID)); // difference in curr water level to next snap
    for (let tank_num = 0; tank_num < 4; tank_num++ ) {
      this.differences.push(this.scada_controller.change_rate_tank(this.valueIdx, tank_num+this.idx_offset));// stores the changes in water vol for each tank in this.differences
    }
    this.water_change = (current_difference/parseFloat(Math.max(...this.differences)));
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
    if (!(this.progress + this.progress_rate < 0 || this.progress + this.progress_rate > 1)) {
      this.progress += this.progress_rate;
    }
    return String(this.interpolate_colour(this.progress));
  }

  progress_rate_update() {
    const old_particulate = this.scada_controller.get_particulate_level(this.valueIdx - 1, this.tank_ID);
    const new_particulate = this.scada_controller.get_particulate_level(this.valueIdx, this.tank_ID);
    const old_scaled_particulate = ((old_particulate) * 100) / parseFloat(this.particulate_range);
    const new_scaled_particulate = ((new_particulate) * 100) / parseFloat(this.particulate_range);
    // pos_neg determines if colour should go towards green or blue
    const pos_neg = (old_particulate <= new_particulate) ? 1 : -1;
    // different behaviour depending on if the next water vol is identical to current water vol
    if (!(this.valuesArr[this.valueIdx - 1] === this.valuesArr[this.valueIdx])) {
      // NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin // rescale colour change to 0 to 1
      this.progress_rate = ((Math.abs(old_scaled_particulate - new_scaled_particulate) / parseFloat(this.num_of_changes)) / 100.0 * pos_neg);
    } else {
      // as the number of changes are 0 the largest number of changes is selected out of all tanks
      this.progress_rate = Math.abs(old_scaled_particulate - new_scaled_particulate) / parseFloat(Math.max(...this.tanks.map((tank) => tank.num_of_changes))) / 100.0 * pos_neg;
    }
  }
  // ==========colour stuff==========
  // checks the elegibility of progressing on to next water vol depending on if identical values are present
  elegibility_duplicate_val() {
    let elegibility = true;
    if ((this.valuesArr[this.valueIdx-1] === this.valuesArr[this.valueIdx])) {
      for (let tank_num = 1; tank_num < 4; tank_num++) {
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
    // if (elegibility === true && this.tank_ID===9) {
    //   // this.calc_helper();
    // }
    if (elegibility === true){
      for (let tank_num = 0; tank_num < 4; tank_num++) { // checks if the next value of all tanks are identical to previous value
        const tank = this.tanks[tank_num];
        tank.calc_helper()
        tank.progress = this.scada_controller.get_particulate_level(tank.valueIdx - 1, tank.tank_ID) * 100 / parseFloat(tank.particulate_range);
      }
    }
  }

  check_update_elegibility(){
    //this checks if values are really close but not identical
    return (Math.abs(this.currentLevel - this.valuesArr[this.valueIdx]) < 0.000000000000000000001)
  }

  calc_helper() {
    this.counter += 1;
    this.currentLevel = this.valuesArr[this.valueIdx];
    this.valueIdx += 1;
    this.water_rate_update();
    this.num_of_changes = this.water_change ? (Math.abs(this.currentLevel - this.valuesArr[this.valueIdx])) / parseFloat(this.water_change) : 0;
  }

  calculate_rates() {
    if (this.valueIdx <= this.valuesArr.length - 1) {
      this.elegibility_all_duplicate();
      // if the next snapshot water level value is reached move onto the next snapshot
      if (this.elegibility_duplicate_val() && this.check_update_elegibility()) {
        this.calc_helper();
        // if the current water level is greater than the next water level decrease by the calculated rate of change
      } else if (this.currentLevel > this.valuesArr[this.valueIdx]) {
        this.currentLevel -= this.water_change;
        if (Math.abs(this.currentLevel - this.valuesArr[this.valueIdx]) < 0.5) {
          this.water_change *= 0.5
        }
        // if the current water level is less than the next water level decrease by the calculated rate of change
      } else if (this.currentLevel < this.valuesArr[this.valueIdx]) {
        this.currentLevel += this.water_change;
        if (Math.abs(this.currentLevel - this.valuesArr[this.valueIdx]) < 0.5) {
          this.water_change *= 0.5
        }
      }
    }
  }

  draw() {
    // draw the shizzle
    waterBG(this.tank_numIdx, this.update_water_colour());
    // if the current snapshot isn't the last update then animate by drawing the water height (this is done via a black square to give illusion of water level dipping/increasing)
    this.ctx_layer2.fillStyle = this.colour;
    this.ctx_layer2.fillRect(this.x, this.y, this.w, this.h - this.currentLevel); // (this.h is the maximum water height)
    // calls the scada screen controller to sync the current water level of tank with the current water level data displayed on the scada screen
    this.scada_controller.draw(this.tank_ID, (this.valueIdx), ['component: ' + 'tank ' + this.tank_ID, 'live water vol: ' + (this.currentLevel*56/163.0).toFixed(2) + ' m³', 'live particulate: ' + this.particulate_range * (this.progress.toFixed(1)) + ' mg', "=========target values========"]);

    this.ctx_layer2.font = '13px Impact';
    this.ctx_layer2.clearRect(this.x+this.w+13, this.h-this.currentLevel+this.y-10, 50, 20)
    this.ctx_layer2.fillText((this.currentLevel*56/163.0).toFixed(2)+"m³", this.x+this.w+15, this.h-this.currentLevel+this.y+5);

    if (this.backwashArr[this.valueIdx - 1] === true) {
      this.ctx_layer2.font = '15px Impact';
      this.ctx_layer2.fillStyle = 'red';
      this.ctx_layer2.fillText('BACKWASH', this.x + 6, this.y + 15);
    }
  }
}

