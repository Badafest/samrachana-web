import { Request, Response } from "express";
import { spawn } from "node:child_process";
import ENV from "./vars";

async function Controller(req: Request, res: Response) {
  const { func, param } = req.body;
  const ls = spawn(ENV.PYTHON, [
    ENV.CWD + "/src/python/app.py",
    func,
    JSON.stringify(param),
  ]);

  ls.stdout.on("data", (data) => {
    console.log(data);
    res.status(200).json({
      message: "Script run successfully",
      call: { func, param },
      data: data.toString(),
    });
  });

  ls.stderr.on("data", (data) => {
    console.error(`stderr: ${data}`);
    res.status(500).json({
      message: "Script failed to run",
      call: { func, param },
      error: data.toString(),
    });
  });

  ls.on("close", (code) => {
    console.log("script closed with code => ", code);
  });
}

export default Controller;
