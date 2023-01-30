import dotenv from "dotenv";

dotenv.config();
import path from "node:path";

const ENV = {
  PYTHON: process.env.PYTHON
    ? path.join(process.cwd(), process.env.PYTHON)
    : "py",
  SCRIPT: path.join(process.cwd(), "./src/python/app.py"),
  PORT: parseInt(process.env.PORT || "8000"),
};

export default ENV;
