import { ChangeEventHandler } from "react";
import { changeSetting } from "../../slices/settings.slice";
import { useAppDispatch, useAppSelector } from "../../store";
import Icon from "../Elements/Icon";
import MainGraph from "../Graphs/MainGraph";
import ViewTopBar from "../Elements/ViewTopBar";

export default function MainView() {
  return (
    <>
      <MainGraph />
      <ViewTopBar>
        <MainGridColor />
        <MainGridOpacityRange />
        <MainGridDotsIcon />
      </ViewTopBar>
    </>
  );
}

function MainGridDotsIcon() {
  const { main_grid_dots } = useAppSelector((state) => state.settings.data);
  const dispatch = useAppDispatch();

  return (
    <Icon
      className="bg-primary text-secondary px-1"
      onClick={() =>
        dispatch(changeSetting({ main_grid_dots: !main_grid_dots }))
      }
    >
      {main_grid_dots ? "▦" : "⋮⋮⋮"}
    </Icon>
  );
}

function MainGridOpacityRange() {
  const { main_grid_opacity } = useAppSelector((state) => state.settings.data);
  const dispatch = useAppDispatch();

  const handleRangeChange: ChangeEventHandler<HTMLInputElement> = (event) => {
    const value = parseFloat(event.target.value);
    if (value >= 0 && value <= 1) {
      dispatch(changeSetting({ main_grid_opacity: value }));
    }
  };

  return (
    <input
      type="number"
      min="0"
      max="1"
      step="0.1"
      className="text-xs bg-primary text-secondary w-min px-2 py-1 rounded outline-none border focus-border-secondary"
      onChange={handleRangeChange}
      value={main_grid_opacity}
    />
  );
}

function MainGridColor() {
  const { main_grid_color } = useAppSelector((state) => state.settings.data);
  const dispatch = useAppDispatch();

  const handleColorChange: ChangeEventHandler<HTMLInputElement> = (event) => {
    dispatch(changeSetting({ main_grid_color: `${event.target.value}` }));
  };

  return (
    <input
      type="color"
      className="cursor-pointer bg-primary text-secondary py-1  px-2 rounded outline-none border focus-border-secondary w-8"
      onChange={handleColorChange}
      value={main_grid_color}
    />
  );
}
