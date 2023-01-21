import SegmentForm from "./forms/SegmentForm";
import { useAppSelector } from "../store";
import tools from "../data/tools.json";
import SupportForm from "./forms/SupportForm";
import LoadForm from "./forms/LoadForm";
import EditDeleteForm from "./forms/EditDeleteForm";

export default function RightSideBar() {
  const { active_tool } = useAppSelector((state) => state.app.data);
  return (
    <div className="flex-grow-0 w-[192px] p-2 bg-primary_dark flex flex-col gap-1 text-sm text-secondary_dark">
      <span>{tools.find((tool) => tool.name === active_tool)?.hint}</span>
      <ToolForm active_tool={active_tool} />
    </div>
  );
}

function ToolForm({ active_tool }: { active_tool: string }) {
  if (["line", "arc", "quad"].indexOf(active_tool) !== -1) {
    return <SegmentForm />;
  } else if (
    ["fixed", "hinge", "roller", "internal_hinge", "node", "custom"].indexOf(
      active_tool
    ) !== -1
  ) {
    return <SupportForm />;
  } else if (
    [
      "moment",
      "point",
      "linear",
      "uniform",
      "quadratic",
      "cubic",
      "misfit",
      "temperature",
    ].indexOf(active_tool) !== -1
  ) {
    return <LoadForm />;
  } else if (active_tool === "select") {
    return <EditDeleteForm />;
  }
  {
    return <></>;
  }
}
