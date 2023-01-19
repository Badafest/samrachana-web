export const getCoordinates: (
  context: CanvasRenderingContext2D,
  pixelX: number,
  pixelY: number,
  originX: number,
  originY: number,
  zoom: number
) => [number, number] = (
  context: CanvasRenderingContext2D,
  pixelX: number,
  pixelY: number,
  originX: number = 0,
  originY: number = 0,
  zoom: number = 50
) => {
  const { x, y } = context.canvas.getBoundingClientRect();
  const coordX = originX + (pixelX - Math.round(x)) / zoom;
  const maxY = context.canvas.height / zoom;
  const coordY = maxY - originY - (pixelY - Math.round(y)) / zoom;
  return [coordX, coordY];
};

export const getPixels: (
  context: CanvasRenderingContext2D,
  coordX: number,
  coordY: number,
  originX: number,
  originY: number,
  zoom: number
) => [number, number] = (
  context: CanvasRenderingContext2D,
  coordX: number,
  coordY: number,
  originX: number = 0,
  originY: number = 0,
  zoom: number = 50
) => {
  const { x, y } = context.canvas.getBoundingClientRect();
  const pixelX = zoom * (coordX - originX) + Math.round(x);
  const maxY = context.canvas.height / zoom;
  const pixelY = zoom * (maxY - originY - coordY) + Math.round(y);

  return [parseInt(`${pixelX}`), parseInt(`${pixelY}`)];
};

export const getGridBkg = (
  color: string,
  width: number,
  opacity: number = 0.8,
  dots: boolean = true
) => {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" height="100" width="100" viewBox="0 0 100 100" style="background: none; stroke-width: ${width}px; stroke: ${color}; opacity: ${opacity}">
<rect x="0" y="0" width="100" height="100" stroke="none" fill="${
    dots ? "url(#gridDots)" : "url(#gridLines)"
  }"/>
${
  dots
    ? `<circle cx="0" cy="0" r="1.5" fill="${color}"/>
      <circle cx="100" cy="0" r="1.5" fill="${color}"/>
      <circle cx="0" cy="100" r="1.5" fill="${color}"/>
      <circle cx="100" cy="100" r="1.5" fill="${color}"/>`
    : '<polyline points="100 0, 0 0, 0 100" fill="none"/>'
}
<defs>
    <pattern id="gridLines" patternUnits="userSpaceOnUse" width="10" height="10">
        <polyline points="10 0, 0 0, 0 10" fill="none"/>
    </pattern>
    <pattern id="gridDots" patternUnits="userSpaceOnUse" width="10" height="10">
      <circle cx="0" cy="0" r="0.5" fill="${color}"/>
      <circle cx="10" cy="0" r="0.5" fill="${color}"/>
      <circle cx="0" cy="10" r="0.5" fill="${color}"/>
      <circle cx="10" cy="10" r="0.5" fill="${color}"/>
    </pattern>
</defs>
</svg>`;
  const encoded = window.btoa(svg);
  return "url(data:image/svg+xml;base64," + encoded + ")";
};

export const getGridScale = (zoom: number) => {
  if (zoom > 500) {
    return 0.1;
  } else if (zoom > 50) {
    return 1;
  } else if (zoom > 5) {
    return 10;
  } else {
    return 100;
  }
};

export const getRounded = (num: number, digits: number) =>
  Math.round(num * 10 ** digits) / 10 ** digits;

export const getNoDigits = (num: number) =>
  num.toString().split(".")[1]?.length || 0;
