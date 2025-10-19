import socket
import threading


class NetworkManager:
    def __init__(self, ip, port, on_receive):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.MY_IP = ip
        self.MY_PORT = port

        self.sock.bind((self.MY_IP, self.MY_PORT))

        self.on_receive = on_receive
        self.running = True
        thread = threading.Thread(target=self.listen, daemon=True)
        thread.start()

    def send_packet(self, message: str, ip, port):
        self.sock.sendto(message.encode("utf-8"), (ip, port))

    def listen(self):
        while self.running:
            data, addr = self.sock.recvfrom(4096)
            self.on_receive(data.decode("utf-8"), addr)
