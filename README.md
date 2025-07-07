# Tutorial on how to build an aeroponics monitoring system
**Isabelle Berg - ib222zz**

For HackMD version of the report go to: https://hackmd.io/@Bookbells/B1KtttMreg 

## Overview
An aeroponics monitoring system was made using an RP2040 Raspberry Pi Pico WH as the microcontroller (MCU). The MCU was coupled with several sensors to measure ambient temperature, humidity, and light at the plant level of the system. This was coupled with an RGB LED light to provide a visual indication of whether the climate was within optimal parameters for the plants. To visualise the data, Grafana from a TIG-stack (Telegraf, InfluxDB, and Grafana) was coupled with Mosquitto MQTT code on the Pico. 

The approximate time to complete, with finished code and all hardware purchased, is 4-6 hours.

## Objective
I was studying this course during the summer break as part of a master’s program in environmental engineering with a focus on sustainable development, and IoT was often mentioned. However, the university did not offer a course on it, so I wanted to complement my knowledge with an introductory IoT course. The reason this project was chosen was due to an interest in aeroponics, as well as how a home DIY system could be optimized using the knowledge gained in the course. 

It is possible to make an entirely manual aeroponics system that involves regularly checking temperature to figure out the surrounding climate, but with built-in sensors giving regular readings as well as a warning LED light for when something needs to be amended, makes the system a great deal less time-consuming and offers new functionalities. I will likely continue to improve the system over the summer to include more sensors for the bucket with nutritional solution, such as a pH and/or TDS sensor, as well as more automation, such as controlling when the mister activates based on the humidity level around the roots. For each step, I will get a significant amount of data from the sensors on the health of the system and the plants, as well as notifications, which will help in the design of new improvements.

