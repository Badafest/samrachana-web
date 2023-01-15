import { MouseEventHandler, useState, WheelEventHandler } from "react";
import drawLine from "../../utils/drawLine";
import { getCoordinates, getPixels } from "./functions";

export default function useEvents(context: CanvasRenderingContext2D | null) {
  const [active, setActive] = useState(false);

  const [prevCoords, setPrevCoords] = useState<number[][]>([]);
  const [origin, setOrigin] = useState([0, 0]);
  const [zoom, setZoom] = useState(100);

  const handleMouseDown: MouseEventHandler = (event) => {
    setActive(true);
    const newCoordinates = getCoordinates(
      event.clientX,
      event.clientY,
      origin[0],
      origin[1],
      zoom
    );
    const lastCoordinates = prevCoords.at(-1);
    if (lastCoordinates && context) {
      const [initialX, initialY] = getPixels(
        context,
        lastCoordinates[0],
        lastCoordinates[1],
        origin[0],
        origin[1],
        zoom
      );
      const [finalX, finalY] = getPixels(
        context,
        newCoordinates[0],
        newCoordinates[1],
        origin[0],
        origin[1],
        zoom
      );
      drawLine(context, initialX, initialY, finalX, finalY, "", 2);
    }
    setPrevCoords((prev) => [...prev.slice(-2), newCoordinates]);
  };

  const handleMouseUp: MouseEventHandler = (event) => {
    setActive(false);
  };

  const handleMouseMove: MouseEventHandler = (event) => {
    const lastCoords = prevCoords.at(-1);
    const tempCoords = getCoordinates(
      event.clientX,
      event.clientY,
      origin[0],
      origin[1],
      zoom
    );
    if (active) {
      setOrigin((prev) => {
        if (lastCoords) {
          return [
            prev[0] - tempCoords[0] + lastCoords[0],
            prev[1] + tempCoords[1] - lastCoords[1],
          ];
        } else {
          return prev;
        }
      });
    }
  };

  const handleWheel: WheelEventHandler = (event) => {
    setZoom((prev) => {
      const newZoom = prev - event.deltaY / 100;
      return newZoom <= 1.001 ? 1.001 : newZoom >= 1000 ? 1000 : newZoom;
    });
  };

  return {
    origin,
    zoom,
    handleMouseDown,
    handleMouseMove,
    handleMouseUp,
    handleWheel,
  };
}
