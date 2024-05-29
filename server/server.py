import socket
import threading

HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 11001        # Port to listen on (non-privileged ports are > 1023)

client_list = []
client_lock = threading.Lock()


def handle_client(conn, addr):
    print(f"System: [Connected by] {addr}")
    username = conn.recv(1024).decode()

    with client_lock:
        client_list.append((username, conn))

    broadcast(f"System: {username} has joined the chat!")

    # Create threads for receiving and broadcasting
    receive_thread = threading.Thread(target=receive_messages, args=(conn, username))

    receive_thread.start()

    # Wait for both threads to finish before closing the connection
    receive_thread.join()

    broadcast(f"System: {username} left the chat!")
    conn.close()
    with client_lock:
        client_list.remove((username, conn))
    print(f"System: [Disconnected by] {addr}")

def receive_messages(conn, username):
    while True:
        data = conn.recv(1024)
        if not data:
            break

        with client_lock:
            for user, c in client_list:
                # Don't send data to receiver
                if c == conn:
                    continue
                try:
                    c.sendall(f"{username}: {data.decode()}".encode())
                except:
                    client_list.remove((user, c))
                    break


def broadcast(msg):
    with client_lock:
        for user, conn in client_list:
            try:
                conn.sendall(msg.encode())
            except:
                client_list.remove((user, conn))
                break


def send_user_list(conn):
    with client_lock:
        usernames = [user for user, _ in client_list]
        usernames.sort()  # Sort usernames alphabetically
        user_list = "\n".join(usernames)
        conn.sendall(f'Connected to server!'.encode())
        #conn.sendall(f"Current Users:\n{user_list}".encode())


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen()

    print(f"System: Server listening on port {PORT}")

    while True:
        conn, addr = sock.accept()
        send_user_list(conn)
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()


if __name__ == "__main__":
    main()

