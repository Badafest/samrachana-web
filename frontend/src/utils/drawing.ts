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

export function drawText(
  context: CanvasRenderingContext2D,
  text: string,
  coords: [number, number],
  origin: [number, number],
  zoom: number,
  color: string,
  width: number
) {
  const pixels = getPixels(
    context,
    coords[0],
    coords[1],
    origin[0],
    origin[1],
    zoom
  );
  context.font = width + "px OpenSans";
  context.fillStyle = color;
  context.textAlign = "center";
  context.beginPath();
  const length = (text.length / 2 + 1) * width;
  const height = (4 * width) / 3;
  context.rect(pixels[0] - length / 2, pixels[1] - height / 2, length, height);
  context.fill();
  context.fillStyle = color;
  context.fillStyle = "white";
  context.fillText(text, pixels[0], pixels[1] + width / 3, text.length * width);
  context.closePath();
}
