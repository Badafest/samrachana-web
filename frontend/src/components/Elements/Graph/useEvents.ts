import { MouseEventHandler, useState, WheelEventHandler } from "react";
import { useAppSelector } from "../../../store";
import {
  getCoordinates,
  getGridScale,
  getNoDigits,
  getRounded,
} from "./functions";

export default function useEvents(
  context: CanvasRenderingContext2D | null,
  onToolMouseMove?: (
    context: CanvasRenderingContext2D,
    zoom: number,
    origin: [number, number],
    prevCoords: [number, number][],
    tempCoords: [number, number]
  ) => void,

  onToolMouseDown?: (
    context: CanvasRenderingContext2D,
    zoom: number,
    origin: [number, number],
    prevCoords: [number, number][],
    tempCoords: [number, number]
  ) => void
) {
  const [active, setActive] = useState(false);

  const [prevCoords, setPrevCoords] = useState<[number, number][]>([]);
  const [tempCoords, setTempCoords] = useState<[number, number]>([0, 0]);
  const [origin, setOrigin] = useState<[number, number]>([0, 0]);
  const [zoom, setZoom] = useState(100);

  const { active_tool } = useAppSelector((state) => state.app.data);

  const { precision } = useAppSelector((state) => state.settings.data);

  const handleMouseDown: MouseEventHandler = (event) => {
    setActive(true);
    if (context) {
      const [x, y] = getCoordinates(
        context,
        event.clientX,
        event.clientY,
        origin[0],
        origin[1],
        zoom
      );
      setPrevCoords((prev) => [
        ...prev.slice(-2),
        [getRounded(x, precision), getRounded(y, precision)],
      ]);
      if (active_tool !== "select" && onToolMouseDown) {
        onToolMouseDown(context, zoom, origin, prevCoords, tempCoords);
      }
    }
  };

  const handleMouseUp: MouseEventHandler = (event) => {
    setActive(false);
  };

  const updateOrigin: (
    prev: [number, number],
    tempCoords: [number, number],
    lastCoords?: [number, number]
  ) => [number, number] = (
    prev: [number, number],
    tempCoords: [number, number],
    lastCoords?: [number, number]
  ) => {
    if (lastCoords) {
      return [
        prev[0] - tempCoords[0] + lastCoords[0],
        prev[1] + tempCoords[1] - lastCoords[1],
      ];
    } else {
      return prev;
    }
  };

  const handleMouseMove: MouseEventHandler = (event) => {
    if (context) {
      const lastCoords = prevCoords.at(-1);
      const [x, y] = getCoordinates(
        context,
        event.clientX,
        event.clientY,
        origin[0],
        origin[1],
        zoom
      );
      const toRound = event.ctrlKey
        ? Math.min(2, getNoDigits(getGridScale(zoom) * 0.1))
        : precision;
      setTempCoords((_) => [getRounded(x, toRound), getRounded(y, toRound)]);
      if (active) {
        setOrigin((prev) => updateOrigin(prev, [x, y], lastCoords));
      }
      if (active_tool !== "select" && onToolMouseMove) {
        onToolMouseMove(context, zoom, origin, prevCoords, tempCoords);
      }
    }
  };

  const handleWheel: WheelEventHandler = (event) => {
    if (context) {
      const lastCoords = getCoordinates(
        context,
        event.clientX,
        event.clientY,
        origin[0],
        origin[1],
        zoom
      );
      setZoom((prev) => {
        const newZoom = event.deltaY > 0 ? prev * 0.8 : prev * 1.2;
        const finalZoom =
          newZoom <= 10 ? 10 : newZoom >= 1000 ? 1000 : Math.round(newZoom);
        const tempCoords: [number, number] = [
          lastCoords[0] * (1 - finalZoom),
          lastCoords[1] * (1 - finalZoom),
        ];
        // setOrigin((prev) => updateOrigin(prev, tempCoords, lastCoords));
        return finalZoom;
      });
    }
  };

  return {
    origin,
    zoom,
    handleMouseDown,
    handleMouseMove,
    handleMouseUp,
    handleWheel,
    tempCoords,
  };
}
