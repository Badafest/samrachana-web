import { ChangeEventHandler } from "react";
import { changeSetting } from "../../slices/settings.slice";
import { useAppDispatch, useAppSelector } from "../../store";
import Icon from "../Elements/Icon";
import SimGraph from "../Graphs/SimGraph";
import ViewTopBar from "../Elements/ViewTopBar";

export default function SimView() {
  return (
    <>
      <ViewTopBar>
        <SimGridColor />
        <SimGridOpacityRange />
        <SimGridDotsIcon />
      </ViewTopBar>
      <SimGraph />
    </>
  );
}

function SimGridDotsIcon() {
  const { sim_grid_dots } = useAppSelector((state) => state.settings.data);
  const dispatch = useAppDispatch();

  return (
    <Icon
      className="bg-primary text-secondary w-8 px-1"
      onClick={() => dispatch(changeSetting({ sim_grid_dots: !sim_grid_dots }))}
    >
      {sim_grid_dots ? "▦" : "⋮⋮⋮"}
    </Icon>
  );
}

function SimGridOpacityRange() {
  const { sim_grid_opacity } = useAppSelector((state) => state.settings.data);
  const dispatch = useAppDispatch();

  const handleRangeChange: ChangeEventHandler<HTMLInputElement> = (event) => {
    const value = parseFloat(event.target.value);
    if (value >= 0 && value <= 1) {
      dispatch(changeSetting({ sim_grid_opacity: value }));
    }
  };

  return (
    <input
      type="number"
      min="0"
      max="1"
      step="0.1"
      className="text-xs bg-primary text-secondary w-min py-1 px-2 rounded outsim-none border focus-border-secondary"
      onChange={handleRangeChange}
      value={sim_grid_opacity}
    />
  );
}

function SimGridColor() {
  const { sim_grid_color } = useAppSelector((state) => state.settings.data);
  const dispatch = useAppDispatch();

  const handleColorChange: ChangeEventHandler<HTMLInputElement> = (event) => {
    dispatch(changeSetting({ sim_grid_color: `${event.target.value}` }));
  };

  return (
    <input
      type="color"
      className="cursor-pointer bg-primary text-secondary py-1  px-2 rounded outsim-none border focus-border-secondary w-8"
      onChange={handleColorChange}
      value={sim_grid_color}
    />
  );
}
