import { useAppSelector } from "../../store";
import Graph from "../Elements/Graph";

export default function LineGraph() {
  const { line_grid_color, line_grid_dots, line_grid_opacity } = useAppSelector(
    (state) => state.settings.data
  );

  const { segments, loads, supports } = useAppSelector(
    (state) => state.structure.members
  );

  const updateFunction = (
    context: CanvasRenderingContext2D | null,
    zoom: number,
    origin: [number, number]
  ) => {
    context?.clearRect(0, 0, context?.canvas.width, context?.canvas.height);
  };

  return (
    <Graph
      color={line_grid_color}
      dots={line_grid_dots}
      opacity={line_grid_opacity}
      updateFunction={updateFunction}
    />
  );
}
