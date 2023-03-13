export class ScadaController {
  constructor(scada_context) {
    this.json_list_simdata = JSON.parse(JSON.parse(document.getElementById('all_SimData').textContent));
    this.scada_context = scada_context;
  }

  // clears the canvas
  clearScada() {
    this.scada_context.clearRect(0, 0, 250, 285);
  }

  // returns the differences between the current and next snapshot water levels in tanks
  change_rate_tank(current_snapshot, tankNum) {
    const json_list = (Object.entries(this.json_list_simdata));
    // filter for next snapshots and current snapshot
    const next_snapshot_data = json_list.filter((fields) => fields[1]['pk'] === ('tank'+tankNum) && fields[1]['fields']['snapshots'] === current_snapshot+1).map((fields) => fields[1]['fields']['waterLevel']);
    const current_snapshot_data = json_list.filter((fields) => fields[1]['pk'] === ('tank'+tankNum) && fields[1]['fields']['snapshots'] === current_snapshot).map((fields) => fields[1]['fields']['waterLevel']);
    return Math.abs(current_snapshot_data - next_snapshot_data);
  }

  // returns an array of form ["field : fieldValue"]
  format_scada_text(snapshot_data, component_specific_data) {
    const text = [];
    // puts key and values into text array e.g. ["water level": 5] based off database column names
    for (let field_num = 0; field_num < Object.entries(snapshot_data['fields']).length; field_num++) {
      text.push(Object.keys(snapshot_data['fields'])[field_num] + ' : ' + Object.values(snapshot_data['fields'])[field_num]);
    }
    // returns the concatenation between any extra data passed in and the current fields found in the data from the database
    return component_specific_data.concat(text);
  }

  // draws the data onto the canvas
  draw(component_name, snapshot_num, component_specific_data) {
    // filters for correct tank and snapshot. (the field that contains the water level sand displacement etc.)
    const snapshot_data = ((Object.entries(this.json_list_simdata)).filter((fields) => fields[1]['pk'] === (component_name) && fields[1]['fields']['snapshots'] === snapshot_num))[0][1];
    // sets font and font size
    this.scada_context.font = '20px serif';
    // gets the pieces of text to be drawn onto scada canvas
    const text_pieces = this.format_scada_text(snapshot_data, component_specific_data);
    // clears the canvas for new data
    this.clearScada();
    // actually draws the stuff on the canvas
    for (let field_num=0; field_num < text_pieces.length; field_num++) {
      this.scada_context.fillText(text_pieces[field_num], 2, 15 + field_num*20);
    }
  }
}
