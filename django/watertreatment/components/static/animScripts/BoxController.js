export const drawText = (canvas, boxNum) => {
    canvas.font = "48px serif";
    canvas.fillText(`Hello from box ${boxNum}`, 10, 50);
};