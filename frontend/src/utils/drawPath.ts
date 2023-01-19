import { getPixels } from "../components/Elements/Graph/functions";

export default function drawPath(
  context: CanvasRenderingContext2D,
  coords: [number, number][],
  origin: [number, number],
  zoom: number,
  color: string,
  width: number
) {
  const pixels = coords.map((x) =>
    getPixels(context, x[0], x[1], origin[0], origin[1], zoom)
  );
  context.strokeStyle = color;
  context.lineWidth = width;
  context.lineCap = "round";
  context.beginPath();
  context.moveTo(pixels[0][0], pixels[0][1]);
  for (let i = 1; i < coords.length; i++) {
    context.lineTo(pixels[i][0], pixels[i][1]);
  }
  context.stroke();
  context.closePath();
}
