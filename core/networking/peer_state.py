from enum import auto, IntEnum


class PeerState(IntEnum):
    UNDISCOVERED = auto()
    DISCOVERED = auto()
    CONNECTING = auto()
    CONNECTED = auto()
    DISCONNECTING = auto()
    DISCONNECTED = auto()
