const ctx = document.getElementById('chart').getContext('2d');
const json_list_simdata = JSON.parse(JSON.parse(document.getElementById('all_SimData').textContent));
const data_array = Object.entries(json_list_simdata).map((fields) => combine_id_fields(fields)).map((fields) => fields[1]['fields']);

function combine_id_fields(json) {
  json[1]['fields']['pk'] = json[1]['pk'];
  return json;
}

// Generate string of snapshot labels inline
const labels = Array.from(Array(((data_array).length/4)), (_, index) => 'Snapshot ' + (index + 1));
console.log(data_array);
// Filter JSON for unique key and get all related values
// { pk : { snapshot_num : water_vol  }, ... }
const pks = {};
data_array.forEach(function(a) {
  if (!pks[a.pk]) {
    pks[a.pk] = {};
  }; // if the pk is not already in the dict, initialse it
  pks[a.pk][a.snap_num] = a.water_vol;
});

// Convert JSON to array by iterating and extracting values from object
// [0 : [ water_vol, ... ], ...]
const tank_values = [];
// (IMPORTANT) Tank IDs are: 9, 10, 11, 12
for (let i = 9; i < 13; i++) {
  tank_values.push(Object.values(pks[i]));
}

// Create 4 lines charts for each tank
new Chart(ctx, {
  type: 'line',
  data: {
    labels: labels,
    datasets: [
      {
        label: 'Tank 1 Water Levels',
        borderColor: 'rgb(75, 192, 192)', // green
        data: tank_values[0],
        tension: 0.1, // curving of line
      },
      {
        label: 'Tank 2 Water Levels',
        borderColor: 'rgb(255, 99, 132)', // red
        data: tank_values[1],
        tension: 0.1,
      },
      {
        label: 'Tank 3 Water Levels',
        borderColor: 'rgb(255, 205, 86)', // yellow
        data: tank_values[2],
        tension: 0.1,
      },
      {
        label: 'Tank 4 Water Levels',
        borderColor: 'rgb(153, 102, 255)', // purple
        data: tank_values[3],
        tension: 0.1,
      },
    ],
  },
});
