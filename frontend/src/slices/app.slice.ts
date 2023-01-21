import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface IAppState {
  data: {
    socket_id: string;
    active_tool: string;
    status: string;
    layout: "1" | "2H" | "2V" | "3H" | "3V" | "4";
    tool_coords: [number, number][];
    selected: string;
  };
}

const initialState: IAppState = {
  data: {
    socket_id: "",
    active_tool: "select",
    status: "everything good :)",
    layout: "1",
    tool_coords: [],
    selected: "",
  },
};

export const appSlice = createSlice({
  name: "app",
  initialState,
  reducers: {
    changeAppData: (
      state,
      { payload }: PayloadAction<Record<string, string | number | boolean>>
    ) => {
      state.data = { ...state.data, ...payload };
    },
    updateToolCoords: (state, { payload }: PayloadAction<[number, number]>) => {
      if (state.data.tool_coords.length < 3) {
        state.data.tool_coords = [...state.data.tool_coords, payload];
      } else {
        state.data.tool_coords = [];
      }
    },
    clearToolCoords: (state) => {
      state.data.tool_coords = [];
    },
  },
});

export const { changeAppData, updateToolCoords, clearToolCoords } =
  appSlice.actions;
