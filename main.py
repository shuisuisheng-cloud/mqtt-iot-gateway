import time
import random
import json
import os
import serial
from mqtt_client import create_mqtt_client,connect_mqtt_client,publish_mqtt_message,disconnect_mqtt_client,configure_mqtt_last_will
from gateway_status import build_heartbeat_payload,build_gateway_status_payload
def open_ser_port(port,baudrate):
    try:
        ser=serial.Serial(port,baudrate,timeout=0.2,write_timeout=0.2)
        print(f"成功打开{port}")
        return ser
    except serial.SerialException as e:
        print(f"打开串口 {port} 失败: {e}")
        return None
def read_data_from_port(ser):
    if ser is None:
        return None
    try:
        raw_data = ser.readline()
        if raw_data == b"":
            return None
        line = raw_data.decode("utf-8").strip()
        if line == "":
            return None
        return line
    except serial.SerialException as e:
        print(f"串口读取失败: {e}")
        return None
    except UnicodeDecodeError as e:
        print(f"串口数据解码失败: {e}")
        return None
def close_ser_port(ser):
    if ser is not None and ser.is_open:
        try:
            ser.close()
            print("串口已关闭")

        except serial.SerialException as e:
            print(f"关闭串口失败: {e}")
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
    print("valid data:","device:",device_data["device"],"temperature:",device_data["temperature"],"status:",device_data["status"],"timestamp:",device_data["timestamp"])
    return json_data
def handle_invalid_data(device,data,timestatus):
    line="device:"+" "+device+" "+"invalid_data:"+" "+data+" "+"timestamp:"+" "+timestatus
    save_line(line)
    print("invalid data: "+"device: "+device +"raw: "+ data,"timestamp: " + timestatus)
    return None
def handle_debug_data(serial_data):
    print(f"stm32 debug: {serial_data}")
    return None
def process_serial_data(device,serial_data,threshold):
    parts=serial_data.split(":")
    timestamp=get_timestamp()
    if parts[0]!="temperature":
        return handle_debug_data(serial_data)
    elif len(parts)!=2:
        return handle_invalid_data(device,serial_data,timestamp)
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
    heartbeat_interval = config["heartbeat_interval"]
    mqtt_reconnect_first_waiting_time=config["mqtt_reconnect_first_waiting_time"]
    mqtt_reconnect_max_waiting_time=config["mqtt_reconnect_max_waiting_time"]
    telemetry_topic = f"{mqtt_topic_prefix}/{device}/telemetry"
    command_topic = f"{mqtt_topic_prefix}/{device}/command"
    ack_topic =f"{mqtt_topic_prefix}/{device}/ack"
    heartbeat_topic = (f"{mqtt_topic_prefix}/gateway/{mqtt_client_id}/heartbeat")
    status_topic=(f"{mqtt_topic_prefix}/gateway/{mqtt_client_id}/status")
    test_data = ["temperature:28.6","temperature:abc","error_data","temperature:","temperature:31.5",
                 "temperature:26.4:extra","DHT11 raw: 41 0 26 4 71","DHT11 response: TIMEOUT","board:STM32F407VET6_CORE_BOARD_V2","KEY PRESSED"]
    online_status_payload=build_gateway_status_payload(mqtt_client_id,device,"online","connected")
    mqtt_client=None
    ser=None
    use_mock_serial = not use_real_serial
    if use_real_serial:
        print("real serial mode")
        ser = open_ser_port(port, baudrate)

        if ser is None:
            print(f"打开串口失败: {port}")
            print("fallback to mock serial mode")
            use_mock_serial = True
    else:
        print("mock serial mode")

    if mqtt_enabled:
        mqtt_client=create_mqtt_client(mqtt_client_id)
        print("mqtt client created")
        status_payload=build_gateway_status_payload(mqtt_client_id,device,"offline" ,"unexpected_disconnect")
        configure_mqtt_last_will(mqtt_client,status_topic,status_payload)
        connect_mqtt_client(
            mqtt_client,
            mqtt_broker,
            mqtt_port,
            mqtt_keepalive,
            command_topic,
            ack_topic,
            status_topic,
            online_status_payload,
            mqtt_reconnect_first_waiting_time,
            mqtt_reconnect_max_waiting_time,
            ser
        )
    else:
        print("mqtt disabled")
    print("mqtt enabled:", mqtt_enabled)
    print("mqtt broker:", mqtt_broker)
    print("mqtt port:", mqtt_port)
    print("mqtt client id:", mqtt_client_id)
    print("telemetry topic:", telemetry_topic)
    print("command topic:", command_topic)

    last_heartbeat_time=0.0
    last_mock_time=0.0
    test_data_number=0
    try:
        print("gateway running, press Ctrl+C to stop")
        while True:
            current_time=time.monotonic()
            serial_data=None
            if  use_mock_serial:
                if current_time-last_mock_time>=2:
                    serial_data=test_data[test_data_number]
                    last_mock_time=current_time
                    test_data_number=(test_data_number+1)%len(test_data)
            else:
                if ser is not None:
                    serial_data=read_data_from_port(ser)
            if serial_data is not None:
                payload = process_serial_data(device,serial_data,threshold)
                if mqtt_client is not None and mqtt_client.is_connected() and payload is not None:
                    publish_mqtt_message(mqtt_client,telemetry_topic,payload)
            if current_time - last_heartbeat_time >= heartbeat_interval:
                if mqtt_client is not None and mqtt_client.is_connected():
                    timestamp=get_timestamp()
                    heartbeat_payload=(build_heartbeat_payload(mqtt_client_id,device,timestamp))
                    publish_mqtt_message(mqtt_client,heartbeat_topic,heartbeat_payload)
                last_heartbeat_time=current_time
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\ngateway shutdown requested")
    finally:
        if mqtt_client is not None and mqtt_client.is_connected():
            graceful_shutdown_Offline_Payload=build_gateway_status_payload(mqtt_client_id,device,"offline","graceful_shutdown")
            publish_mqtt_message(mqtt_client,status_topic,graceful_shutdown_Offline_Payload,retain=True)
        if ser is not None and ser.is_open:
            close_ser_port(ser)
        if mqtt_client is not None:
            disconnect_mqtt_client(mqtt_client)   
if __name__ == "__main__":    
    main()
