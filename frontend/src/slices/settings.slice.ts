import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface ISettingsState {
  data: {
    theme: "platinum" | "user";
    material: string;
    section: string;
    units: [number, number, number];
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
    anim_grid_color: string;
    anim_grid_opacity: number;
    anim_grid_dots: boolean;
    vec_grid_color: string;
    vec_grid_opacity: number;
    vec_grid_dots: boolean;
    afd_plot_color: string;
    sfd_plot_color: string;
    bmd_plot_color: string;
    rfd_plot_color: string;
    add_plot_color: string;
    sdd_plot_color: string;
    slp_plot_color: string;
    rdd_plot_color: string;
    [key: string]: any;
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
        units: [1, 1, 1],
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
        vec_grid_color: "#000000",
        vec_grid_opacity: 0.5,
        vec_grid_dots: false,
        afd_plot_color: "#c521bb",
        sfd_plot_color: "#229959",
        bmd_plot_color: "#d53459",
        rfd_plot_color: "#23321f",
        add_plot_color: "#c521bb",
        sdd_plot_color: "#229959",
        slp_plot_color: "#d53459",
        rdd_plot_color: "#23321f",
        anim_grid_color: "#000000",
        anim_grid_opacity: 0.5,
        anim_grid_dots: false,
      },
};

export const settingsSlice = createSlice({
  name: "settings",
  initialState,
  reducers: {
    changeSetting: (
      state,
      {
        payload,
      }: PayloadAction<
        Record<string, string | number | boolean | [number, number, number]>
      >
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
