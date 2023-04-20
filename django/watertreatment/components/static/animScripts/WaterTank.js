import {Fillable} from './Fillable.js';
import {waterBG} from './AnimController.js';

export class WaterTank extends Fillable {
  constructor(xCoord, yCoord, waterWidth, waterHeight, colour, ctx_layer2, tank_num, scada_controller) {
    super(xCoord, yCoord, waterWidth, waterHeight, colour);

    this.json_list_simdata = JSON.parse(JSON.parse(document.getElementById('all_SimData').textContent));
    this.json_list = Object.entries(this.json_list_simdata);
    this.valueIdx = 0;
    this.valuesArr = Object.entries(this.json_list_simdata).filter((fields) => fields[1]['pk'] === (tank_num)).map((fields) => fields[1]['fields']['water_vol']);
    this.currentLevel = this.valuesArr[0];
    this.ctx_layer2 = ctx_layer2;
    this.ctx_layer2.fillStyle = colour;
    this.scada_controller = scada_controller;
    this.tank_num = tank_num;
    this.waterWidth = waterWidth;
    this.waterHeight = waterHeight;
    this.differences = [];
    this.water_change = 0;

    this.particulate_range = 500000
    this.progress = 0;
    this.progress_rate = 0;
    this.num_of_changes = 0;
    this.next_particulate = 0;
  }

  // code for getting flow rates to sync so the next snapshot is reached simultaneously
  water_rate_update() {
    this.differences = [];
    const current_difference = (this.scada_controller.change_rate_tank((this.valueIdx), this.tank_num));
    if (this.tank_num===0){console.log(this.valuesArr[this.valueIdx-1])} ////////////////
    for (let tank_num = 0; tank_num < 4; tank_num++ ) { //stores the changes in water vol for each tank in this.differences
      this.differences.push(this.scada_controller.change_rate_tank((this.valueIdx), tank_num));
    }

    this.water_change = current_difference/(Math.max(...this.differences))/2

  }

  // colour stuff
  hex_to_rgba_formatted(colour) {// colour, alpha = 1
    const [r, g, b] = colour.match(/\w\w/g).map((x) => parseInt(x, 16));
    return [r, g, b, 1];
  }

  format_rgba(colour){
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
    });
  }

  update_water_colour() {
    this.progress += this.progress_rate;
    return String(this.interpolate_colour(this.progress));
  }

  progress_rate_update(){

    const old_particulate = this.scada_controller.get_particulate_level(this.valueIdx-1, this.tank_num)
    const new_particulate = this.scada_controller.get_particulate_level(this.valueIdx, this.tank_num)
    const old_scaled_particulate = ((old_particulate) * 100)/this.particulate_range;
    const new_scaled_particulate = ((new_particulate) * 100)/this.particulate_range;
    //determines if colour should go towards green or blue
    let pos_neg = (old_particulate <= new_particulate) ? 1 : -1;
    //NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin // rescale colour change to 0 to 1
    this.progress_rate = (this.num_of_changes) ? ((Math.abs(old_scaled_particulate-new_scaled_particulate)/this.num_of_changes * pos_neg)/100.0) : 0
    // if (this.tank_num===0){console.log("progress_rate: ",this.progress_rate*100, "snap:", this.valueIdx-1)}
    // if (this.tank_num===0){console.log(old_particulate, new_particulate)}
    // console.log("progress:",this.progress.toFixed(2),"progress_rate:",this.progress_rate, "num of changes:",this.num_of_changes, "pos/neg:", pos_neg)
  }

  draw() {
    if (this.valueIdx <= this.valuesArr.length-1) {
      // console.log(this.valuesArr.length)
      // if the next snapshot water level value is reached move onto the next snapshot
      if (Math.abs(this.currentLevel - this.valuesArr[this.valueIdx]) < 0.00000000001) { // TODO: only if all tanks are equal to the next one and if all next are same sleep
        this.currentLevel = this.valuesArr[this.valueIdx];
        this.valueIdx += 1;
        this.water_rate_update();
        this.num_of_changes = this.water_change ? (Math.abs(this.currentLevel - this.valuesArr[this.valueIdx])) / this.water_change : 0
        // this.progress_rate_update();
        // if the current water level is greater than the next water level decrease by the calculated rate of change
      } else if (this.currentLevel > this.valuesArr[this.valueIdx]) {
        this.currentLevel -= this.water_change;
        // if the current water level is less than the next water le   vel decrease by the calculated rate of change
      } else if (this.currentLevel < this.valuesArr[this.valueIdx]) {
        this.currentLevel += this.water_change;
      }
      //UPDATE WATER COLOUR HERE
      waterBG(this.tank_num)
      // waterBG(this.tank_num, this.update_water_colour());
      // if the current snapshot isn't the last update then animate by drawing the water height (this is done via a black square to give illusion of water level dipping/increasing)
      this.ctx_layer2.fillRect(this.x, this.y, this.w, this.h - this.currentLevel); // (this.h is the maximum water height)
      // calls the scada screen controller to sync the current water level of tank with the current water level data displayed on the scada screen
      this.scada_controller.draw(this.tank_num, (this.valueIdx-1), ['component name : '+'tank ' + this.tank_num, 'live water vol: '+ this.currentLevel.toFixed(2), 'live particulate level:'+ this.particulate_range*(this.progress.toFixed(1))]);
    }
  }
}
