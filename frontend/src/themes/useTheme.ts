import { useEffect, useState } from "react";
import { useAppSelector } from "../store";
import themes from "./themes.json";

export function useTheme() {
  const { theme } = useAppSelector((state) => state.settings.data);
  const [userTheme, setUserTheme] = useState<object>({});

  useEffect(() => {
    if (theme && theme !== "user") {
      setUserTheme(themes[theme]);
    } else {
      const localTheme = localStorage.getItem("user_theme");
      setUserTheme((_) =>
        localTheme ? JSON.parse(localTheme) : themes.platinum
      );
    }
  }, [theme]);
  return userTheme;
}
