import { useAppSelector } from "../../store";
import Graph from "../Elements/Graph";

export default function AnimGraph() {
  const { anim_grid_color, anim_grid_dots, anim_grid_opacity } = useAppSelector(
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
      color={anim_grid_color}
      dots={anim_grid_dots}
      opacity={anim_grid_opacity}
      updateFunction={updateFunction}
    />
  );
}
