export default function getBoundingPoints(data: [number, number][]) {
  const X = data.map((p) => p[0]);
  const Y = data.map((p) => p[1]);
  const topLeft = [0.99 * Math.min(...X), 1.01 * Math.max(...Y)];
  const bottomRight = [1.01 * Math.max(...X), 0.99 * Math.min(...Y)];
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
