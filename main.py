import machine
from machine import ADC, Pin
from time import sleep
from dht import DHT11
from simple import MQTTClient   #added a umqtt-simple file, Pico refused to collect from umqtt.simple
import micropython            # Needed to run any MicroPython code
import keys                   # Contain all keys used here

#Use the MQTT protocol to connect to TIG stack
client = MQTTClient(keys.CLIENT_ID, keys.MQTT_BROKER, port=keys.MQTT_PORT, user=keys.MQTT_USER, password=keys.MQTT_KEY)
#Example code and some trouble-shooting from this video: https://www.youtube.com/watch?v=Gsw0CIsJJfE
def connect_to_mqtt():
    try:
        client.connect()
        print("Connected to the MQTT Broker")
    except Exception as e:
        print("Failed to connect to MQTT Broker")

#All relevant pieces like Sensors and Actuators are listed here
#DHT11 sensor
ambientsensor = DHT11(Pin(22))

#Photo Resistor light sensor
ldr = ADC(Pin(27))

#RGB LED
LED_Pin_Red = Pin(3, Pin.OUT)
LED_Pin_Green = Pin(2, Pin.OUT)
LED_Pin_Blue = Pin(4, Pin.OUT)

#Function to publish DHT11 humidity data to MQTT broker
def publish_humidity(client):
    try:
        humidity = ambientsensor.humidity()
        print("Publishing: Humidity: {}%".format(humidity))
        client.publish(keys.MQTT_TOPIC_HUMIDITY, b"%.2f" % humidity)
    except Exception as e:
        print(e)
        
#Function to publish DHT11 humidity data to MQTT broker
def publish_temperature(client):
    try:
        temperature = ambientsensor.temperature()
        print("Publishing: Temperature: {}°C".format(temperature))
        client.publish(keys.MQTT_TOPIC_TEMP, b"%.2f" % temperature)
    except Exception as e:
        print(e)
        
#Function to publish DHT11 humidity data to MQTT broker
def publish_brightness(client):
    try:
        light = ldr.read_u16()
        brightness = 100-round(light / 65535 * 100, 1)
        print("Publishing: Brightness: {}%".format(brightness))
        client.publish(keys.MQTT_TOPIC_LIGHT, b"%.2f" % brightness)
    except Exception as e:
        print(e) 
        
def check_ambient(temperature, humidity):
    #I defined a happy plants conditions where ambient climate was good.
    ambient = ("Temperature ({}°C) and humidity ({}%) ok, plants are happy.".format(temperature, humidity))
    happy_plants = True
    
    #And that this condition is false whenever one condition is out of bounds
    #Conditions from: https://kryzen.com/optimizing-air-temperature-and-humidity-for-hydroponic-crops/ and,
    #https://greg.app/garden-lettuce-humidity/
    if temperature >= 27:
        ambient = ("Temperature is above 27°C ({}°C)".format(temperature))
        happy_plants = False
    elif temperature < 18:
        ambient = ("Temperature is below 18°C ({}°C)".format(temperature))
        happy_plants = False
    elif humidity > 70:
        ambient = ("Humidity is above 70% ({}%)".format(humidity))
        happy_plants = False
    elif humidity <= 40:
        ambient = ("Humidity is below 40% ({}%)".format(humidity))
        happy_plants = False
    
    #In great conditions the LED is green, in poor conditions it is red.
    if happy_plants==True:
        LED_Pin_Red.value(0)
        LED_Pin_Green.value(1)
        LED_Pin_Blue.value(0)
    else:
        LED_Pin_Red.value(1)
        LED_Pin_Green.value(0)
        LED_Pin_Blue.value(0)

    print(ambient)
   
try:
    connect_to_mqtt()  
    while True:
        try:
            ambientsensor.measure()
            temperature = ambientsensor.temperature()
            humidity = ambientsensor.humidity()
            check_ambient(temperature, humidity)
            publish_humidity(client)
            publish_temperature(client)
            publish_brightness(client)
        except Exception as error:
            print("Exception occurred", error)
        sleep(60)
    
finally:
    client.disconnect()   # ... disconnect the client and turn off LED
    client = None
    LED_Pin_Red.value(0)
    LED_Pin_Green.value(0)
    LED_Pin_Blue.value(0)
    print("Disconnected from MQTT.")