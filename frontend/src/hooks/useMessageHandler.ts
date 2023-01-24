import { parseAnalysedData } from "../controller/analyse.controller.";
import { parseNumpyArray } from "../controller/plot.controller";
import { changeAppData } from "../slices/app.slice";
import {
  addPlotData,
  analysisData,
  diagramsData,
  ISegment,
} from "../slices/structure.slice";
import { useAppDispatch } from "../store";

export default function useMessageHandler() {
  const dispatch = useAppDispatch();
  function socketMessageHandler(event: MessageEvent) {
    const { func, param, data } = JSON.parse(event.data);
    if (func === "id") {
      dispatch(changeAppData({ socket_id: data }));
      return dispatch(
        changeAppData({ status: "socket connected successfully" })
      );
    } else if (["plot-seg", "plot-sup", "plot-lod"].includes(func)) {
      const points = parseNumpyArray(data);
      return dispatch(addPlotData({ name: param.name, data: points }));
    } else if (["frame", "truss"].includes(func)) {
      const parsed = parseAnalysedData(data);
      return dispatch(analysisData(JSON.parse(parsed)));
    } else if (func === "vec-diag") {
      const diagramData = JSON.parse(parseAnalysedData(data));
      const segments = param["segments"].map((x: ISegment) => x.name);
      return dispatch(
        diagramsData({
          segments,
          ...diagramData,
        })
      );
    }
  }
  return socketMessageHandler;
}
