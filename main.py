threshold=30
def check_temperature(temp):
    if temp > threshold:
        return "warning"
    else:
        return "normal"
def main():
    project_name="linux-serial-tool"
    verision="v0.1"
    author="shuisuisheng"
    port="/dev/ttyUSB0"
    temperature_str="25.3"
    temperature=float(temperature_str)
    baudrate=9600
    print(check_temperature(temperature))
if __name__ == "__main__":    
    main()