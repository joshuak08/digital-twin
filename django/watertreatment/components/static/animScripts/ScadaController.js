export const drawText = (canvas, boxNum) => {
    canvas.font = "48px serif";
    canvas.fillText(`Scada: ${boxNum}`, 10, 50);
};