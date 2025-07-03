import ubinascii              # Conversions between binary data and various encodings
import machine                # To Generate a unique id from processor

# Wireless network
WIFI_SSID = "{your_SSID}" #change
WIFI_PASS = "{your_password}" #change

#TIG Stack keys
CLIENT_ID = "Pico"
MQTT_BROKER = "{your_IP}" #change
MQTT_PORT = 1883

#MOSQUITTO LOG IN
MQTT_USER = "{your_user_name}" #change
MQTT_KEY = "{your_password}" #change

# topics
MQTT_TOPIC_HUMIDITY = "humidity"
MQTT_TOPIC_TEMP = "temperature"
MQTT_TOPIC_LIGHT = "brightness"