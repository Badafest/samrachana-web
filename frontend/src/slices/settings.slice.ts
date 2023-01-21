import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface ISettingsState {
  data: {
    theme: "platinum" | "user";
    material: string;
    section: string;
    units: string;
    precision: 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;
    main_grid_color: string;
    main_grid_opacity: number;
    main_grid_dots: boolean;
    temp_plot_color: string;
    temp_plot_width: number;
    seg_plot_color: string;
    seg_plot_width: number;
    load_plot_color: string;
    load_plot_width: number;
    support_plot_color: string;
    support_plot_width: number;
    line_grid_color: string;
    line_grid_opacity: number;
    line_grid_dots: boolean;
    sim_grid_color: string;
    sim_grid_opacity: number;
    sim_grid_dots: boolean;
  };
}

const userSettings = localStorage.getItem("settings");
const initialState: ISettingsState = {
  data: userSettings
    ? JSON.parse(userSettings)
    : {
        theme: "user",
        material: "Default",
        section: "DEFAULT",
        units: "N m C",
        precision: 3,
        main_grid_color: "#000000",
        main_grid_opacity: 0.5,
        main_grid_dots: false,
        temp_plot_color: "#222222",
        temp_plot_width: 0.5,
        seg_plot_color: "#2643ff",
        seg_plot_width: 3,
        load_plot_color: "#d53459",
        load_plot_width: 2,
        support_plot_color: "#417c45",
        support_plot_width: 2,
        line_grid_color: "#000000",
        line_grid_opacity: 0.5,
        line_grid_dots: false,
        sim_grid_color: "#000000",
        sim_grid_opacity: 0.5,
        sim_grid_dots: false,
      },
};

export const settingsSlice = createSlice({
  name: "settings",
  initialState,
  reducers: {
    changeSetting: (
      state,
      { payload }: PayloadAction<Record<string, string | number | boolean>>
    ) => {
      state.data = { ...state.data, ...payload };
      localStorage.setItem("settings", JSON.stringify(state.data));
    },

    saveSetting: (state) => {
      localStorage.setItem("settings", JSON.stringify(state.data));
    },
  },
});

export const { changeSetting, saveSetting } = settingsSlice.actions;
