import { useDispatch } from "react-redux";
import { updateToolCoords } from "../../slices/app.slice";
import { useAppSelector } from "../../store";
import Graph from "../Elements/Graph";

export default function MainGraph() {
  const { main_grid_color, main_grid_dots, main_grid_opacity } = useAppSelector(
    (state) => state.settings.data
  );
  const dispatch = useDispatch();

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

  const onToolMouseDown = (
    context: CanvasRenderingContext2D | null,
    zoom: number,
    origin: [number, number],
    prevCoords: [number, number][],
    tempCoords: [number, number]
  ) => {
    dispatch(updateToolCoords(tempCoords));
  };

  return (
    <Graph
      color={main_grid_color}
      dots={main_grid_dots}
      opacity={main_grid_opacity}
      updateFunction={updateFunction}
      onToolMouseDown={onToolMouseDown}
    />
  );
}
