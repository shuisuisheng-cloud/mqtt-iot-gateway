# mqtt-iot-gateway

## 项目简介

这是一个基于 Linux + Python + pyserial + MQTT 的物联网边缘网关项目。

当前版本已完成串口数据解析、JSON 日志、异常处理、模式切换和 pyserial 读取函数预留，后续将接入 MQTT 发布与订阅。

当前项目用于模拟从 STM32 等嵌入式设备接收串口数据，完成温度数据解析、异常数据处理、JSON 格式转换和日志保存。

本项目是后续 Linux 串口与 MQTT 物联网网关系统的第一阶段。

## 当前功能

- 模拟串口数据输入
- 解析 temperature:xx.x 格式数据
- 判断温度状态 normal / warning
- 处理异常数据，避免程序崩溃
- 使用 dict 组织设备数据
- 使用 JSON 保存结构化日志
- 为每条数据增加 device 和 timestamp 字段
- 将正常数据和异常数据写入 logs/serial.log

## 运行环境

- Ubuntu / WSL
- Python 3
- VSCode
- Git / GitHub

## 运行方式

```bash
python3 main.py
```

## 示例输出

```text
valid data: device: stm32_node_01 temperature: 28.6 status: normal timestamp: 2026-06-04 15:24:24
invalid data: device: stm32_node_01 raw: temperature:abc timestamp: 2026-06-04 15:24:24
valid data: device: stm32_node_01 temperature: 31.5 status: warning timestamp: 2026-06-04 15:24:28
```

## JSON日志格式
正常日志格式：

```JSON
{"device": "stm32_node_01", "temperature": 28.6, "status": "normal", "timestamp": "2026-06-04 15:24:24"}
```
```text
device:stm32_node_01 invalid_data:temperature:abc timestamp:2026-06-04 15:24:24
```
## 配置文件

项目使用 `config.json` 管理网关基础参数：

```json
{
    "project_name": "Linux-STM32 IoT Edge Gateway",
    "version": "v0.1",
    "author": "shuisuisheng",
    "port": "/dev/ttyUSB0",
    "baudrate": 9600,
    "device": "stm32_node_01",
    "use_real_serial": false
}
```
## 当前阶段说明

当前版本仍使用模拟串口数据进行测试。

项目已加入 pyserial 依赖，并预留真实串口读取函数：

```python
read_serial_data_from_port(port, baudrate)
```

## 当前依赖

- pyserial

## 后续依赖

- paho-mqtt

