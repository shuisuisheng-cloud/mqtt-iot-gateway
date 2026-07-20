import json
import serial
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
def send_command_to_serial(ser, command):
    if ser is None:
        print(f"ser is not exist:{ser}")
        return False
    if not  ser.is_open:
        print(f"ser is not open:{ser}")
        return False
    if not isinstance(command,str):
        print(f"command is not str:{command}")
        return False
    command = command.strip()
    if command =="":
        print(f"command can not be empty")
        return False
    if command not in ("led_on", "led_off"):
        print(f"unsupported serial command: {command}")
        return False
    right_command=command+"\r\n"
    command_bytes=right_command.encode("utf-8")
    try:
        written_bytes = ser.write(command_bytes)

        if written_bytes != len(command_bytes):
            print(f"serial partial write: "f"written={written_bytes}, "f"expected={len(command_bytes)}")
            return False

        print(f"command forwarded to serial: {command}")
        return True

    except serial.SerialTimeoutException as e:
        print(f"serial write timeout: {e}")
        return False

    except serial.SerialException as e:
        print(f"serial write failed: {e}")
        return False