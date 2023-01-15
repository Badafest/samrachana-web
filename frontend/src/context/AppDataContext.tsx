import { createContext, PropsWithChildren, useEffect, useState } from "react";

export interface IAppData {
  grid_color: string;
  grid_opacity: number;
  grid_dots: boolean;
}

export type TAppDataProps = "grid_color" | "grid_opacity" | "grid_dots";

export const defaultAppData: IAppData = {
  grid_color: "gray",
  grid_opacity: 0.8,
  grid_dots: false,
};

export interface IAppDataContext {
  appData: IAppData;
  updateAppData: (
    property: TAppDataProps,
    value: string | boolean | number
  ) => void;
}

export const AppData = createContext<IAppDataContext>({
  appData: defaultAppData,
  updateAppData: () => {},
});

export default function AppDataProvider({ children }: PropsWithChildren) {
  const [appData, setAppData] = useState<IAppData>(defaultAppData);

  useEffect(() => {
    const localAppData = localStorage.getItem("app_data");
    if (localAppData) {
      const parsedAppData = JSON.parse(localAppData);
      setAppData(parsedAppData);
    }
  }, []);

  function updateAppData(
    property: TAppDataProps,
    value: string | boolean | number
  ) {
    setAppData((prev) => ({ ...prev, ...{ [property]: value } }));
    localStorage.setItem("app_data", JSON.stringify(appData));
  }

  return (
    <AppData.Provider value={{ appData, updateAppData }}>
      {children}
    </AppData.Provider>
  );
}