## Material
The acquired hardware, price, and supplier are listed in Table 1 below. This is provided for each specific piece, resulting in a lower price than purchasing kits as I did. If you need additional basic electrical components, you can also purchase the base kits; [LNU starter](https://www.electrokit.com/lnu-starter) and [Sensor Kit](https://www.electrokit.com/sensor-kit-25-moduler).

**Table 1:** How each component in this IoT project was acquired, details as of 2025-06-24.
| Component | Supplier | Article# | Price |
| -------- | -------- | -------- | --------|
| [Raspberry Pi Pico WH](https://www.electrokit.com/raspberry-pi-pico-wh)    | Electro:kit     | 41019114     |99 sek|
| [DHT11](https://www.electrokit.com/digital-temperatur-och-fuktsensor-dht11)     | Electro:kit     | 41015728     |49 sek|
| [Light sensor](https://www.electrokit.com/ljussensor)     | Electro:kit     | 41015727     |39 sek|
| [RGB LED-module](https://www.electrokit.com/led-modul-rgb)     | Electro:kit     | 41015715     |22 sek|

In addition to the MCU and sensors, you will also need basic electrical components, including a breadboard, wires, and a power supply. A brief description of each component's function is provided in Table 2 below.

**Table 2:** Short descriptions of components

| Component | Picture | Short description |
| -------- | -------- | -------- |
|Raspberry Pi Pico WH     | ![image](https://hackmd.io/_uploads/SkbuuoGHex.png)| A microcontroller unit (MCU) with an RP2040 ARM circuit and pre-soldered headers, which means it can be connected to a breadboard without soldering. Uses MicroPython as the programming language. For the Pinout diagram, see here.     |
|DHT11     | ![image](https://hackmd.io/_uploads/S1nOOoMHle.png)| A digital sensor that reads temperature (0-50±2 °C) and relative humidity (20-90%±5%).      |
|Light sensor     | ![image](https://hackmd.io/_uploads/HyXK_izSex.png)| An analogue light sensor with a non-linear light detection (%), detects lightness/darkness.     |
|RGB LED module SMD     | ![image](https://hackmd.io/_uploads/HJ9YuifHel.png)| A light diode that can be coded into a wide range of colors.     |

## Computer setup
I’m using a Windows laptop and had to download all of the required software since I’m new to IoT, which included:
1.	Thonny, installed from [here](https://github.com/thonny/thonny/releases/download/v4.1.7/thonny-4.1.7.exe), for the chosen IDE. I used this to code the Raspberry Pi Pico.
2.	Docker, installed from [here](https://docs.docker.com/compose/install/), for the Mosquitto, Telegraf, InfluxDB and Grafana images needed to transfer the data.
3.	Fritzing, installed from [here](https://fritzing.org/download), for drawing the circuit diagram.

### Thonny
After installation, the first step is to connect Thonny to the Pico in the “Run/Configure interpreter” section, where you select “MicroPython (Raspberry Pi Pico)” and choose the correct USB port that corresponds to the Pico's USB connection.
The next step is to update the firmware in the Pico, this is done by downloading the correct uf2 file. Since I had a Raspberry Pi Pico WH I used [this one](https://micropython.org/resources/firmware/RPI_PICO_W-20250415-v1.25.0.uf2) but you need to make sure it matches the Pico you are using. While holding down the Bootsel button, you can open the file manager when the Pico is connected to the computer. Release the Bootsel button, then simply drop the uf2 file into the Pico’s storage. Unplug and plug it back in and start testing the connection in Thonny to make sure everything is set up properly, then you are ready for coding! For my code see the section "The code". The basis of my code have been LNU tutorials which can be found here: https://hackmd.io/@lnu-iot, with additions and alterations from lectures, the book "Get started with Micropython on Raspberry Pi Pico" by Gareth Halfacree and Ben Everard (2nd editon, 2024) as well as guides found on the internet which is mentioned where applicable.

### Docker
The next essential software for this setup is Docker, be sure that you pick the correct version for your operating system. For Windows, it will automatically install a workaround to use it since it’s designed to work in Linux, allow this, and it will work.
After installing Docker, you need to pull the images you will be using. I used the search bar, but you can also use the command “Docker pull XXX” and replace XXX with the name of the image. The images I pulled were “eclipse-mosquitto:latest”, “telegraf: latest”, “influxdb:latest”, and “grafana/grafana:latest”. More about how to get the images in a working container under the section “Setting up the platform”. For now you should be able to see something like this under “Images”: 
![image](https://hackmd.io/_uploads/S15XHhfHxg.png)
*Figure 1: A printscreen of the downloaded images in my Docker.*

Before you can get anything working here, you will need to connect to a network. I picked a WiFi solution in boot.py, see the section "Transmitting the data / connectivity".

### Fritzing
Fritzing is entirely voluntary and not required for completing this project, I’m mentioning it since it was what I used to make the picture of how the hardware was connected. The basic library is pretty limited, but you can find most pieces by searching for the module you want and either “fzz” or “fritzing”, download the .fzz file, and then save it in your Fritzing.

## Putting everything together
Now comes the part where you connect all the hardware. I connected everything as shown in Figure 2. It’s essential to connect the power wires and ground correctly to prevent short-circuiting your Pico. Ground to “-“ sign, signal to “S”. Double-check the nodes in data-sheets for the module. Double-check all wires before connecting the Pico to the computer or power source.

An important note here is that sometimes the nodes on the smaller modules can be switched, as was the case both for my LDR and the RGB LED light. In my comment, you can see why I, in my case, had to switch the connections for signal and ground; wires are shown as connected on my Pico. For the RBD LED, you couldn’t see the shift, and I didn’t have to rewire anything to correct it. However, it turned out when I was coding that the node marked as “R” was actually the green one, and the one marked “G” was the red one. It was easily fixed by changing the PIN in the code after some troubleshooting. So, start with connecting according to the datasheet, and then perform some smaller tests to ensure the modules are responding as expected before proceeding to more advanced code.
![image](https://hackmd.io/_uploads/S1XtK3frge.png)
*Figure 2: Circuit diagram drawn in Fritzing.*

![Hardware](https://hackmd.io/_uploads/rkAg-QVHxg.png)
*Figure 3: Photograph of connected hardware.*

### Electrical calculations
*Nothing here yet, oh no! Any tips on what to add here would be aprreciated. :>*

## Platform
I have chosen to use a TIG (Telegraf, InfluxDB and Grafana) stack with Grafana for visualisation. Initially, I created an Adafruit platform. I got everything working but rather quickly noticed that I couldn’t design the dashboard the way I wanted, that there was a limit to the amount of data and that data was only saved for a month (in the free version), since I want to monitor my aeroponics system over a more extended period of time and have more options when building the dashboard I switched to a TIG-stack with Grafana for visualisation. See pictures under “Presenting the data” for the difference in the dashboard. 

The platform is currently installed on my laptop, but it will be moved to a local server, as there are issues with the Pico not sending signals as soon as the laptop goes into sleep mode. The local server is an old computer that is always on and is currently used to host the family’s IT solutions. I will continue to use the free version of Grafana for the foreseeable future, as it allows 50 GB of data and 2232 host hours (three months), which already offers possibilities for scaling. It only saves data for two weeks, but since InfluxDB is used for storage, this is fine. InfluxDB stores data indefinitely and offers the option of downloading the data, which would allow me to perform statistics in other sofware.

### Functionality
Many different components are connected to create a dashboard that visualizes the sensor data from your Pico; they are connected and function as shown in Figure 4.

![image](https://hackmd.io/_uploads/BytYRGVSxx.png)
*Figure 4: Diagram of the functionality and connectivity between the different components.*

### Setting up the platform
Remember that your platform will also need to be able to transmit the data between the Pico and the platform. I chose WiFi and Mosquitto for this, and you can read about that setup under "Transmitting the data/connectivity". Make sure to this step first.

First, set up your InfluxDB user by typing http://localhost:8086/ into your browser and following the instructions to create the initial user. You will get an API token, which is a long string of code containing letters, numbers, and special characters. Copy this entire code exactly and keep it for later. Copy all the credentials you used, as well as the Organization name (I used “School”) and the Initial Bucket name (I used “Aeroponics_monitoring”, don’t use blank spaces).

In Docker, import the Grafana, InfluxDB, and Telegraf images. This can be done either by code: `docker pull {image_name}` or by searching for the image and pulling it. Then, create a “docker-compose.yml” file and a “telegraf.conf” file, examples are available in the “Code” section. Make sure to update with your own user name, password, etc, from the previous step, as well as make up a user name and password for Grafana, and locate the credentials for you Mosquitto solution and IP address. I wrote the files in Notepad and placed them in a new folder under C:\Users\Isabelle\School project. Update this to reflect where you have placed your own files. Then, open that folder in Docker with the command: cd "C:\Users\..." before running the command “docker compose up -d” to build the stack. I had to do this several times before I got the entire stack working, using “docker command down” in between since I got errors for the telegraf file having an additional extension “txt” for example, and some coding errors, but eventually you should get something like this:

![image](https://hackmd.io/_uploads/BJbTnzEBlx.png)
*Figure 5: Print-screen of running containers.*

Next, you need to set up the InfluxDB plug-in in Grafana. Go to http://localhost:3000/ then to Connections/Add new connection and search for InfluxDB. Pick Query language “Flux” and add URL http://influxdb:8086. Also, add your InfluxDB credentials, and then click “Save and Test”. Click on "Build a dashboard" in the top right corner. See section “Presenting the data” for how to set up a Dashboard.

## The code
Initially, you will only have a main.py where you’ll run the main coding, and boot.py which will run each time the Pico is started, you should also have a file for all your credentials, make a new file on the Pico and name it “keys.py”, for example code of what you will need see the example-keys.py file under “Code”. I chose to have the code for the WiFi-connection in boot.py, and had to install a library-file (simple.py) for the Mosquitto MQTT solution, see how I set that up under “Transmitting the data/connectivity” and under “Code”. So for this project there is four files on the Pico: main.py, boot.py, keys.py and simple.py:

![image](https://hackmd.io/_uploads/r1V5jmEBeg.png)
*Figure 6: Screen-shot of Raspberry Pi Pico files in Thonny IDE.*

For complete code see the files under “Code”. We will first need to tell the Pico to collect all the information it will need to understand the code:
```
import machine                 #Always needed, the Pico is the machine
from machine import ADC, Pin   #For the machine to read Pin-data and data from analogue sensors
from time import sleep         #So we can tell the Pico to sleep
from dht import DHT11          #Needed to understand DHT11 data
from simple import MQTTClient  #added a umqtt-simple file, Pico refused to collect from umqtt.simple
import micropython             #Needed to run MicroPython code
import keys                    #For your credentials
```
I then had the code for connecting to the MQTT client before starting to define which Pin and name correspond to which module, an example of this:
```
#DHT11 sensor
ambientsensor = DHT11(Pin(22))
```
You will need code for how the Pico publishes data to the client for each topic, which, for brightness, including calculations to interpret the analog signal, looks like this:
```
#Function to publish bightness to MQTT broker
def publish_brightness(client):
    try:
        light = ldr.read_u16()
        brightness = 100-round(light / 65535 * 100, 1) #calculation to relate the analog signal to a percentage of light
        print("Publishing: Brightness: {}%".format(brightness))
        client.publish(keys.MQTT_TOPIC_LIGHT, b"%.2f" % brightness)
   except Exception as e:
       print(e) 
```
I also wrote a code section to change the LED light color based on temperature and humidity readings, so I get a visual indication of whether the thresholds are exceeded or not. This code is quite lengthy, so please look it up in the main.py file.
After all definitions and functions have been defined, you need your main loop where you tell the Pico what to do in a specific order:
```
try:
    connect_to_mqtt()  
    while True:
       try:
            ambientsensor.measure() #We need the first four lines to get the data for changing the LED
            temperature = ambientsensor.temperature()
            humidity = ambientsensor.humidity()
            check_ambient(temperature, humidity) #Will update the LED color
            publish_humidity(client) #Publish data according to the previous definition
            publish_temperature(client) #Publish data according to the previous definition
            publish_brightness(client) #Publish data according to the previous definition
        except Exception as error:
            print("Exception occurred", error) #We get an error if something goes wrong
        sleep(600) #then the Pico sleeps for 10 minutes before repeating the loop
```
Lastly, we tell the Pico how to shut down, to get a visual identification when the Pico is off, we also turn off the LED light:
```
finally: # ... disconnect the client and turn off LED
    client.disconnect()   
    client = None
    LED_Pin_Red.value(0)
    LED_Pin_Green.value(0)
    LED_Pin_Blue.value(0)
    print("Disconnected from MQTT.")
```

## Transmitting the data / connectivity
### Wireless connection
Wi-Fi was used for wireless since the aeroponics system will be stationary at home, well within range of the Wi-Fi and connected to wall power, so the extra power consumption is not a concern. Data was sent every minute during the testing phase. Since this resulted in 1440 datapoints per sensor per day, it felt excessive, and it was later minimized to once every 10 minutes (600 seconds) for a more reasonable 144 datapoints per day. This is to limit the amount of data for eventual future statistics, where, for example, light hours or temperature could be correlated to plant growth. Wi-Fi was set up in boot.py, see the complete code in the added file. When setting it up, make sure that you update all sections that say “#change” into your own usernames, passwords, IP address etc.

### Transport protocol
MQTT was used as a transport protocol. I pulled the Mosquitto image (“eclipse/mosquitto”) from the search bar in the Docker interface, named the container “mos1”, and followed [this guide](https://cedalo.com/blog/mosquitto-docker-configuration-ultimate-guide/) to set up the config file. Basically, I added a file for username and password in the MQTT client, restarted, and ran it. 

More detailed steps:
1. Pull image
2.	Run image on port 1883 with name “mos1”
3.	Type: `docker exec -it mos1 sh`
4.	Open mosquito.conf and add (e.g. on line 11 between all brackets): 
```
allow_anonymous true
listener 1883 0.0.0.0
```
5.	Enter mosquitto with: `docker exec -it -u 1883 mos1 sh`
a. Type: `mosquitto_passwd -c /mosquitto/passwd_file {your_username}` #change user name!! then Type: password then Type: password, again.
6.	Change mosquito.conf with:
```
password_file /mosquitto/passwd_file
allow_anonymous false
listener 1883 0.0.0.0
```

## Presenting the data
When new to Grafana I’d recommend downloading a finished dashboard and then altering it rather than trying to build it from scratch. I started out with this template: https://grafana.com/grafana/dashboards/16035-zero-weather/ and then changed it to what you see in Figure 9. When searching for templates, you can check “InfluxDB” as the source of data and then search for “temperature,” for example, to find good examples. You can then copy the JSON code of the dashboard and upload it to your own dashboard. For my code, see the file “ib222zz_grafana.json”. Note that you need to update this with the correct data source from your InfluxDB plug-in according to the following steps:
1.	Go to “Data Explore” in http://localhost:8086. If everything is working you pick the data series you want in your Dashboard like this: ![image](https://hackmd.io/_uploads/B1vmFZrHgx.png)
*Figure 7: A print-screen of how to get the JSON script for the data source.*
3.	And then click on “Script Editor” for the code. Copy this, then switch to Grafana where you add a dashboard and then a visualisation and add the code in the box for “queries”: 
![image](https://hackmd.io/_uploads/rkp4KbBSxl.png)	*Figure 8: A print-screen on how to add the JSON script to make a query in Grafana.*

The temperature and humidity section in my Grafana looks like this:
![image](https://hackmd.io/_uploads/Sk-CpdtBxx.png)
*Figure 9: A print-screen of a dashboard section from Grafana. Current and historic temperature and humidity readings, is shown. For temperature, cold climates will shift to blue, while too hot climates will shift to red. For humidity, we instead have yellow for too arid and blue for too humid. In both cases, optimal climates are green.*

The data is refreshed every 5 minutes to collect new data from InfluxDB where the data is stored. As mentioned before, I chose this solution over Adafruit due to its more inclusive free version, which offers scalability, additional visualization options, including data conversions, and a wider range of customization options. Another benefit is that InfluxDB stores data indefinitely, making it easy to download for further analysis. 

More alerts and automations can be added, but currently, I have an automation that changes the LED light according to temperature and humidity data, providing a visual indication of whether the climate for the plants is suitable or if adjustments are needed. A green light indicates that the temperature and humidity are within the thresholds, while it switches to red when the conditions are too hot or cold, or too dry or wet.

A comparison with the previous Adafruit dashboard is shown in Figure XX. I find the Grafana version more visually pleasing, likely because it was easy to adjust the format to look exactly how I wanted it. However, aside from that, it was also easier to set up the figures to provide more data, such as having all thresholds visible and represented by their own color, so we can immediately see how close a reading is to the thresholds. One positive aspect with Adafruit, however, was the ease with which you could set alerts and webhooks to post messages on Discord, for example.

![image](https://hackmd.io/_uploads/HkNxc-rBxx.png)
*Figure 10: An Adafruit dashboard showing current temperature, humidity, and light level, switching to red when thresholds are reached, as well as historical data over the last week.*

## Finalizing the design
Overall, it went better than I expected, considering I'm a chemist and find coding to be rather challenging. However, it was enjoyable to learn more about it, and in the end, I obtained a functioning device that I will continue to improve over the summer. Some improvements I’ve already planned:
•	Add alerts in either InfluxDB or Grafana so I can view text messages based on triggers in my data.
•	Sort out a container for all the tech, perhaps 3D-printed.
•	Determine a way to enhance the usefulness of the LDR sensor or replace it with a more accurate one, allowing for a more precise indication of sun hours and/or light intensity.
•	Add more sensors for the nutritional solution in the bucket, such as pH, TDS, and/or water level.
•	Add more automation based on the readings, like for example connecting an on/off switch to the fogger and controlling this based on humidity levels in the bucket.

![Light_red](https://hackmd.io/_uploads/rktDs-Srgl.png)
*Figure 11: Picture of the first test where I connected it to the wall power and placed it in the window for kitchen readings, the lamp is red because it was more than 27 degrees celsius.*

*More pictures and video demonstration will show up sometimes during the week. :>
