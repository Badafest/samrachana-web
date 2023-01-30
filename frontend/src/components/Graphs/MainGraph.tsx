import { useDispatch } from "react-redux";
import { changeAppData, updateToolCoords } from "../../slices/app.slice";
import { useAppSelector } from "../../store";
import drawPath, { drawText } from "../../utils/drawing";
import getBoundingPoints, {
  isPointBounded,
} from "../../utils/getBoundingPoints";
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
  const { active_tool, selected } = useAppSelector((state) => state.app.data);
  const { segments, loads, supports } = useAppSelector(
    (state) => state.structure.members
  );

  const { tool_coords } = useAppSelector((state) => state.app.data);

  const { nodes } = useAppSelector((state) => state.structure.data.analysis);

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
      nodes.length &&
        nodes.forEach((node, index) => {
          drawText(
            context,
            `${index}`,
            node,
            origin,
            zoom,
            support_plot_color,
            12
          );
        });
    }
  };

  const onToolMouseDown = (
    context: CanvasRenderingContext2D | null,
    zoom: number,
    origin: [number, number],
    active: boolean,
    prevCoords: [number, number][],
    tempCoords: [number, number]
  ) => {
    if (active_tool === "select") {
      const newSelected = Object.keys(plot).find((key) => {
        const boundingPoints = getBoundingPoints(plot[key]);
        return (
          key !== selected &&
          isPointBounded(boundingPoints[0], boundingPoints[1], tempCoords)
        );
      });
      dispatch(changeAppData({ selected: newSelected || "" }));
    } else if (!["analyse", "vector"].includes(active_tool)) {
      dispatch(updateToolCoords(tempCoords));
    }
  };

  const onToolMouseMove = (
    context: CanvasRenderingContext2D | null,
    zoom: number,
    origin: [number, number],
    active: boolean,
    prevCoords: [number, number][],
    tempCoords: [number, number]
  ) => {
    if (context) {
      updateFunction(context, zoom, origin);
      if (!["select", "none"].includes(active_tool)) {
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
