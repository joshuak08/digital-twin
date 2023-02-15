var sim_data = JSON.parse(document.getElementById('all_SimData').textContent);
console.log(sim_data)

export const drawText = (canvas, boxNum) => {
    canvas.font = "48px serif";
    canvas.fillText(`Scada: ${boxNum}`, 10, 50);
};

// probably should handle the sql stuff ajax and what not
// once data is retrieved convert it to array from, unsure on how to sync pipe and tanks but can worry about that later