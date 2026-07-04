import paho.mqtt.client as mqtt
from command_handler import parse_command_payload,execute_command,build_command_ack
def on_connect(client,userdata,connect_flags,reason_code,properties):
    if reason_code == 0:
        print("mqtt broker connected:",reason_code)
        command_topic =userdata["command_topic"]
        result,mid=client.subscribe(command_topic)
        print("mqtt command topic subscribed:",command_topic)
    else:
        print("mqtt broker connection failed:",reason_code)
def create_mqtt_client(client_id):
    client =mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=client_id
    )
    return client
def connect_mqtt_client(client,broker,port,keepalive,command_topic,ack_topic):
    client.user_data_set({"command_topic":command_topic,"ack_topic":ack_topic})
    client.on_connect =on_connect
    client.on_message=on_message
    client.connect(broker,port,keepalive)
    client.loop_start()
def publish_mqtt_message(client,topic,payload):
    message_info = client.publish(topic,payload)
    if message_info.rc==mqtt.MQTT_ERR_SUCCESS:
        message_info.wait_for_publish()
        print("mqtt message published:",topic)
        return True
    else:
        print("mqtt publish failed:", message_info.rc)
        return False
def publish_command_ack(client,topic,payload):
    message_info=client.publish(topic,payload)
    if message_info.rc == mqtt.MQTT_ERR_SUCCESS:
        print("mqtt ack queued:",topic)
        return True
    else:
        print("mqtt ack publish failed:",message_info.rc)
        return False
def on_message(client,userdata,message):
    topic=message.topic
    payload=message.payload.decode("utf-8")
    print("mqtt command received")
    print("topic:",topic)
    print("payload",payload)
    command=parse_command_payload(payload)
    if command is None:
        return
    print("command:",command)
    command_result=execute_command(command)
    if command_result:
        print("command executed successfully:",command)
    else:
        print("command execution failed:",command)
    ack_topic=userdata["ack_topic"]
    ack_payload=build_command_ack(command,command_result)
    publish_command_ack(client,ack_topic,ack_payload)
def disconnect_mqtt_client(client):
    client.disconnect()
    client.loop_stop()
    print("mqtt connect disconnected")
def configure_mqtt_last_will(client,topic,payload):
    client.will_set(topic,payload)
    print("mqtt last will configure:",topic)