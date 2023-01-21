import axios from "axios";
import { ILoad, ISegment, ISupport } from "../slices/structure.slice";

const api_url = import.meta.env.VITE_API_URL;

export const parseNumpyArray = (data: string) => {
  const parse =
    "[" +
    data
      .replaceAll(/\]\[/g, "], [")
      .replaceAll(/([0-9])\.([^0-9])/g, "$1 $2")
      .replaceAll(/([0-9]) +([-0-9])/g, "$1, $2")
      .replaceAll(" ", "") +
    "]";
  return JSON.parse(parse);
};

export async function getSegmentPlotData(segment: ISegment, user_id?: string) {
  const { data } = await axios.post(api_url, {
    user_id,
    func: "plot-seg",
    param: {
      name: segment.name,
      type: segment.type,
      P1: segment.P1,
      P3: segment.P3,
      P2: segment.P2,
      scale: 1,
      no: 400,
    },
  });
  return parseNumpyArray(data.data);
}

export async function getSupportPlotData(support: ISupport, user_id?: string) {
  const { data } = await axios.post(api_url, {
    user_id,
    func: "plot-sup",
    param: {
      name: support.name,
      type: support.type,
      location: support.location,
      normal: support.normal,
      scale: 0.5,
    },
  });
  return parseNumpyArray(data.data);
}

export async function getLoadPlotData(load: ILoad, user_id?: string) {
  const { data } = await axios.post(api_url, {
    user_id,
    func: "plot-lod",
    param: {
      name: load.name,
      degree: load.degree,
      peak: load.peak,
      normal: load.normal,
      A: load.parentSegment.P1,
      B: load.parentSegment.P3,
      C: load.parentSegment.P2,
      X: load.P1,
      Y: load.P3,
      type: load.parentSegment.type,
      scale: 0.5,
      log_plot: 1,
    },
  });
  return parseNumpyArray(data.data);
}
