project_name="linux-serial-tool"
verision="v0.1"
author="shuisuisheng"
port="/dev/ttyUSB0"
temperature_str="25.3"
temperature=float(temperature_str)
baudrate=9600
threshold=30
if temperature > threshold:
    print("warning")
else:
    print("normal")
