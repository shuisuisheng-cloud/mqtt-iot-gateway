import json
def parse_command_payload(payload_text):
    try:
        command_data=json.loads(payload_text)
    except json.JSONDecodeError:
        print("invalid command json")
        return None
    if not isinstance(command_data,dict):
        print("command must be an object")
        return None
    command=command_data.get("command")
    if not isinstance(command,str):
        print("command must be a string")
        return None
    command=command.strip()
    if command == "":
        print("command cannot be empty")
        return None
    return command
def execute_command(command):
    if command == "led_on":
        print("simulated actuator: LED ON")
        return True

    elif command == "led_off":
        print("simulated actuator: LED OFF")
        return True

    else:
        print("unsupported command:", command)
        return False
def build_command_ack(command, success):
    if success:
        status = "success"
    else:
        status = "failed"

    ack_data = {
        "command": command,
        "status": status
    }

    return json.dumps(ack_data)