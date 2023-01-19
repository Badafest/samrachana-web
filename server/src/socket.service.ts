export interface IClient {
  user_id: string;
  socket: WebSocket;
}

export interface ISocketService {
  insertClient: (user_id: string, ws: WebSocket) => Promise<void>;
  removeClient: (user_id: string) => Promise<IClient[]>;
  getClient: (user_id: string) => Promise<IClient | undefined>;
  getUniqueId: () => Promise<string>;
}

class SocketService implements ISocketService {
  private clients: IClient[] = [];

  async insertClient(user_id: string, ws: WebSocket) {
    const client = await this.getClient(user_id);
    if (client) {
      const newClients = await this.removeClient(user_id);
      this.clients = [...newClients];
    }
    this.clients = [...this.clients, { user_id, socket: ws }];
  }

  async removeClient(user_id: string) {
    return this.clients.filter((client) => client.user_id !== user_id);
  }

  async getClient(user_id: string) {
    const client = this.clients.find((client) => client.user_id === user_id);
    return client;
  }

  async getUniqueId() {
    const clientLength = this.clients.length;
    console.log(this.clients.length);
    return `${Math.round(
      Math.random() * ((clientLength % 7) + 1) * Date.now()
    )}`;
  }
}

const socketService = new SocketService();

export default socketService;
