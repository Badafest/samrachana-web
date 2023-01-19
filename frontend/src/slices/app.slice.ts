import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface IAppState {
  data: {
    active_tool: string;
    status: string;
    layout: "1" | "2H" | "2V" | "3H" | "3V" | "4";
    tool_coords: [number, number][];
  };
}

const initialState: IAppState = {
  data: {
    active_tool: "none",
    status: "everything good :)",
    layout: "1",
    tool_coords: [],
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
