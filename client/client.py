import socket
import threading

HOST = 'localhost'  # The server's hostname or IP address
PORT = 11001        # The port used by the server

def send_messages(s, username):
    while True:
        data = input(f"{username}: ")
        if not data:
            continue
        s.sendall(f"{data}".encode())

def receive_messages(s):
    while True:
        data = s.recv(1024).decode()
        if not data:
            break
        print(f'\n{data}')

def main():
    username = input("Enter Username: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(username.encode())

        print("Connected to server!")
        print("-" * 20)

        # Receive initial user list
        user_list = s.recv(1024).decode()
        print(user_list)
        print("-" * 20)

        # Create threads for sending and receiving
        send_thread = threading.Thread(target=send_messages, args=(s, username))
        receive_thread = threading.Thread(target=receive_messages, args=(s,))

        send_thread.start()
        receive_thread.start()

        # Wait for both threads to finish before closing the connection
        send_thread.join()
        receive_thread.join()

if __name__ == "__main__":
    main()
