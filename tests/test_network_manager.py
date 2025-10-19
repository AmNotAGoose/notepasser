import time
from core.network_manager import NetworkManager

def test_send_and_receive():
    received = []

    def callback(inp, addr):
        received.append(inp)

    nm = NetworkManager("127.0.0.1", 30303, callback)

    nm.send_packet("hello", "127.0.0.1", 30303)

    time.sleep(0.5)

    assert "hello" in received
