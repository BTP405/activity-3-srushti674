import socket
import pickle

def send_file(file_path, server_host, server_port):
    try:
        with open(file_path, 'rb') as f:
            file_data = f.read()

        file_object = {'filename': file_path, 'data': file_data}

        pickled_file = pickle.dumps(file_object)

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_host, server_port))
        client_socket.sendall(pickled_file)
        print("File sent successfully.")

    finally:
        client_socket.close()

def run_client():
    file_path = 'Q1sent.txt'
    server_host = "localhost"
    server_port = 3000

    send_file(file_path, server_host, server_port)

if __name__ == "__main__":
    run_client()