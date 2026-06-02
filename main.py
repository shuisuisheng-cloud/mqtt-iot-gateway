import time
import random
import json
threshold=30
def save_line(line):
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
def handle_json_data(temperature,device):
    status=check_temperature(temperature)
    timestatus=time.strftime("%Y-%m-%d %H:%M:%S")
    device_data=build_device_data(device,temperature,status,timestatus)
    json_data=json.dumps(device_data)
    save_line(json_data)
    time.sleep(1)
    print("valid data:","temperature:",device_data["temperature"],"status:",device_data["status"],"timestamp:",device_data["timestamp"])
def handle_invalid_data(device,data,timestatus):
    line="device:"+" "+device+" "+"invalid_data:"+" "+data+" "+"timestamp:"+" "+timestatus
    save_line(line)
    time.sleep(1)
    print("invalid data:" + data,"timestamp:" + timestatus)
def main():
    project_name="linux-serial-tool"
    verision="v0.1"
    author="shuisuisheng"
    port="/dev/ttyUSB0"
    baudrate=9600
    device = "stm32_node_01"
    test_data = ["temperature:28.6","temperature:abc","error_data","temperature:","temperature:31.5"]
    timestatus=time.strftime("%Y-%m-%d %H:%M:%S")
    for serial_data in test_data:
        temperature=parse_temperature(serial_data)
        if temperature is None:
            handle_invalid_data(device,serial_data,timestatus)
        else:
            handle_json_data(temperature,device)
if __name__ == "__main__":    
    main()
