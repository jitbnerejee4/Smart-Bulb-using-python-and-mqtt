import paho.mqtt.client as mqtt
import time

broker_address = "test.mosquitto.org" 
broker_port = 1883
topic_state = "smart-light-bulb/state"
topic_brightness = "smart-light-bulb/brightness"


class SmartLightBulb:
    def __init__(self):
        self.bulb_state = False
        self.brightness_level = 0

    # Callback function when a message is received on the subscribed topics
    def on_message(self, client, userdata, message):
        if message.topic == topic_state:
            if message.payload.decode() == "on":
                self.bulb_state = True
            elif message.payload.decode() == "off":
                self.bulb_state = False
        elif message.topic == topic_brightness:
            self.brightness_level = int(message.payload)

    # Connect to MQTT broker and subscribe to topics
    def connect(self):
        client = mqtt.Client()
        client.on_message = self.on_message
        client.connect(broker_address, broker_port)
        client.subscribe(topic_state)
        client.subscribe(topic_brightness)
        client.loop_start()
        print("Connected to MQTT broker and subscribed to topics")

        # Loop to continuously check the bulb state and brightness level and publish to MQTT topics
        while True:
            try:
                bulb_state_str = "on" if self.bulb_state else "off"
                brightness_level_str = str(self.brightness_level)
                client.publish(topic_state, bulb_state_str)
                client.publish(topic_brightness, brightness_level_str)
                print("Bulb is " + bulb_state_str + " and brightness level is " + brightness_level_str)
                time.sleep(1)
            except Exception as error:
                print("There is an error!", error)



if __name__ == '__main__':
    bulb = SmartLightBulb()
    bulb.connect()
