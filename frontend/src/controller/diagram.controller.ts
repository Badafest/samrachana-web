import axios from "axios";
import { IAnalysisData, ISegment } from "../slices/structure.slice";

const api_url = import.meta.env.VITE_API_URL;

export async function getVectorDiagramData(
  user_id: string,
  segments: ISegment[],
  analysisData: IAnalysisData,
  maxPlot: number,
  precision: number,
  plots: (
    | "_force_comp.x"
    | "_force_comp.y"
    | "_force_comp"
    | "_moment"
    | "_slope"
    | "_delta_comp.x"
    | "_delta_comp.y"
    | "_delta_comp"
  )[],
  structure: "frame" | "truss",
  component?: string
) {
  const { data } = await axios.post(api_url, {
    user_id,
    func: "vec-diag",
    param: {
      segments,
      data: analysisData,
      maxPlot,
      precision,
      component: component || "None",
      plots,
      structure,
    },
  });
  return data;
}
