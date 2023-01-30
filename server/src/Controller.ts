import { Request, Response } from "express";
import { spawn } from "node:child_process";
import socketService from "./socket.service";
import ENV from "./vars";

async function Controller(req: Request, res: Response) {
  const { user_id, func, param } = req.body;

  try {
    const ls = ENV.SCRIPT
      ? spawn(ENV.PYTHON, [ENV.SCRIPT, func, JSON.stringify(param)])
      : spawn(ENV.PYTHON, [func, JSON.stringify(param)]);

    const sendData = async (data: any) => {
      ls.stdout.removeAllListeners();
      ls.stderr.removeAllListeners();
      const client = await socketService.getClient(user_id);
      if (client && client.socket) {
        client.socket.send(
          JSON.stringify({
            func,
            param,
            data: data.toString().replaceAll("\r\n", ", "),
          })
        );
      }
      return res.status(200).json({
        message: "Script run successfully",
        call: { func, param },
        data: data.toString().replaceAll("\r\n", ", "),
      });
    };

    const sendError = (data: any) => {
      ls.stderr.removeAllListeners();
      ls.stderr.removeAllListeners();
      console.log(data.toString());
      return res.status(400).json({
        message: "Script run with error",
        call: { func, param },
        error: data.toString().split("\r\n").at(-2),
      });
    };

    ls.stdout.addListener("data", sendData);
    ls.stderr.addListener("data", sendError);

    ls.on("close", (code) => {
      console.log("script closed with code => ", code);
    });
  } catch (error) {
    console.log(error);
    return res.status(500).json({
      message: "Something went wrong",
      error: error instanceof Error ? error.message : error,
    });
  }
}

export default Controller;
