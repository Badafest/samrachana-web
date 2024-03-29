import { useAppDispatch, useAppSelector } from "../../store";
import { useState, useEffect } from "react";

import {
  addSegment,
  deletePlotData,
  deleteSegment,
  ISegment,
} from "../../slices/structure.slice";
import {
  changeAppData,
  clearToolCoords,
  updateToolCoords,
} from "../../slices/app.slice";

import materials from "../../data/materials.json";
import sections from "../../data/sections.json";
import { getSegmentPlotData } from "../../controller/plot.controller";

export default function SegmentForm({ edit }: { edit?: ISegment }) {
  const { active_tool, tool_coords } = useAppSelector(
    (state) => state.app.data
  );

  const { segments } = useAppSelector((state) => state.structure.members);
  const { material, section, units } = useAppSelector(
    (state) => state.settings.data
  );
  const { socket_id } = useAppSelector((state) => state.app.data);
  const dispatch = useAppDispatch();

  const [segMaterial, setSegMaterial] = useState<string>(material);
  const [segSection, setSegSection] = useState<string>(section);

  const [type, setType] = useState<"line" | "arc" | "quad">(
    edit?.type || (active_tool as "line" | "arc" | "quad")
  );

  const [name, setName] = useState<string>(
    edit?.name || `segment#${segments.length + 1}`
  );

  const [P1, setP1] = useState<[number, number]>(edit?.P1 || [0, 0]);
  const [P2, setP2] = useState<[number, number]>(edit?.P2 || [0, 0]);
  const [P3, setP3] = useState<[number, number]>(edit?.P3 || [0, 0]);

  useEffect(() => {
    if (!edit) {
      dispatch(clearToolCoords());
      setType(active_tool as "line" | "arc" | "quad");
    }
  }, [active_tool]);

  useEffect(() => {
    if (!edit) {
      if (tool_coords.length === 1) {
        setP1(tool_coords[0]);
      } else if (tool_coords.length === 2) {
        setP3(tool_coords[1]);
        if (type === "line") {
          setP2([
            0.5 * (tool_coords[0][0] + tool_coords[1][0]),
            0.5 * (tool_coords[0][1] + tool_coords[1][1]),
          ]);
        }
      } else if (tool_coords.length === 3 && type !== "line") {
        setP2(tool_coords[2]);
      } else {
        setP1([0, 0]);
        setP2([0, 0]);
        setP3([0, 0]);
      }
    }
  }, [tool_coords]);

  useEffect(() => {
    if (!edit) {
      if (tool_coords.length === 2 && type === "line") {
        handleAddSegment();
        const lastClickedPoint = tool_coords.at(-1);
        dispatch(clearToolCoords());
        lastClickedPoint && dispatch(updateToolCoords(lastClickedPoint));
      }
      if (tool_coords.length === 3 && type !== "line") {
        handleAddSegment();
        const lastClickedPoint = tool_coords.at(-2);
        dispatch(clearToolCoords());
        lastClickedPoint && dispatch(updateToolCoords(lastClickedPoint));
      }
    }
  }, [P2]);

  const handleAddSegment = async () => {
    const userMaterial = materials.find((item) => item.name === segMaterial);
    const userSection = sections.find((item) => item.name === segSection);

    const isNameTaken = segments.find((item) => item.name === name);

    const newName = `segment#${segments.length + (isNameTaken ? 1 : 2)}`;
    if (!edit) {
      setName(newName);
    }

    const newSegment: ISegment = {
      name: edit ? name : isNameTaken ? newName : name,
      class: "segment",
      type,
      P1,
      P3,
      P2,
      I: (userSection?.Iyy || edit?.I || 1) / units[1] ** 4,
      area: (userSection?.A || edit?.area || 1) / units[1] ** 2,
      youngsModulus:
        (units[1] ** 2 * (userMaterial?.E || edit?.youngsModulus || 1)) /
        units[0],
      shearModulus:
        (units[1] ** 2 * (userMaterial?.G || edit?.shearModulus || 1)) /
        units[0],
      alpha: units[2] * (userMaterial?.alpha || edit?.alpha || 1),
      density:
        (units[1] ** 3 * (userMaterial?.density || edit?.density || 1)) /
        units[0],
      shapeFactor: userSection?.k || edit?.shapeFactor || 1,
    };

    dispatch(deleteSegment(edit?.name || ""));
    try {
      const length = Math.hypot(P1[0] - P3[0], P1[1] - P3[1]);
      if (length === 0) {
        dispatch(clearToolCoords());
        throw new Error("Segment should have non zero length");
      }
      await getSegmentPlotData(newSegment, socket_id);
      dispatch(addSegment(newSegment));
      dispatch(changeAppData({ status: `${name} added to structure!` }));
      if (edit?.name !== name) {
        dispatch(deletePlotData(edit?.name || ""));
      }
    } catch (error: any) {
      edit && dispatch(addSegment(edit));
      dispatch(
        changeAppData({
          status: error.message || error,
        })
      );
    }
  };

  const handleFormSubmit = (event: any) => {
    event.preventDefault();
    handleAddSegment();
  };

  const handleDelete = (event: any) => {
    event.preventDefault();
    dispatch(deleteSegment(edit?.name || ""));
    dispatch(deleteSegment(edit?.name || ""));
  };

  return (
    <div className="bg-primary_light text-contrast1 rounded p-2">
      <form onSubmit={handleFormSubmit} className="flex flex-col gap-1 text-sm">
        <label htmlFor="type">Type</label>
        <select
          name="type"
          id="type"
          className="bg-primary cursor-pointer rounded px-2 py-1  text-secondary outline-none border focus-border-secondary"
          value={type}
          onChange={(e) => setType(e.target.value as "line" | "arc" | "quad")}
        >
          <option value="line">Linear</option>
          <option value="arc">Circular</option>
          <option value="quad">Parabolic</option>
        </select>
        <div className="h-[1px] w-full bg-primary_dark">ss</div>
        <label htmlFor="name">Name</label>
        <input
          name="name"
          id="name"
          className="bg-primary rounded px-2 py-1  text-secondary outline-none border focus-border-secondary"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <div className="h-[1px] w-full bg-primary_dark" />
        <label>Initial Coordinates</label>
        <div className="flex gap-1">
          <input
            name="P1x"
            id="P1x"
            type="number"
            placeholder="X"
            className="bg-primary rounded py-1 px-2 text-secondary outline-none border focus-border-secondary"
            value={P1[0]}
            onChange={(e) => {
              setP1((prev) => [parseFloat(e.target.value), prev[1]]);
            }}
          />
          <input
            name="P1y"
            id="P1y"
            type="number"
            placeholder="Y"
            className="bg-primary rounded py-1 px-2 text-secondary outline-none border focus-border-secondary"
            value={P1[1]}
            onChange={(e) => {
              setP1((prev) => [prev[0], parseFloat(e.target.value)]);
            }}
          />
        </div>
        <label>Final Coordinates</label>
        <div className="flex gap-1">
          <input
            name="P3x"
            id="P3x"
            type="number"
            placeholder="X"
            className="bg-primary rounded py-1 px-2 text-secondary outline-none border focus-border-secondary"
            value={P3[0]}
            onChange={(e) => {
              setP3((prev) => [parseFloat(e.target.value), prev[1]]);
            }}
          />
          <input
            name="P3y"
            id="P3y"
            type="number"
            placeholder="Y"
            className="bg-primary rounded py-1 px-2 text-secondary outline-none border focus-border-secondary"
            value={P3[1]}
            onChange={(e) => {
              setP3((prev) => [prev[0], parseFloat(e.target.value)]);
            }}
          />
        </div>

        <label>Mid Coordinates</label>
        <div className="flex gap-1">
          <input
            name="P2x"
            id="P2x"
            type="number"
            placeholder="X"
            className="bg-primary rounded py-1 px-2 text-secondary outline-none border focus-border-secondary"
            value={P2[0]}
            onChange={(e) => {
              setP2((prev) => [parseFloat(e.target.value), prev[1]]);
            }}
          />
          <input
            name="P2y"
            id="P2y"
            type="number"
            placeholder="Y"
            className="bg-primary rounded py-1 px-2 text-secondary outline-none border focus-border-secondary"
            value={P2[1]}
            onChange={(e) => {
              setP2((prev) => [prev[0], parseFloat(e.target.value)]);
            }}
          />
        </div>
        <div className="h-[1px] w-full bg-primary_dark" />
        <label htmlFor="material">Material</label>
        <select
          name="material"
          id="material"
          className="bg-primary cursor-pointer rounded px-2 py-1  text-secondary outline-none border focus-border-secondary"
          value={segMaterial}
          onChange={(e) => setSegMaterial(e.target.value)}
        >
          {materials.map((material, index) => (
            <option key={index} value={material.name}>
              {material.name}
            </option>
          ))}
        </select>

        <label htmlFor="section">Section</label>
        <select
          name="section"
          id="section"
          className="bg-primary cursor-pointer rounded px-2 py-1  text-secondary outline-none border focus-border-secondary"
          value={segSection}
          onChange={(e) => setSegSection(e.target.value)}
        >
          {sections.map((section, index) => (
            <option key={index} value={section.name}>
              {section.name}
            </option>
          ))}
        </select>

        <div className="h-[1px] w-full bg-primary_dark" />
        <button className="bg-secondary text-primary_light rounded px-2 py-1 border hover-border-contrast1">
          {edit ? "Edit" : "Add"} Segment
        </button>
        {edit && (
          <>
            <div className="h-[1px] w-full bg-primary_dark" />
            <button
              className="bg-secondary text-primary_light rounded px-2 py-1 border hover-border-contrast1"
              onClick={handleDelete}
            >
              Delete Segment
            </button>
          </>
        )}
      </form>
    </div>
  );
}
