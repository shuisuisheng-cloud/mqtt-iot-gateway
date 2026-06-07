# Linux Serial Tool

## 项目简介

这是一个基于 Linux / WSL + Python 的串口数据解析与日志工具。

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

## 依赖安装

当前版本仅使用 Python 标准库，无需额外安装第三方依赖。

后续接入真实串口和 MQTT 后，将使用：

- pyserial
- paho-mqtt

如果后续 requirements.txt 中加入依赖，可使用：

```bash
pip install -r requirements.txt
```