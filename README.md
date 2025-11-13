# home_assistant
Code and design relating to home assistant devices
Code in yaml providing coded access to a facility controlled, in this case a front door,  by home assistant
There some schematics and pcb desing for wifi node based on esp8266 in the design folder
The outsidefront_1.yaml code resides in the esp8266 (esphome module)  whose schematic is given the design folder
unlock_front_door_1.yaml is an home assistant automation which is trigged by a simple script
The python code is a an cut down version of python called SNAP that runs in a  Synapse Wireless https://www.synapsewireless.com/  
model SM700 or SM200. It receives and sends commands via 9600 baud UART (UART1 in HAcontrol31.py )
SW modles are now defunct and are replaced by RF220 and SM220 see https://abrupt-sheathbill.files.svdcdn.com/production/uploads/Synapse-Core-IoT-Platform-Flyer_v4-2.pdf

Further experiment revealed that the ble scan in the esp32c6 yaml file  in ble_ibeacon/lightSwitch04.yaml  was found to be unreliable and required the beacon to be scanning continuously.
The battery lifetime for a CR3032 cell in the iBeacon, ~300mAhr, would only provide a maximum of 40 days.  The beacon was then modified such that a push-button supplied power to the beacon to advertise its ble data.  This extends the battery liftetime to well over a year  Secondly the scanning receiver was moved to separate ESP32C6 which processed the detection and switched a GPIO pin on another ESP8266 module to swich the light on.  This allows the light to be controlled centrally and locally.

Although combersome  it simplifies the switch detection procedure.

Depencies for ble_switch3.py running in ESP32C6 are aioble and asyncio
