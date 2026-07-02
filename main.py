import time
import random
import json
import os
import serial
from mqtt_client import create_mqtt_client,connect_mqtt_client,publish_mqtt_message,disconnect_mqtt_client
def read_serial_data_from_port(port, baudrate):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        line = ser.readline().decode("utf-8").strip()
        ser.close()
        return line
    except:
        print("serial read error")
        return None
def save_line(line):
    os.makedirs("logs", exist_ok=True)
    with open("logs/serial.log","a",encoding="utf-8") as f:
        f.write(line+"\n")
def check_temperature(temp,threshold):
    if temp > threshold:
        return "warning"
    else:
        return "normal"
def read_serial_data():
    return "temperature:"+str(round(random.uniform(20,40),1))
def parse_temperature(data):
    try:
        part=data.split(":")
        temperature=float(part[1])
        return temperature
    except:
        return None
def build_device_data(device,temperature,status,time,threshold):
    return {"device":device,"temperature":temperature,"status":status,"timestamp":time,"temperature_threshold":threshold}
def get_timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S")
def load_config():
    with open("config.json","r",encoding="utf-8") as f:
        config=json.load(f)
    return config
def handle_valid_data(temperature,device,timestamp,threshold):
    status=check_temperature(temperature,threshold)
    device_data=build_device_data(device,temperature,status,timestamp,threshold)
    json_data=json.dumps(device_data)
    save_line(json_data)
    time.sleep(1)
    print("valid data:","device:",device_data["device"],"temperature:",device_data["temperature"],"status:",device_data["status"],"timestamp:",device_data["timestamp"])
    return json_data
def handle_invalid_data(device,data,timestatus):
    line="device:"+" "+device+" "+"invalid_data:"+" "+data+" "+"timestamp:"+" "+timestatus
    save_line(line)
    time.sleep(1)
    print("invalid data: "+"device: "+device +"raw: "+ data,"timestamp: " + timestatus)
    return None
def process_serial_data(device,serial_data,threshold):
    timestamp=get_timestamp()
    temperature=parse_temperature(serial_data)
    if temperature is None:
        return handle_invalid_data(device,serial_data,timestamp)
    else:
        return handle_valid_data(temperature,device,timestamp,threshold)
def main():
    config=load_config()
    threshold=config["temperature_threshold"]
    project_name=config["project_name"]
    verision=config["version"]
    author=config["author"]
    port=config["port"]
    baudrate=config["baudrate"]
    device = config["device"]
    mqtt_enabled = config["mqtt_enabled"]
    mqtt_broker = config["mqtt_broker"]
    mqtt_port = config["mqtt_port"]
    mqtt_client_id = config["mqtt_client_id"]
    mqtt_topic_prefix = config["mqtt_topic_prefix"]
    mqtt_keepalive = config["mqtt_keepalive"]
    use_real_serial=config["use_real_serial"]
    telemetry_topic = f"{mqtt_topic_prefix}/{device}/telemetry"
    command_topic = f"{mqtt_topic_prefix}/{device}/command"
    ack_topic =f"{mqtt_topic_prefix}/{device}/ack"
    test_data = ["temperature:28.6","temperature:abc","error_data","temperature:","temperature:31.5"]
    mqtt_client=None
    if mqtt_enabled:
        mqtt_client=create_mqtt_client(mqtt_client_id)
        print("mqtt client created")
        connect_mqtt_client(
            mqtt_client,
            mqtt_broker,
            mqtt_port,
            mqtt_keepalive,
            command_topic,
            ack_topic
        )
    else:
        print("mqtt disabled")
    print("mqtt enabled:", mqtt_enabled)
    print("mqtt broker:", mqtt_broker)
    print("mqtt port:", mqtt_port)
    print("mqtt client id:", mqtt_client_id)
    print("telemetry topic:", telemetry_topic)
    print("command topic:", command_topic)
    if use_real_serial:
        print("real serial mode")
        serial_data_port=read_serial_data_from_port(port,baudrate)
        timestamp=get_timestamp()
        if serial_data_port is None:
            print("read serial_data_from_port fail")
            print("fellback to mock serial mode")
            handle_invalid_data(device, "serial_read_failed", timestamp)
            for mock_data in test_data:
               process_serial_data(device,mock_data,threshold)
        else:
            process_serial_data(device,serial_data_port,threshold)
    else:
        print("mock serial mode")
        for serial_data in test_data:
            payload=process_serial_data(device,serial_data,threshold)
            if payload is not None and mqtt_client is not None:
                publish_mqtt_message(mqtt_client,telemetry_topic,payload)
    if mqtt_client is not None:
            try:
                print("gateway running, press Ctrl+C to stop")
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\ngateway shutdown requested")
            finally:
                disconnect_mqtt_client(mqtt_client)   
if __name__ == "__main__":    
    main()
