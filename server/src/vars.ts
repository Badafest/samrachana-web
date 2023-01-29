import dotenv from "dotenv";

dotenv.config();

const ENV = {
  CWD: process.cwd(),
  PYTHON: process.env.PYTHON || "py",
  PORT: parseInt(process.env.PORT || "8000"),
};

export default ENV;
