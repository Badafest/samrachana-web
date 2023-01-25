import { FormEventHandler, useRef } from "react";
import { getVectorDiagramData } from "../../controller/diagram.controller";
import { changeAppData } from "../../slices/app.slice";

import { useAppDispatch, useAppSelector } from "../../store";

export default function VectorDiagramForm() {
  const { options, data } = useAppSelector(
    (state) => state.structure.data.analysis
  );
  const { segments } = useAppSelector((state) => state.structure.members);

  const { socket_id } = useAppSelector((state) => state.app.data);

  const { precision } = useAppSelector((state) => state.settings.data);

  const formRef = useRef<HTMLFormElement>(null);

  const dispatch = useAppDispatch();

  const handleFormSubmit: FormEventHandler = async (event) => {
    event.preventDefault();
    if (formRef.current) {
      const formData = new FormData(formRef.current);
      const plots = formData.getAll("plot") as (
        | "_force_comp.x"
        | "_force_comp.y"
        | "_force_comp"
        | "_moment"
        | "_slope"
        | "_delta_comp.x"
        | "_delta_comp.y"
        | "_delta_comp"
      )[];
      try {
        await getVectorDiagramData(
          socket_id,
          segments,
          data,
          1,
          precision,
          plots,
          options.type
        );
        dispatch(changeAppData({ layout: "3H" }));
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
        <label>Action Diagrams</label>
        <div className="flex gap-1 bg-primary rounded p-2 text-secondary">
          <input
            type="checkbox"
            name="plot"
            id="axialForce"
            value="_force_comp.x"
            className="cursor-pointer"
            defaultChecked={true}
          />
          <label htmlFor="axialForce" className="cursor-pointer">
            Axial Force
          </label>
        </div>
        <div className="flex gap-1 bg-primary rounded p-2 text-secondary">
          <input
            type="checkbox"
            name="plot"
            id="shearForce"
            value="_force_comp.y"
            className="cursor-pointer"
            defaultChecked={true}
          />
          <label htmlFor="shearForce" className="cursor-pointer">
            Shear Force
          </label>
        </div>
        <div className="flex gap-1 bg-primary rounded p-2 text-secondary">
          <input
            type="checkbox"
            name="plot"
            id="force"
            value="_force_comp"
            className="cursor-pointer"
            defaultChecked={true}
          />
          <label htmlFor="force" className="cursor-pointer">
            Resultant Force
          </label>
        </div>
        <div className="flex gap-1 bg-primary rounded p-2 text-secondary">
          <input
            type="checkbox"
            name="plot"
            id="moment"
            value="_moment"
            className="cursor-pointer"
            defaultChecked={true}
          />
          <label htmlFor="moment" className="cursor-pointer">
            Bending Moment
          </label>
        </div>

        <div className="h-[1px] w-full bg-primary_dark" />
        <label>Response Diagrams</label>
        <div className="flex gap-1 bg-primary rounded p-2 text-secondary">
          <input
            type="checkbox"
            name="plot"
            id="axialDisplacement"
            value="_delta_comp.x"
            className="cursor-pointer"
            defaultChecked={true}
          />
          <label htmlFor="axialDisplacement" className="cursor-pointer">
            Axial Displacement
          </label>
        </div>
        <div className="flex gap-1 bg-primary rounded p-2 text-secondary">
          <input
            type="checkbox"
            name="plot"
            id="shearDisplacement"
            value="_delta_comp.y"
            className="cursor-pointer"
            defaultChecked={true}
          />
          <label htmlFor="shearDisplacement" className="cursor-pointer">
            Shear Displacement
          </label>
        </div>
        <div className="flex gap-1 bg-primary rounded p-2 text-secondary">
          <input
            type="checkbox"
            name="plot"
            id="disps"
            value="_delta_comp"
            className="cursor-pointer"
            defaultChecked={true}
          />
          <label htmlFor="disps" className="cursor-pointer">
            Resultant Displacement
          </label>
        </div>
        <div className="flex gap-1 bg-primary rounded p-2 text-secondary">
          <input
            type="checkbox"
            name="plot"
            id="slope"
            value="_slope"
            className="cursor-pointer"
            defaultChecked={true}
          />
          <label htmlFor="slope" className="cursor-pointer">
            Slope
          </label>
        </div>
        <div className="h-[1px] w-full bg-primary_dark" />
        <button className="bg-secondary text-primary_light rounded px-2 py-1 border hover-border-contrast1">
          Calculate Diagrams
        </button>
      </form>
    </div>
  );
}
