import json
import queue

from core.debug.debugging import log


class PeerEvents:
    def __init__(self, disconnect):
        self.disconnect = disconnect

        self.messages = queue.Queue()
        self.token_requests = queue.Queue()

    def on_event_received(self, addr, event):
        if not event["type"]:
            log(f"[{addr}] event missing type! {json.dumps(event)}")
            return

        log(f"[{addr}] {event}")

        match event["type"]:
            case "message":
                self.messages.put([addr, event])
            case "trusted_token":
                self.token_requests.put([addr, event])
            case "disconnect":
                log(f"disconnect gracefully")
                self.disconnect()
                return
            case _:
                log("broke")
                self.disconnect()
