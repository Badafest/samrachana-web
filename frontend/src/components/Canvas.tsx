import { forwardRef, MouseEventHandler } from "react";

export interface ICanvasProps {
  width: number;
  height: number;
  onMouseDown?: MouseEventHandler;
  onMouseMove?: MouseEventHandler;
  onMouseUp?: MouseEventHandler;
  onWheel?: MouseEventHandler;
  style?: object;
  className?: string;
}

export default forwardRef<HTMLCanvasElement, ICanvasProps>((props, ref) => (
  <canvas ref={ref} {...props} />
));
