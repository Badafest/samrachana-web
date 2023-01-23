import { useState } from "react";
import AnalysisTable from "../AnalysisTable";
import ViewTopBar from "../Elements/ViewTopBar";

export default function TableView() {
  const [current, setCurrent] = useState<"reactions" | "action" | "response">(
    "reactions"
  );
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
      <AnalysisTable current={current} />
    </>
  );
}
