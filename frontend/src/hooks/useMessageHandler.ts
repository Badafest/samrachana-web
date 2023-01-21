import { parseNumpyArray } from "../controller/plot.controller";
import { changeAppData } from "../slices/app.slice";
import { addPlotData } from "../slices/structure.slice";
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
    }
    if (["plot-seg", "plot-sup", "plot-lod"].includes(func)) {
      const points = parseNumpyArray(data);
      return dispatch(addPlotData({ name: param.name, data: points }));
    }
  }
  return socketMessageHandler;
}
