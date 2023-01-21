export function snapToSegment(
  P1: [number, number],
  P3: [number, number],
  point: [number, number]
) {
  const xv = [P3[0] - P1[0], P3[1] - P1[1]];
  const len = Math.hypot(...xv);
  const fv = [point[0] - P1[0], point[1] - P1[1]];
  const dot = (xv[0] * fv[0] + xv[1] * fv[1]) / len;
  return [P1[0] + (dot * xv[0]) / len, P1[1] + (dot * xv[1]) / len] as [
    number,
    number
  ];
}

export function snapToPoint(
  targets: [number, number][],
  point: [number, number]
) {
  const dists = targets.map((target) =>
    Math.hypot(target[0] - point[0], target[1] - point[1])
  );
  const minIndex = dists.indexOf(Math.min(...dists));
  return targets[minIndex] as [number, number];
}
