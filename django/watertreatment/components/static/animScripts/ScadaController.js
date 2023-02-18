console.log(JSON.parse(JSON.parse(document.getElementById('all_SimData').textContent)));

// first parse converts to list second converts to json list

export class ScadaController{
    constructor(scada_context){
        this.json_list_simdata = JSON.parse(JSON.parse(document.getElementById('all_SimData').textContent));
        this.scada_context = scada_context;
    }

    clearScada(){
        this.scada_context.clearRect(0, 0, 250,     285);
    }

    format_scada_text(snapshot_data, component_specific_data){ // input = this.json_list_simdata[scada_num].fields
        let text = []
        // puts key and values into text array e.g. "water level": 5 based off database column names
        for (let field_num = 0; field_num < Object.entries(snapshot_data["fields"]).length; field_num++){
            text.push(Object.keys(snapshot_data["fields"])[field_num] + " : " + Object.values(snapshot_data["fields"])[field_num])
        }
        return component_specific_data.concat(text)
    }

    draw(component_name ,snapshot_num, component_specific_data){

        //filters for correct tank and snapshot row where fields contain the water level sand displacement
        let snapshot_data = ((Object.entries(this.json_list_simdata)).filter(fields => fields[1]["pk"] === (component_name) && fields[1]["fields"]["snapshots"] === snapshot_num))

        snapshot_data = snapshot_data[0][1]


        this.scada_context.font = "20px serif"; // sets font and font size

        let text_pieces = this.format_scada_text(snapshot_data, component_specific_data)

        this.clearScada()
        for (let field_num=0; field_num < text_pieces.length; field_num++) {
            this.scada_context.fillText(text_pieces[field_num], 2, 15 + field_num*20)
        }
    }
}
