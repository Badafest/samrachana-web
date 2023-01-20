import { useDispatch } from "react-redux";
import { changeAppData } from "../slices/app.slice";
import shortcuts from "../data/keyboard.json";

type TShortcut = "l" | "a" | "q" | "x";

export default function useKeypressHandler() {
  const dispatch = useDispatch();
  return function keypressHandler(event: any) {
    const target = event.target?.tagname;
    if (target === "INPUT") {
      return;
    }
    dispatch(changeAppData({ active_tool: "select" }));
    if (Object.keys(shortcuts).includes(event.key)) {
      dispatch(
        changeAppData({
          active_tool: shortcuts[event.key as TShortcut],
        })
      );
    }
  };
}
