import { useAppSelector } from "../../store";
import Graph from "../Elements/Graph";

export default function SimGraph() {
  const { sim_grid_color, sim_grid_dots, sim_grid_opacity } = useAppSelector(
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
      color={sim_grid_color}
      dots={sim_grid_dots}
      opacity={sim_grid_opacity}
      updateFunction={updateFunction}
    />
  );
}
