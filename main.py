import time
import random
import json
import os
import serial
threshold=30
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
def check_temperature(temp):
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
def build_device_data(device,temperature,status,time):
    return {"device":device,"temperature":temperature,"status":status,"timestamp":time}
def get_timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S")
def handle_valid_data(temperature,device,timestamp):
    status=check_temperature(temperature)
    device_data=build_device_data(device,temperature,status,timestamp)
    json_data=json.dumps(device_data)
    save_line(json_data)
    time.sleep(1)
    print("valid data:","device:",device_data["device"],"temperature:",device_data["temperature"],"status:",device_data["status"],"timestamp:",device_data["timestamp"])
def handle_invalid_data(device,data,timestatus):
    line="device:"+" "+device+" "+"invalid_data:"+" "+data+" "+"timestamp:"+" "+timestatus
    save_line(line)
    time.sleep(1)
    print("invalid data: "+"device: "+device +"raw: "+ data,"timestamp: " + timestatus)
def main():
    project_name="linux-serial-tool"
    verision="v0.1"
    author="shuisuisheng"
    port="/dev/ttyUSB0"
    baudrate=9600
    device = "stm32_node_01"
    use_real_serial=False
    test_data = ["temperature:28.6","temperature:abc","error_data","temperature:","temperature:31.5"]
    if use_real_serial:
        print("real serial mode")
        serial_data_port=read_serial_data_from_port(port,baudrate)
        timestamp=get_timestamp()
        if serial_data_port is None:
            print("read serial_data_from_port fail")
            handle_invalid_data(device, "serial_read_failed", timestamp)
        else:
            temperature=parse_temperature(serial_data_port)
            if temperature is None:
                handle_invalid_data(device,serial_data,timestamp)
            else:
                handle_valid_data(temperature,device,timestamp)
    else:
        print("mock serial mode")
        for serial_data in test_data:
            temperature=parse_temperature(serial_data)
            timestamp = get_timestamp()
            if temperature is None:
                handle_invalid_data(device,serial_data,timestamp)
            else:
                handle_valid_data(temperature,device,timestamp)
if __name__ == "__main__":    
    main()
