import time
import random
threshold=30
def check_temperature(temp):
    if temp > threshold:
        return "warning"
    else:
        return "normal"
def read_serial_data():
    return "temperature:"+str(round(random.uniform(20,35),1))
def parse_temperature(data):
    return float(data.split(":")[1])
def main():
    project_name="linux-serial-tool"
    verision="v0.1"
    author="shuisuisheng"
    port="/dev/ttyUSB0"
    baudrate=9600
    count=1
    while count <=5:
        serial_data=read_serial_data()
        temperature=parse_temperature(serial_data)
        temperature_str=str(temperature)
        time.sleep(1)
        print("temperature:"+temperature_str,"status:"+check_temperature(temperature))
        count +=1
if __name__ == "__main__":    
    main()