import { useState } from "react";
import FrameAnalysisTable from "../tables/FrameAnalysisTable";
import ViewTopBar from "../Elements/ViewTopBar";
import { useAppSelector } from "../../store";
import TrussAnalysisTable from "../tables/TrussAnalysisTable";

export default function TableView() {
  const [current, setCurrent] = useState<"reactions" | "action" | "response">(
    "reactions"
  );
  const { options } = useAppSelector((state) => state.structure.data.analysis);
  return (
    <>
      <ViewTopBar>
        <div className="flex rounded-lg bg-primary text-secondary  gap-2 border border-secondary">
          <span
            className={`cursor-pointer px-4 py-2 ${
              current === "reactions" ? "bg-secondary text-primary" : ""
            }`}
            onClick={() => setCurrent("reactions")}
          >
            Reactions
          </span>
          <span
            className={`cursor-pointer px-4 py-2 ${
              current === "action" ? "bg-secondary text-primary" : ""
            }`}
            onClick={() => {
              setCurrent("action");
            }}
          >
            Actions
          </span>
          <span
            className={`cursor-pointer px-4 py-2 ${
              current === "response" ? "bg-secondary text-primary" : ""
            }`}
            onClick={() => setCurrent("response")}
          >
            Responses
          </span>
        </div>
      </ViewTopBar>
      {options.type === "frame" ? (
        <FrameAnalysisTable current={current} />
      ) : (
        <TrussAnalysisTable current={current} />
      )}
    </>
  );
}
