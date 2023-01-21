import { useDispatch } from "react-redux";
import { updateToolCoords } from "../../slices/app.slice";
import { useAppSelector } from "../../store";
import drawPath from "../../utils/drawPath";
import Graph from "../Elements/Graph";

export default function MainGraph() {
  const {
    main_grid_color,
    main_grid_dots,
    main_grid_opacity,
    seg_plot_color,
    seg_plot_width,
    support_plot_color,
    support_plot_width,
    temp_plot_color,
    temp_plot_width,
    load_plot_color,
    load_plot_width,
  } = useAppSelector((state) => state.settings.data);
  const dispatch = useDispatch();

  const { plot } = useAppSelector((state) => state.structure.data);
  const { active_tool } = useAppSelector((state) => state.app.data);
  const { segments, loads, supports } = useAppSelector(
    (state) => state.structure.members
  );

  const { tool_coords } = useAppSelector((state) => state.app.data);

  const updateFunction = (
    context: CanvasRenderingContext2D | null,
    zoom: number,
    origin: [number, number]
  ) => {
    if (context) {
      context?.clearRect(0, 0, context?.canvas.width, context?.canvas.height);
      segments.forEach((segment) => {
        const data = plot[segment.name];
        data &&
          drawPath(context, data, origin, zoom, seg_plot_color, seg_plot_width);
      });
      loads.forEach((load) => {
        const data = plot[load.name];
        data &&
          drawPath(
            context,
            data,
            origin,
            zoom,
            load_plot_color,
            load_plot_width
          );
      });
      supports.forEach((support) => {
        const data = plot[support.name];
        data &&
          drawPath(
            context,
            data,
            origin,
            zoom,
            support_plot_color,
            support_plot_width
          );
      });
    }
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

  const onToolMouseMove = (
    context: CanvasRenderingContext2D | null,
    zoom: number,
    origin: [number, number],
    prevCoords: [number, number][],
    tempCoords: [number, number]
  ) => {
    if (context) {
      updateFunction(context, zoom, origin);
      tool_coords.length &&
        tool_coords.length < 3 &&
        drawPath(
          context,
          [...tool_coords, tempCoords, tool_coords[0]],
          origin,
          zoom,
          temp_plot_color,
          temp_plot_width
        );
    }
  };

  return (
    <Graph
      color={main_grid_color}
      dots={main_grid_dots}
      opacity={main_grid_opacity}
      updateFunction={updateFunction}
      updateDependency={[active_tool, Object.values(plot)]}
      onToolMouseDown={onToolMouseDown}
      onToolMouseMove={onToolMouseMove}
    />
  );
}
