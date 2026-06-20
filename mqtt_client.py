import paho.mqtt.client as mqtt
def create_mqtt_client(client_id):
    client =mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=client_id
    )
    return client