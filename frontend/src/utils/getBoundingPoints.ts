export default function getBoundingPoints(data: [number, number][]) {
  const X = data.map((p) => p[0]);
  const Y = data.map((p) => p[1]);
  const topLeft = [Math.min(...X), Math.max(...Y)];
  const bottomRight = [Math.max(...X), Math.min(...Y)];
  return [topLeft, bottomRight] as [number, number][];
}

export function isPointBounded(
  topLeft: [number, number],
  bottomRight: [number, number],
  point: [number, number]
) {
  return (
    point[0] >= topLeft[0] &&
    point[0] <= bottomRight[0] &&
    point[1] >= bottomRight[1] &&
    point[1] <= topLeft[1]
  );
}
