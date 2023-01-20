import axios from "axios";
import { ISegment } from "../slices/structure.slice";

const api_url = import.meta.env.VITE_API_URL;

export async function getSegmentPlotData(segment: ISegment, user_id?: string) {
  try {
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
        no: 200,
      },
    });
    const parse =
      "[" +
      data.data
        .replaceAll(/\]\[/g, "], [")
        .replaceAll(/([0-9])\.([^0-9])/g, "$1 $2")
        .replaceAll(/([0-9]) +([-0-9])/g, "$1, $2")
        .replaceAll(" ", "") +
      "]";
    return JSON.parse(parse);
  } catch (error) {
    console.log(error);
  }
}
