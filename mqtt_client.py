import paho.mqtt.client as mqtt
def on_connect(client,userdata,connect_flags,reason_code,properties):
    if reason_code == 0:
        print("mqtt broker connected:",reason_code)
    else:
        print("mqtt broker connection failed:",reason_code)
def create_mqtt_client(client_id):
    client =mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=client_id
    )
    return client
def connect_mqtt_client(client,broker,port,keepalive):
    client.on_connect =on_connect
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