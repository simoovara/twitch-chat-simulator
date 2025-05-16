import websocket
import json

class OBSWebsocket:
    def __init__(self, ip, port: int):
        self.ws: websocket.WebSocket = websocket.create_connection(f"ws://{ip}:{port}")

        identify = {"op":1,"d":{"rpcVersion":1}}  # Identify payload so the websocket acts nice to us

        self.send_message(identify)

    def __del__(self):
        self.ws.close()

    def send_message(self, message):
        self.ws.send(json.dumps(message))
        res = self.ws.recv()
        print(f"Received response: {res}")
        return res

    def send_start_timer(self):
        message = {
            "op": 6,
            "d": {
                "requestType": "CallVendorRequest",
                "requestId": "playTimer1",
                "requestData": {
                    "vendorName": "ashmanix-countdown-timer",
                    "requestType": "period_play",
                }
            }
        }

        self.ws.send(json.dumps(message))
        res = self.ws.recv()
        print(f"Received response: {res}")
        return res

    def send_pause_timer(self):
        message = {
            "op": 6,
            "d": {
                "requestType": "CallVendorRequest",
                "requestId": "pauseTimer1",
                "requestData": {
                    "vendorName": "ashmanix-countdown-timer",
                    "requestType": "period_pause",
                }
            }
        }

        self.ws.send(json.dumps(message))
        res = self.ws.recv()
        print(f"Received response: {res}")
        return res

    def send_reset_timer(self):
        message = {
            "op": 6,
            "d": {
                "requestType": "CallVendorRequest",
                "requestId": "resetTimer1",
                "requestData": {
                    "vendorName": "ashmanix-countdown-timer",
                    "requestType": "period_set",
                }
            }
        }

        self.ws.send(json.dumps(message))
        res = self.ws.recv()
        print(f"Received response: {res}")
        return res