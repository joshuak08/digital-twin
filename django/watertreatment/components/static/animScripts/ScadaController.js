export class ScadaController {
  constructor(scada_context, json_list_simdata) {
    this.json_list_simdata = json_list_simdata;
    this.scada_context = scada_context;
  }

  // clears the canvas
  clearScada() {
    this.scada_context.clearRect(0, 0, 250, 285);
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
    this.scada_context.font = '18px sans-serif';// sets font and font size
    const text_pieces = this.format_scada_text(snapshot_data, component_specific_data);// gets the pieces of text to be drawn onto scada canvas
    this.clearScada();// clears the canvas for new data
    for (let field_num=0; field_num < text_pieces.length; field_num++) {// actually draws the stuff on the canvas
      this.scada_context.fillText(text_pieces[field_num], 2, 15 + field_num*20);
    }
  }
}
