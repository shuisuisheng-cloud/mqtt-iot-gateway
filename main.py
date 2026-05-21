import time
import random
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
        if temperature is None:
            save_line("invalid data:"+serial_data)
            print("invalid data")
        else:
            temperature_str=str(temperature)
            time.sleep(1)
            log="temperature:"+temperature_str+" "+"status:"+check_temperature(temperature)
            save_line(str(log))
            print(log)
        count +=1
if __name__ == "__main__":    
    main()
# "temperature:"+str(round(random.uniform(20,40),1))