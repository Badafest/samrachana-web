import { useEffect, useRef, useState } from "react";
import Canvas from "../Canvas";
import { getGridBkg, getGridScale } from "./functions";
import useEvents from "./useEvents";

interface IGraphProps {
  color: string;
  dots: boolean;
  opacity: number;
  updateFunction?: (
    context: CanvasRenderingContext2D | null,
    zoom: number,
    origin: [number, number]
  ) => void;
  updateDependency?: any[];
  onToolMouseMove?: (
    context: CanvasRenderingContext2D | null,
    zoom: number,
    origin: [number, number],
    prevCoords: [number, number][],
    tempCoords: [number, number]
  ) => void;
  onToolMouseDown?: (
    context: CanvasRenderingContext2D | null,
    zoom: number,
    origin: [number, number],
    prevCoords: [number, number][],
    tempCoords: [number, number]
  ) => void;
}

function Graph({
  color,
  dots,
  opacity,
  updateFunction,
  updateDependency = [],
  onToolMouseMove,
  onToolMouseDown,
}: IGraphProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [context, setContext] = useState<CanvasRenderingContext2D | null>(null);

  const {
    zoom,
    origin,
    handleMouseDown,
    handleMouseMove,
    handleMouseUp,
    handleWheel,
    tempCoords,
  } = useEvents(context, onToolMouseMove, onToolMouseDown);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas) {
      setContext(canvasRef.current?.getContext("2d"));
      const rect = canvas.parentElement?.getBoundingClientRect();
      canvas.height = rect?.height || innerHeight;
      canvas.width = rect?.width || innerWidth;
      canvas.setAttribute("left", `${rect?.left || 0}`);
      canvas.setAttribute("top", `${rect?.top || 0}`);
    }
  }, []);

  useEffect(() => {
    updateFunction && updateFunction(context, zoom, origin);
  }, [zoom, origin, ...updateDependency]);

  return (
    <>
      <div
        className="absolute z-10 right-2  bottom-2 text-sm bg-primary rounded p-1"
        style={{ color }}
      >
        1:{getGridScale(zoom)} | {tempCoords.join(", ")}
      </div>
      <Canvas
        ref={canvasRef}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onWheel={handleWheel}
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          backgroundImage: getGridBkg(
            color,
            40 / (zoom * getGridScale(zoom)),
            opacity,
            dots
          ),
          backgroundSize: zoom * getGridScale(zoom),
          backgroundPosition:
            "left " +
            `${-origin[0] * zoom}px` +
            " bottom " +
            `${origin[1] * zoom}px`,
        }}
      />
    </>
  );
}

export default Graph;
