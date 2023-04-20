const Jtemp = (Object.entries(JSON.parse(JSON.parse(document.getElementById('all_SimData').textContent))));
// console.log(Jtemp);
// console.log(Jtemp.filter((fields) => fields[1]['pk'] === (0) && fields[1]['fields']['snap_num'] === 0).map((fields) => fields[1]['fields']));
// console.log( (Jtemp.filter(fields => fields[1]['pk'] === (0) && fields[1]['fields']['snap_num'] === 0))[0][1]['fields']['particulate'])

export class ScadaController {
  constructor(scada_context) {
    // this.json_list_simdata = JSON.parse(JSON.parse(document.getElementById('all_SimData').textContent));
    this.json_list_simdata = Object.entries(JSON.parse(JSON.parse(document.getElementById('all_SimData').textContent)));
    this.scada_context = scada_context;
  }

  get_particulate_level(snapshot_num, tank_num) {
    return this.json_list_simdata.filter((fields) => fields[1]['pk'] === (tank_num) && fields[1]['fields']['snap_num'] === snapshot_num)[0][1]['fields']['particulate'];
  }

  // clears the canvas
  clearScada() {
    this.scada_context.clearRect(0, 0, 250, 285);
  }

  // returns the differences between the current and next snapshot water levels in tanks
  change_rate_tank(next_snap_num, tankNum) {
    const json_list = this.json_list_simdata;
    // filter for next snapshots and current snapshot | (id integer, snap_num integer, water_vol integer, particulate integer, backwash boolean)
    // TODO<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< done
    const next_snapshot_data = json_list.filter((fields) => fields[1]['pk'] === (tankNum) && fields[1]['fields']['snap_num'] === next_snap_num).map((fields) => fields[1]['fields']['water_vol']);
    const current_snapshot_data = json_list.filter((fields) => fields[1]['pk'] === (tankNum) && fields[1]['fields']['snap_num'] === next_snap_num-1).map((fields) => fields[1]['fields']['water_vol']);
    const scaled_next = next_snapshot_data*163/56
    const scaled_curr = current_snapshot_data*163/56
    return Math.abs(scaled_curr - scaled_next);
  }

  // returns an array of form ["field : fieldValue"]
  format_scada_text(snapshot_data, component_specific_data) {
    const text = [];
    // puts key and values into text array e.g. ["water level": 5] based off database column names
    for (let field_num = 0; field_num < Object.entries(snapshot_data).length; field_num++) {
      text.push(Object.keys(snapshot_data)[field_num] + ' : ' + Object.values(snapshot_data)[field_num]);
    }
    // returns the concatenation between any extra data passed in and the current fields found in the data from the database
    return component_specific_data.concat(text);
  }

  // draws the data onto the canvas
  draw(component_name, snapshot_num, component_specific_data) {
    // filters for correct tank and snapshot. (the field that contains the water volume, snapshot number, particulate, etc.)
    const snapshot_data = this.json_list_simdata.filter((fields) => fields[1]['pk'] === (component_name) && fields[1]['fields']['snap_num'] === snapshot_num)[0][1]['fields'];
    // const snapshot_data = ((Object.entries(this.json_list_simdata)).filter((fields) => fields[1]['pk'] === (component_name) && fields[1]['fields']['snap_num'] === snapshot_num))[0][1];

    this.scada_context.font = '20px serif';// sets font and font size
    const text_pieces = this.format_scada_text(snapshot_data, component_specific_data);// gets the pieces of text to be drawn onto scada canvas
    this.clearScada();// clears the canvas for new data
    for (let field_num=0; field_num < text_pieces.length; field_num++) {// actually draws the stuff on the canvas
      this.scada_context.fillText(text_pieces[field_num], 2, 15 + field_num*20);
    }
  }
}

// (id integer, snap_num integer, water_vol integer, particulate integer, backwash boolean)
