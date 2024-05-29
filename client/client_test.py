import unittest
import socket
import threading
import time

class ClientTest(unittest.TestCase):

    def setUp(self):
        self.server_host = 'localhost'
        self.server_port = 11001
        self.username = 'TestUser'

    def test_connect_to_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.server_host, self.server_port))
            s.sendall(self.username.encode())
            response = s.recv(1024).decode()
            self.assertEqual(response, f"Connected to server!", "Server connection failed")

    def test_send_message(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.server_host, self.server_port))
            s.sendall(self.username.encode())

            def send_message_thread():
                time.sleep(1)  # Wait for server to process connection
                s.sendall(b"Test message")

            send_thread = threading.Thread(target=send_message_thread)
            send_thread.start()

            response = s.recv(1024).decode()
            self.assertEqual(response, f"{self.username}: Test message", "Message sending failed")

    def test_receive_message(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.server_host, self.server_port))
            s.sendall(self.username.encode())

            def send_message_thread():
                time.sleep(1)  # Wait for server to process connection
                s.sendall(b"Test message")

            send_thread = threading.Thread(target=send_message_thread)
            send_thread.start()

            time.sleep(2)  # Wait for message to be received

            response = s.recv(1024).decode()
            self.assertEqual(response, f"Test message", "Message receiving failed")

if __name__ == '__main__':
    unittest.main()
