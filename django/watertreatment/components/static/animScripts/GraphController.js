const ctx1 = document.getElementById('chart1').getContext('2d');
const ctx2 = document.getElementById('chart2').getContext('2d');
const json_list_simdata = JSON.parse(JSON.parse(document.getElementById('all_SimData').textContent));
const data_array = Object.entries(json_list_simdata).map((fields) => combine_id_fields(fields)).map((fields) => fields[1]['fields']);

function combine_id_fields(json) {
  json[1]['fields']['pk'] = json[1]['pk'];
  return json;
}

// Generate string of snapshot labels inline
const labels = Array.from(Array(((data_array).length/4)), (_, index) => 'Snapshot ' + (index + 1))
// Filter JSON for unique key and get all related values

const pks = {
  'water_vol': {},
  'particulate': {},
};
data_array.forEach(function(entry) {
  if (!pks['water_vol'][entry.pk]) {
    pks['water_vol'][entry.pk] = {};
    pks['particulate'][entry.pk] = {};
  }; // if the pk is not already in the dict, initialse it
  pks['water_vol'][entry.pk][entry.snap_num] = entry.water_vol;
  pks['particulate'][entry.pk][entry.snap_num] = entry.particulate;
});

// Convert JSON to array by iterating and extracting values from object
// [0 : [ water_vol, ... ], ...]
const tank_values = [];
const particulate_values = [];
// (IMPORTANT) Tank IDs are: 9, 10, 11, 12
for (let i = 9; i < 13; i++) {
  tank_values.push(Object.values(pks['water_vol'][i]));
  particulate_values.push(Object.values(pks['particulate'][i]));
}

// Create 4 lines charts for each tank
try {
  const json_sim_data = Object.entries(JSON.parse(JSON.parse(document.getElementById('all_SimData').textContent)));
  json_sim_data.filter((fields) => fields[1]['pk'] === (9) && fields[1]['fields']['snap_num'] === 1)[0][1]['fields']['particulate'];
  new Chart(ctx1, {
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
    options: {
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'water volume (m ³)',
            font: {size: 15},
          },
        },
        x: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Snapshot (5 seconds)',
            font: {size: 15},
          },
        },
      },
      responsive: true,
      showTooltips: true,
      plugins: {
        tooltips: {
          mode: 'index',
          intersect: false,
        },
        hover: {
          mode: 'nearest',
          intersect: true,
        },
      },
    },
  });
  new Chart(ctx2, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Tank 1 Particulate Levels',
          borderColor: 'rgb(75, 192, 192)', // green
          data: particulate_values[0],
          tension: 0.1, // curving of line
        },
        {
          label: 'Tank 2 Particulate Levels',
          borderColor: 'rgb(255, 99, 132)', // red
          data: particulate_values[1],
          tension: 0.1,
        },
        {
          label: 'Tank 3 Particulate Levels',
          borderColor: 'rgb(255, 205, 86)', // yellow
          data: particulate_values[2],
          tension: 0.1,
        },
        {
          label: 'Tank 4 Particulate Levels',
          borderColor: 'rgb(153, 102, 255)', // purple
          data: particulate_values[3],
          tension: 0.1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'particulate (mg)',
          },
        },
        x: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Snapshot (5 seconds)',
          },
        },
      },
    },
  });
} catch (err) {
  ctx1.font = '30px Arial';
  ctx1.fillStyle = 'red';
  ctx1.fillText('Please create a simulation in the inputs tab.', 300, 300);
}


