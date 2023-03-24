import webSocket from "ws";
import http from "http";
import app from "./app";
import ENV from "./src/vars";
import socketService from "./src/socket.service";

const server = http.createServer(app);

const wss = new webSocket.Server({ server });
wss.on("connection", async function (ws: WebSocket, request: any) {
  const user_id = await socketService.getUniqueId();
  try {
    await socketService.insertClient(user_id, ws);
    console.log("socket connected => ", user_id);
    ws.send(JSON.stringify({ func: "id", data: user_id }));
  } catch (error) {
    console.log(error);
    console.log("socket not connected => ", user_id);
    return;
  }
  wss.on("message", (message) => {});
  wss.on("close", () => {});
});

server.listen(ENV.PORT, async () => {
  console.log("server listening on port => ", ENV.PORT);
  console.log("Open Samrachana in browser => http://localhost:8000");
});
