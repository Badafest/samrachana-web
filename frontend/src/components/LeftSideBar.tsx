import { changeAppData } from "../slices/app.slice";
import { useAppDispatch, useAppSelector } from "../store";
import Icon from "./Elements/Icon";

export default function LeftSideBar() {
  return (
    <div className="min-w-max px-2 bg-primary_dark flex flex-col gap-1 p-1">
      <SetViewIcon choose="1" icon="1" />
      <SetViewIcon choose="2H" icon="2H" />
      <SetViewIcon choose="2V" icon="2V" />
      <SetViewIcon choose="3H" icon="3H" />
      <SetViewIcon choose="3V" icon="3V" />
      <SetViewIcon choose="4" icon="4" />
    </div>
  );
}

function SetViewIcon({
  choose,
  icon,
}: {
  choose: "1" | "2H" | "2V" | "3H" | "3V" | "4";
  icon: string;
}) {
  const dispatch = useAppDispatch();
  const { layout } = useAppSelector((state) => state.app.data);
  return (
    <Icon
      className={`bg-primary_light border ${
        layout === choose ? "border-secondary" : ""
      }`}
      onClick={() => dispatch(changeAppData({ layout: choose }))}
    >
      {icon}
    </Icon>
  );
}
