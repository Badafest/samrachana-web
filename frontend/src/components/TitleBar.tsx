import { changeAppData, clearToolCoords } from "../slices/app.slice";
import { useAppDispatch, useAppSelector } from "../store";
import Icon from "./Elements/Icon";

import tools from "../data/tools.json";

export default function TitleBar() {
  return (
    <div className="h-[48px] bg-primary text-contrast1">
      <div className="flex justify-center gap-2 p-2">
        {tools.map((tool, index) => (
          <ToolIcon key={index} tool={tool.name} icon={tool.icon_name} />
        ))}
      </div>
    </div>
  );
}

function ToolIcon({ tool, icon }: { tool: string; icon: string }) {
  const { active_tool } = useAppSelector((state) => state.app.data);
  const dispatch = useAppDispatch();
  return (
    <Icon
      className={`bg-primary_light text-secondary cursor-pointer border active-bg-primary_dark ${
        active_tool === tool ? "border-secondary" : "border-primary_dark"
      }`}
      onClick={() => {
        dispatch(clearToolCoords());
        dispatch(changeAppData({ active_tool: tool }));
      }}
    >
      <span className="icon">{icon}</span>
    </Icon>
  );
}
