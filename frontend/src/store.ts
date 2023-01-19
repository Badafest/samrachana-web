import { configureStore } from "@reduxjs/toolkit";
import { TypedUseSelectorHook, useDispatch, useSelector } from "react-redux";

import { appSlice } from "./slices/app.slice";
import { settingsSlice } from "./slices/settings.slice";
import { structureSlice } from "./slices/structure.slice";

const store = configureStore({
  reducer: {
    settings: settingsSlice.reducer,
    app: appSlice.reducer,
    structure: structureSlice.reducer,
  },
});

export default store;

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export const useAppDispatch: () => AppDispatch = useDispatch;
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
