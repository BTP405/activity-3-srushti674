import socket
import pickle
from Q2Task import *

def execute_task(task_data):
    task, args = pickle.loads(task_data)
    return task(*args)

def main():
    host = ''
    port = 3000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print("Worker is listening the port", port)
        while True:
            conn, addr = s.accept()
            with conn:
                print('Received a task from Client', addr)
                task_data = conn.recv(1024)
                result = execute_task(task_data)
                conn.sendall(pickle.dumps(result))

if __name__ == "__main__":
    main()