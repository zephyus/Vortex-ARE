import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from system_engine import NeuralHub


def run_test():
    hub = NeuralHub()
    called = {"count": 0}

    def bad_callback(_payload):
        raise RuntimeError("intentional callback failure")

    def good_callback(payload):
        if payload.get("ok"):
            called["count"] += 1

    hub.subscribe("topic", bad_callback)
    hub.subscribe("topic", good_callback)
    hub.emit("topic", {"ok": True})

    assert called["count"] == 1, "good callback should still execute despite bad callback"


if __name__ == "__main__":
    run_test()
    print("test_neuralhub.py: PASS")
