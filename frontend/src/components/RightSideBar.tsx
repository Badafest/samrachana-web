import AddSegmentForm from "./forms/AddSegmentForm";
import { useAppSelector } from "../store";
import tools from "../data/tools.json";

export default function RightSideBar() {
  const { active_tool } = useAppSelector((state) => state.app.data);
  return (
    <div className="flex-grow-0 w-[192px] p-2 bg-primary_dark flex flex-col gap-1 text-sm text-secondary_dark">
      <span>{tools.find((tool) => tool.name === active_tool)?.hint}</span>
      <ToolForm active_tool={active_tool} />
    </div>
  );
}

function getToolHint(tool: string) {}

function ToolForm({ active_tool }: { active_tool: string }) {
  if (["line", "arc", "quad"].indexOf(active_tool) !== -1) {
    return <AddSegmentForm />;
  } else {
    return <></>;
  }
}
