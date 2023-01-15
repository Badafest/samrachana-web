export default function drawLine(
  context: CanvasRenderingContext2D,
  x1: number,
  y1: number,
  x2: number,
  y2: number,
  color: string,
  width: number
) {
  context.strokeStyle = color;
  context.lineWidth = width;
  context.lineCap = "round";
  context.moveTo(x1, y1);
  context.lineTo(x2, y2);
  context.stroke();
}
