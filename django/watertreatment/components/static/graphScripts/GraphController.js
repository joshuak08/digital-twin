let ctx = document.getElementById("chart").getContext("2d");
let json_list_simdata = JSON.parse(JSON.parse(document.getElementById('all_SimData').textContent));
let data_array = Object.entries(json_list_simdata).map((fields) => combine_id_fields(fields)).map((fields) => fields[1]['fields'])

function combine_id_fields(json){
    json[1]['fields']['pk'] = json[1]['pk']
    return json
}

console.log(data_array)

let chart = new Chart(ctx, {
type: "line",
data: {
    labels: ["snapshot1", "snapshot2", "snapshot3", "snapshot4", "snapshot5", "snapshot6", "..."],
    datasets: [
        {
            label: "Tank 1 Water levels",
            //backgroundColor: "#79AEC8",
            //fill: false,
            borderColor: "rgb(75, 192, 192)",
            data: [65, 59, 40, 51, 46, 55, 50],
            tension: 0.1,
        },
        {
            label: "Tank 2 Water levels",
            //backgroundColor: "#79AEC8",
            borderColor: 'rgb(255, 99, 132)',
            data: [75, 59, 33, 61, 53, 65, 43],
            tension: 0.1,
        },
        {
            label: "Tank 3 Water levels",
            //backgroundColor: "#79AEC8",
            borderColor: 'rgb(255, 205, 86)',
            data: [65, 39, 34, 31, 43, 55, 53],
            tension: 0.1,
        },
        {
            label: "Tank 4 Water levels",
            //backgroundColor: "#79AEC8",
            borderColor: 'rgb(153, 102, 255)',
            data: [55, 59, 43, 51, 73, 55, 63],
            tension: 0.1,
        }
    ]
}
});