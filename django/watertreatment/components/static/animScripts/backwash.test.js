import {WaterTank} from './WaterTank.js';
jest.mock('./AnimController.js', () => jest.fn()); // https://stackoverflow.com/questions/61409827/how-to-ignore-import-statements-with-jest-testing/67581836#67581836

let output_data = [];
let test_count = 0;

// helper functions==================================================
function round_precision(number, decimal_precision=10**13) {
  return Math.round(number*decimal_precision)/decimal_precision;
}

function raw_convert_to_json(raw_data) {
  const output = [];

  for (let x = 0; x < raw_data[0].length; x++) {
    const template = ['ignore', {model: 'components.simdatatable', pk: undefined, fields: undefined}];
    template[1]['pk'] = raw_data[0][x];
    template[1]['fields'] = {snap_num: raw_data[1][x], water_vol: raw_data[2][x], particulate: raw_data[3][x], backwash: raw_data[4][x]};
    output.push(template);
  }
  return output;
}

function correct_answer(raw_data) {
  const correct_answer = [];
  for (let x = 0; x < raw_data[0].length; x++) { // iterates max(snapshot) * 4 number of times
    correct_answer.push([raw_data[2][x], raw_data[3][x], raw_data[0][x], raw_data[1][x]]);
  }
  return correct_answer;
}
// ==================================================================

describe('backwash tests', () =>{
  beforeEach(()=>{
    const tanks = [];
    const json_list_simdata = raw_convert_to_json(raw_data[test_count]);
    output_data = [];

    // initialise tanks for testing
    for (let tank_num = 0; tank_num < 4; tank_num++) {
      const starting_progress = round_precision(raw_data[test_count][3][0 + tank_num*raw_data[0][0].length/4] /parseFloat(11340000), 10**3);
      tanks.push(new WaterTank(0, 0, 0, 0, '#000000', undefined, tank_num, undefined, json_list_simdata, starting_progress, true));
    }

    tanks.forEach((tank) => tank.setup_tank(tanks)); // set up tanks
    tanks.forEach((tank) => output_data.push([round_precision(tank.currentLevel*56/163.0, 10**2), tank.progress*11340000, tank.tank_ID, tank.valueIdx-1]));// adds starting values to output_data

    // do fake animation loops and add data to output
    while (!(tanks.reduce((acc, tank) => acc && tank.end, true))) {
      tanks.forEach((tank) => tank.update_progress_rate()); // calculates new progress rate
      tanks.forEach((tank) => tank.calculate_rates());
    }
    tanks.forEach((tank)=> output_data.push(...tank.testoutput)); // combine outputs
    output_data.sort(([a, b, c, d], [e, f, g, h]) => c < g?-1:1); // sort them into correct answer form
  });

  test('no duplicates', () => {
    expect(output_data).toStrictEqual(correct_answer(raw_data[test_count]));
    test_count += 1;
  });

  test('<4 duplicates', () => {
    expect(output_data).toStrictEqual(correct_answer(raw_data[test_count]));
    test_count += 1;
  });

  test('all duplicates in middle', () => {
    expect(output_data).toStrictEqual(correct_answer(raw_data[test_count]));
    test_count += 1;
  });

  test('duplicate values start', () => {
    expect(output_data).toStrictEqual(correct_answer(raw_data[test_count]));
    test_count += 1;
  });

  test('triple duplicate at start', () => {
    expect(output_data).toStrictEqual(correct_answer(raw_data[test_count]));
    test_count += 1;
  });

  test('mixed values, water and particulate', () => {
    expect(output_data).toStrictEqual(correct_answer(raw_data[test_count]));
    test_count += 1;
  });
});
// test sets for specific cases ===================================================
const no_Dupes_no_allDupes = [
  [/* componentID 0*/
    9, 9, 9, 9, 9,
    10, 10, 10, 10, 10,
    11, 11, 11, 11, 11,
    12, 12, 12, 12, 12,
  ],
  [/* snapnum 1*/
    0, 1, 2, 3, 4,
    0, 1, 2, 3, 4,
    0, 1, 2, 3, 4,
    0, 1, 2, 3, 4,
  ],
  [/* # water_vol 2*/
    0, 56, 15, 42, 10,
    0, 56, 15, 42, 10,
    0, 56, 15, 42, 10,
    0, 56, 15, 42, 10,
  ],
  [/* particulate 3*/
    0, 500000, 0, 250000, 0,
    0, 500000, 0, 250000, 0,
    0, 500000, 0, 250000, 0,
    0, 500000, 0, 250000, 0,
  ],
  [/* bool 4*/
    false, true, true, false, false,
    false, true, true, false, false,
    false, true, true, false, false,
    false, true, true, false, false,
  ],
];

