import { FormEventHandler, useRef } from "react";
import {
  getFrameAnalysedData,
  getTrussAnalysedData,
} from "../../controller/analyse.controller.";
import { changeAppData } from "../../slices/app.slice";
import { analysisOptions } from "../../slices/structure.slice";
import { useAppDispatch, useAppSelector } from "../../store";

export default function AnalyseForm() {
  const { options } = useAppSelector((state) => state.structure.data.analysis);
  const { segments, loads, supports } = useAppSelector(
    (state) => state.structure.members
  );
  const { socket_id } = useAppSelector((state) => state.app.data);

  const formRef = useRef<HTMLFormElement>(null);

  const dispatch = useAppDispatch();

  const handleFormSubmit: FormEventHandler = async (event) => {
    event.preventDefault();
    if (formRef.current) {
      const formData = new FormData(formRef.current);

      const newOptions = {
        type: formData.get("analyse_as") as "frame" | "truss",
        inextensible: formData.get("inextensible") === "on",
        simplify: formData.get("simplify") === "on",
        accuracy: parseFloat(
          `${formData.get("accuracy")}` || "0.995"
        ) as number,
      };

      dispatch(analysisOptions(newOptions));
      const elements = [...segments, ...loads, ...supports];
      try {
        newOptions.type === "frame"
          ? await getFrameAnalysedData(
              elements,
              false,
              newOptions.inextensible,
              newOptions.simplify,
              newOptions.accuracy,
              socket_id
            )
          : await getTrussAnalysedData(
              elements,
              newOptions.simplify,
              newOptions.accuracy,
              false,
              false,
              socket_id
            );
        dispatch(changeAppData({ layout: "2V" }));
      } catch (error: any) {
        dispatch(
          changeAppData({
            status: error.message || error,
          })
        );
      }
    }
  };

  return (
    <div className="bg-primary_light text-contrast1 rounded p-2">
      <form
        ref={formRef}
        onSubmit={handleFormSubmit}
        className="flex flex-col gap-1 text-sm"
      >
        <label>Structure</label>
        <div className="flex gap-1 bg-primary rounded p-2 text-secondary">
          <input
            type="radio"
            name="analyse_as"
            id="frame"
            value="frame"
            className="cursor-pointer"
            defaultChecked={options.type === "frame"}
          />
          <label htmlFor="frame" className="cursor-pointer">
            Frame
          </label>
        </div>
        <div className="flex gap-1 bg-primary rounded p-2 text-secondary">
          <input
            type="radio"
            name="analyse_as"
            id="truss"
            value="truss"
            className="cursor-pointer"
            defaultChecked={options.type === "truss"}
          />
          <label htmlFor="truss" className="cursor-pointer">
            Truss
          </label>
        </div>
        <div className="h-[1px] w-full bg-primary_dark" />
        <div className="flex gap-1 bg-primary rounded p-2 text-secondary">
          <input
            type="checkbox"
            name="inextensible"
            id="inextensible"
            className="cursor-pointer"
            defaultChecked={options.inextensible}
          />
          <label htmlFor="inextensible" className="cursor-pointer">
            Inextensible
          </label>
        </div>
        <div className="h-[1px] w-full bg-primary_dark" />
        <div className="flex gap-1 bg-primary rounded p-2 text-secondary">
          <input
            type="checkbox"
            name="simplify"
            id="simplify"
            className="cursor-pointer"
            defaultChecked={options.simplify}
          />
          <label htmlFor="simplify" className="cursor-pointer">
            Simplify
          </label>
        </div>
        <label htmlFor="accuracy" className="cursor-pointer">
          Accuracy
        </label>
        <input
          type="number"
          name="accuracy"
          id="accuracy"
          min="0.9"
          max="0.999"
          step="0.001"
          defaultValue={options.accuracy}
          className="bg-primary rounded py-2 px-4 text-secondary outline-none border focus-border-secondary"
        />
        <div className="h-[1px] w-full bg-primary_dark" />
        <button className="bg-secondary text-primary_light rounded px-2 py-1 border hover-border-contrast1">
          Analyse Structure
        </button>
      </form>
    </div>
  );
}
