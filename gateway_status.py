import json
def build_heartbeat_payload(gateway_id,device,timestamp):
    heartbeat_data = {
        "gateway": gateway_id,
        "device": device,
        "status": "online",
        "timestamp": timestamp
    }

    return json.dumps(heartbeat_data)
def build_gateway_status_payload(gateway_id,device):
    gateway_status_payload={"gateway":gateway_id,"device":device,"status":"offline","reason":"unexpected_disconnect"}
    return json.dumps(gateway_status_payload)