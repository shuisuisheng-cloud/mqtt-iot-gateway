import json
def build_heartbeat_payload(gateway_id,device,timestamp):
    heartbeat_data = {
        "gateway": gateway_id,
        "device": device,
        "status": "online",
        "timestamp": timestamp
    }

    return json.dumps(heartbeat_data)