const dupes_no_allDupes =[
  [/* componentID 0*/
    9, 9, 9, 9, 9,
    10, 10, 10, 10, 10,
    11, 11, 11, 11, 11,
    12, 12, 12, 12, 12,
  ],
  [/* snapnum 1*/
    0, 1, 2, 3, 4,
    0, 1, 2, 3, 4,
    0, 1, 2, 3, 4,
    0, 1, 2, 3, 4,
  ],
  [/* # water_vol 2*/
    0, 56, 56, 42, 10,
    0, 56, 56, 42, 10,
    0, 56, 15, 42, 10,
    0, 56, 15, 42, 10,
  ],
  [/* particulate 3*/
    0, 500000, 0, 250000, 0,
    0, 500000, 0, 250000, 0,
    0, 500000, 0, 250000, 0,
    0, 500000, 0, 250000, 0,
  ],
  [/* bool 4*/
    false, true, true, false, false,
    false, true, true, false, false,
    false, true, true, false, false,
    false, true, true, false, false,
  ],
];

const allDupes = [
  [/* componentID 0*/
    9, 9, 9, 9, 9,
    10, 10, 10, 10, 10,
    11, 11, 11, 11, 11,
    12, 12, 12, 12, 12,
  ],
  [/* snapnum 1*/
    0, 1, 2, 3, 4,
    0, 1, 2, 3, 4,
    0, 1, 2, 3, 4,
    0, 1, 2, 3, 4,
  ],
  [/* # water_vol 2*/
    0, 56, 56, 42, 10,
    0, 56, 56, 42, 10,
    0, 56, 56, 42, 10,
    0, 56, 56, 42, 10,
  ],
  [/* particulate 3*/
    0, 500000, 0, 250000, 0,
    0, 500000, 0, 250000, 0,
    0, 500000, 0, 250000, 0,
    0, 500000, 0, 250000, 0,
  ],
  [/* bool 4*/
    false, true, true, false, false,
    false, true, true, false, false,
    false, true, true, false, false,
    false, true, true, false, false,
  ],
];

const allDupes_at_start = [
  [/* componentID 0*/
    9, 9, 9, 9, 9,
    10, 10, 10, 10, 10,
    11, 11, 11, 11, 11,
    12, 12, 12, 12, 12,
  ],
  [/* snapnum 1*/
    0, 1, 2, 3, 4,
    0, 1, 2, 3, 4,
    0, 1, 2, 3, 4,
    0, 1, 2, 3, 4,
  ],
  [/* # water_vol 2*/
    56, 56, 25, 42, 10,
    56, 56, 25, 42, 10,
    56, 56, 25, 42, 10,
    56, 56, 25, 42, 10,
  ],
  [/* particulate 3*/
    0, 500000, 0, 250000, 0,
    0, 500000, 0, 250000, 0,
    0, 500000, 0, 250000, 0,
    0, 500000, 0, 250000, 0,
  ],
  [/* bool 4*/
    false, true, true, false, false,
    false, true, true, false, false,
    false, true, true, false, false,
    false, true, true, false, false,
  ],
];

const triple_duplicate_at_start = [
  [/* componentID 0*/
    9, 9, 9, 9, 9,
    10, 10, 10, 10, 10,
    11, 11, 11, 11, 11,
    12, 12, 12, 12, 12,
  ],
  [/* snapnum 1*/
    0, 1, 2, 3, 4,
    0, 1, 2, 3, 4,
    0, 1, 2, 3, 4,
    0, 1, 2, 3, 4,
  ],
  [/* # water_vol 2*/
    56, 56, 56, 42, 10,
    56, 56, 56, 42, 10,
    56, 56, 56, 42, 10,
    56, 56, 56, 42, 10,
  ],
  [/* particulate 3*/
    0, 500000, 0, 250000, 0,
    0, 500000, 0, 250000, 0,
    0, 500000, 0, 250000, 0,
    0, 500000, 0, 250000, 0,
  ],
  [/* bool 4*/
    false, true, true, false, false,
    false, true, true, false, false,
    false, true, true, false, false,
    false, true, true, false, false,
  ],
];

const mixed_values_mixed_particulate = [
  [/* componentID 0*/
    9, 9, 9, 9, 9,
    10, 10, 10, 10, 10,
    11, 11, 11, 11, 11,
    12, 12, 12, 12, 12,
  ],
  [/* snapnum 1*/
    0, 1, 2, 3, 4,
    0, 1, 2, 3, 4,
    0, 1, 2, 3, 4,
    0, 1, 2, 3, 4,
  ],
  [/* # water_vol 2*/
    5, 56, 15, 42, 3,
    3, 42, 12, 32, 5,
    1, 53, 37, 42, 8,
    2, 50, 23, 44, 2,
  ],
  [/* particulate 3*/
    0, 500000, 0, 250000, 0,
    0, 500000, 0, 250000, 0,
    0, 500000, 0, 250000, 0,
    0, 500000, 0, 250000, 0,
  ],
  [/* bool 4*/
    false, true, true, false, false,
    false, true, true, false, false,
    false, true, true, false, false,
    false, true, true, false, false,
  ],
];

const raw_data = [no_Dupes_no_allDupes, dupes_no_allDupes, allDupes, allDupes_at_start, triple_duplicate_at_start, mixed_values_mixed_particulate];
