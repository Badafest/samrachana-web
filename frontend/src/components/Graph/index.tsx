import { useContext, useEffect, useRef, useState } from "react";
import Canvas from "../Canvas";
import { getGridBkg, getGridScale } from "./functions";
import { AppData } from "../../context/AppDataContext";
import useEvents from "./hook";
import drawLine from "../../utils/drawLine";

function Graph({
  name,
  width,
  height,
}: {
  name: string;
  width: number;
  height: number;
}) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [context, setContext] = useState<CanvasRenderingContext2D | null>(null);

  const { appData } = useContext(AppData);

  const {
    zoom,
    origin,
    handleMouseDown,
    handleMouseMove,
    handleMouseUp,
    handleWheel,
  } = useEvents(context);

  useEffect(() => {
    canvasRef.current && setContext(canvasRef.current?.getContext("2d"));
  }, []);

  useEffect(() => {
    // if (context) {
    //   context.clearRect(0, 0, 1000, 1000);
    //   drawLine(context, 0, 0, 20, 20, "blue", 2);
    // }
  }, [context]);

  return (
    <Canvas
      ref={canvasRef}
      width={width}
      height={height}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onWheel={handleWheel}
      style={{
        backgroundImage: getGridBkg(
          appData.grid_color,
          40 / getGridScale(zoom),
          appData.grid_opacity,
          appData.grid_dots
        ),
        backgroundSize: getGridScale(zoom),
        backgroundPosition: `left ${-origin[0] * zoom}px bottom ${
          origin[1] * zoom
        }px`,
      }}
    />
  );
}

export default Graph;
