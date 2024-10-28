import json
import socket
from threading import Thread


class Server:
    def __init__(self):
        self.port = 5000
        self.host = "127.0.0.1"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.players_data = {}

    def start(self):
        self.get_socket_ready()
        self.handle_connection()

    def get_socket_ready(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        print("服务器已准备接收客户端连接")

    def handle_connection(self):
        while True:
            conn, addr = self.sock.accept()
            print(f"接收到来自{addr}的连接")
            conn.send(str(id(conn)).encode("utf-8"))
            Thread(target=self.handle_message, args=(conn, )).start()

    def handle_message(self, conn):
        while True:
            try:
                data = conn.recv(2048)
                if not data:
                    print("未接收到数据，关闭连接")
                    self.players_data.pop(str(id(conn)))
                    conn.close()
                    break
                else:
                    data = json.loads(data.decode("utf-8"))
                    self.update_one_player_data(data)
                    conn.sendall(json.dumps(self.get_other_players_data(data["id"])).encode("utf-8"))
            except Exception as e:
                print(repr(e))
                break

    def update_one_player_data(self, data):
        key = data["id"]
        pos = data["pos"]
        color = data["color"]
        self.players_data[key] = {"pos": pos, "color": color}

    def get_other_players_data(self, current_player_id):
        data = {}
        for key, value in self.players_data.items():
            if key != current_player_id:
                data[key] = value
        return data


if __name__ == '__main__':
    server = Server()
    server.start()


