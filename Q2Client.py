import socket
import pickle
from Q2Task import add, multiply

def send_task(task, *args):
    task_data = pickle.dumps((task, args))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 3000))
        s.sendall(task_data)
        data = s.recv(1024)
    return pickle.loads(data)

if __name__ == "__main__":

    # For Example
    print("Result of addition:", send_task(add, 10, 25))
    print("Result of multiplication:", send_task(multiply, 10, 25))