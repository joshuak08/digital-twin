// export const drawText = (canvas, boxNum) => {
//     canvas.font = "48px serif";
//     canvas.fillText(`Scada: ${boxNum}`, 10, 50);
// };

console.log(JSON.parse(JSON.parse(document.getElementById('all_SimData').textContent)));
// first parse converts to list second converts to json list

export class ScadaController{
    constructor(scada_contexts){
        this.json_list_simdata = JSON.parse(JSON.parse(document.getElementById('all_SimData').textContent));
        this.scada_contexts = scada_contexts;
    }

    clearScada(){
        for (let scada_num=0; scada_num < 4; scada_num++) {
            this.scada_contexts[scada_num].clearRect(0, 0, 250,     285);
        }
    }

    format_json(scada_num, snapshot_num){ // input = this.json_list_simdata[scada_num].fields
        // let text = []
        // console.log("field length:" + Object.keys(scada_json).length);
        //
        // text.push("component-name : " + component_name)
        // for (let field_num=0; field_num < Object.keys(scada_json).length; field_num++){
        //
        //
        //     let field = Object.keys(scada_json)[field_num];
        //     text.push(field+ " : " + scada_json[field]);
        // }
        // return text;
        let text = []
        let fields = (Object.entries(this.json_list_simdata).filter(([entry_num, json]) => json.pk === "tank1").filter(([entry_num, json]) => json.fields.snapshots === 1).map(([entry_num, json]) => json.fields))
        console.log(fields)
        // let tank_name = Object.keys(this.scada_contexts).map().filter(field => field === ("tank"+scada_num))
    }

    //filter correct component first then filter for snapshot number

    draw(snapshot_num){ //JSON.parse(this.json_list_simdata[scada_num])
        // for (let scada_num=0; scada_num < 4; scada_num++) {
        //     this.scada_list[scada_num].font = "20px serif";
        //     let simdata = this.json_list_simdata;
        //
        //     for (let field_num=0; field_num < Object.keys(simdata[scada_num].fields).length+1; field_num++) {
        //
        //         let text_piece = this.format_json(scada_num)[field_num];
        //
        //         this.scada_list[scada_num].fillText(text_piece, 2, 15 + field_num*20)
        //     }
        // }
    }


}
// probably should handle the sql stuff ajax and what not
// once data is retrieved convert it to array from, unsure on how to sync pipe and tanks but can worry about that later