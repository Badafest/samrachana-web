import { useAppDispatch, useAppSelector } from "../store";
import { changeSetting } from "../slices/settings.slice";

import materials from "../data/materials.json";
import sections from "../data/sections.json";
import userUnits from "../data/units.json";

export default function StatusBar() {
  const { status, socket_id } = useAppSelector((state) => state.app.data);

  const { segments, loads, supports } = useAppSelector(
    (state) => state.structure.members
  );
  return (
    <div className="h-[24px] px-2 flex justify-between items-center text-contrast1 text-sm bg-primary">
      <span className="text-xs italic">{socket_id}</span>
      <span>{status}</span>
      <div className="flex gap-2 items-center">
        <span>
          {segments.length} segments | {loads.length} loads | {supports.length}{" "}
          supports
        </span>
        <MaterialSelect />
        <SectionSelect />
        <UnitsSelect />
        <PrecisionSelect />
      </div>
    </div>
  );
}

function MaterialSelect() {
  const { material } = useAppSelector((state) => state.settings.data);
  const dispatch = useAppDispatch();
  return (
    <select
      value={material}
      onChange={(e) => dispatch(changeSetting({ material: e.target.value }))}
      className="bg-primary_light outline-none cursor-pointer  border-contrast1"
    >
      {materials.map((item, index) => (
        <option key={index} value={item.name}>
          {item.name}
        </option>
      ))}
    </select>
  );
}

function SectionSelect() {
  const { section } = useAppSelector((state) => state.settings.data);
  const dispatch = useAppDispatch();
  return (
    <select
      value={section}
      onChange={(e) => dispatch(changeSetting({ section: e.target.value }))}
      className="bg-primary_light outline-none cursor-pointer  border-contrast1"
    >
      {sections.map((item, index) => (
        <option key={index} value={item.name}>
          {item.name}
        </option>
      ))}
    </select>
  );
}

function UnitsSelect() {
  const { units } = useAppSelector((state) => state.settings.data);
  const dispatch = useAppDispatch();
  const forces = userUnits.filter((item) => item.Quantity === "Force");
  const lengths = userUnits.filter((item) => item.Quantity === "Length");
  return (
    <>
      <select
        value={units[0]}
        onChange={(e) =>
          dispatch(
            changeSetting({
              units: [parseFloat(e.target.value), units[1], units[2]],
            })
          )
        }
        className="bg-primary_light outline-none cursor-pointer  border-contrast1"
      >
        {forces.map((item, index) => (
          <option key={index} value={item.Conversion}>
            {item.Symbol}
          </option>
        ))}
      </select>
      <select
        value={units[1]}
        onChange={(e) =>
          dispatch(
            changeSetting({
              units: [units[0], parseFloat(e.target.value), units[2]],
            })
          )
        }
        className="bg-primary_light outline-none cursor-pointer  border-contrast1"
      >
        {lengths.map((item, index) => (
          <option key={index} value={item.Conversion}>
            {item.Symbol}
          </option>
        ))}
      </select>
      <select
        value={units[2]}
        onChange={(e) =>
          dispatch(
            changeSetting({
              units: [units[0], units[1], parseFloat(e.target.value)],
            })
          )
        }
        className="bg-primary_light outline-none cursor-pointer  border-contrast1"
      >
        <option value={1}>C</option>
        <option value={0.55555555555}>F</option>
      </select>
    </>
  );
}

function PrecisionSelect() {
  const { precision } = useAppSelector((state) => state.settings.data);
  const dispatch = useAppDispatch();

  return (
    <select
      value={precision}
      onChange={(e) =>
        dispatch(
          changeSetting({
            precision: parseInt(e.target.value),
          })
        )
      }
      className="bg-primary_light outline-none cursor-pointer  border-contrast1"
    >
      <option value={0}>0</option>
      <option value={1}>1</option>
      <option value={2}>2</option>
      <option value={3}>3</option>
      <option value={4}>4</option>
      <option value={5}>5</option>
      <option value={6}>6</option>
      <option value={7}>7</option>
      <option value={8}>8</option>
      <option value={9}>9</option>
      <option value={10}>10</option>
    </select>
  );
}
