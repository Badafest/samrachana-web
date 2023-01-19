import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
// import AppDataProvider from "./context/AppDataContext";
import { Provider } from "react-redux";
import store from "./store";

import "./index.css";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </React.StrictMode>
);
