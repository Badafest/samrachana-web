import { changeAppData } from "../slices/app.slice";
import { addPlotData } from "../slices/structure.slice";
import { useAppDispatch } from "../store";

export default function useMessageHandler() {
  const dispatch = useAppDispatch();

  async function socketMessageHandler(event: MessageEvent) {
    const { func, param, data } = JSON.parse(event.data);
    if (func === "id") {
      dispatch(changeAppData({ socket_id: data }));
      dispatch(changeAppData({ status: "socket connected successfully" }));
    }
    if (func === "plot-seg") {
      const parse =
        "[" +
        data
          .replaceAll(/\]\[/g, "], [")
          .replaceAll(/([0-9])\.([^0-9])/g, "$1 $2")
          .replaceAll(/([0-9]) +([-0-9])/g, "$1, $2")
          .replaceAll(" ", "") +
        "]";
      const points = JSON.parse(parse);
      dispatch(addPlotData({ name: param.name, data: points }));
    }
  }
  return socketMessageHandler;
}
