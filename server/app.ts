import express from "express";
import { Request, Response } from "express";
import Controller from "./src/Controller";
import cors from "cors";

const app = express();

app.use(cors());

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.post("/api", Controller);

app.use("*", (_: Request, res: Response) => {
  res.status(404).json({
    error: "Not Found",
  });
});

export default app;
