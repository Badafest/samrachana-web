import axios from "axios";
import { ILoad, ISegment, ISupport } from "../slices/structure.slice";

const api_url = import.meta.env.VITE_API_URL;

export const parseAnalysedData = (data: string) =>
  data
    .replaceAll(/array|[()]|dtype=object|dtype=int64/g, "")
    .replaceAll("None", '"None"')
    .replaceAll("'", '"')
    .replaceAll(/\]\[/g, "], [")
    .replaceAll(/([0-9])\.([^0-9])/g, "$1 $2")
    .replaceAll(/([0-9]) +([-0-9])/g, "$1, $2")
    .replaceAll(" ", "")
    .replaceAll(",,", ",")
    .replaceAll(",,", ",")
    .replaceAll(",}", "}");

export async function getFrameAnalysedData(
  elements: (ISegment | ISupport | ILoad)[],
  shear: boolean = false,
  inextensible: boolean,
  simplify: boolean,
  accuracy: number,
  user_id?: string
) {
  const { data } = await axios.post(api_url, {
    user_id,
    func: "frame",
    param: {
      elements,
      shear,
      inextensible,
      simplify,
      accuracy,
    },
  });
  const formatted = data.data;
  return formatted;
}

export async function getTrussAnalysedData(
  elements: (ISegment | ISupport | ILoad)[],
  simplify: boolean,
  accuracy: number,
  shear: boolean = false,
  inextensible: boolean = false,
  user_id?: string
) {
  const { data } = await axios.post(api_url, {
    user_id,
    func: "truss",
    param: {
      elements,
      simplify,
      shear,
      inextensible,
      accuracy,
    },
  });
  const formatted = data.data;
  return formatted;
}
