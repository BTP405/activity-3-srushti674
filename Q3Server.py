import socket
import threading
import pickle
import signal
import sys

class ChatClient:
    def __init__(self):
        self.host = 'localhost'
        self.port = 3000
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.lock = threading.Lock()
        self.running = True

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        print("Server listening on port")

        accept_thread = threading.Thread(target=self.accept_clients, daemon=True)
        accept_thread.start()

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def accept_clients(self):
        while self.running:
            client_socket, client_address = self.server_socket.accept()
            print("New connection:", client_address)
            self.clients.append(client_socket)

            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True)
            client_thread.start()

    def handle_client(self, client_socket):
        while self.running:
            try:
                data = client_socket.recv(4096)
                if not data:
                    break

                # Unpickle received data
                message = pickle.loads(data)
                print("Message received:", message)

                self.broadcast(message, client_socket)
            except Exception as error:
                print("Error:", error)
                break

        with self.lock:
            self.clients.remove(client_socket)
            client_socket.close()

    def broadcast(self, message, sender_socket):
        with self.lock:
            for client_socket in self.clients:
                if client_socket != sender_socket:
                    try:
                        # Pickle the message before sending
                        data = pickle.dumps(message)
                        client_socket.sendall(data)
                    except Exception as e:
                        print("Error broadcasting message:", e)

    def signal_handler(self, sig, frame):
        print("Server closed")
        self.running = False
        self.server_socket.close()
        sys.exit(0)

if __name__ == "__main__":
    chat_server = ChatClient()
    chat_server.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
