import SegmentForm from "./forms/SegmentForm";
import { useAppSelector } from "../store";
import tools from "../data/tools.json";
import SupportForm from "./forms/SupportForm";
import LoadForm from "./forms/LoadForm";
import EditDeleteForm from "./forms/EditDeleteForm";
import AnalyseForm from "./forms/AnalyseForm";
import VectorDiagramForm from "./forms/VectorDiagramForm";
import shortcuts from "../data/keyboard.json";

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
  } else if (active_tool === "analyse") {
    return <AnalyseForm />;
  } else if (active_tool === "vector") {
    return <VectorDiagramForm />;
  }
  {
    return <ShortcutHint />;
  }
}

function ShortcutHint() {
  return (
    <div className="h-[90vh] overflow-auto flex flex-col gap-2 pr-2">
      {Object.keys(shortcuts).map((key, index) => (
        <div
          key={index}
          className="text-sm flex-shrink-0 bg-primary_light p-2 rounded"
        >
          <div>
            PRESS{" "}
            <span className="bg-primary inline-flex items-center justify-center w-6 h-6 rounded">
              {key.slice(0, 3)}
            </span>{" "}
            TO
          </div>
          <div>
            {tools.find((item) => item.name === (shortcuts as any)[key])
              ?.hint || "See this hint"}
          </div>
        </div>
      ))}
    </div>
  );
}
