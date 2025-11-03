# home_assistant
Code and design relating to home assistant devices
Code in yaml providing coded access to a facility controlled, in this case a front door,  by home assistant
There some schematics and pcb desing for wifi node based on esp8266 in the desing floder
The outsidefront_1.yaml code resides in the esp8266 (esphome module)  whose schematic is given the design folder
unlock_front_door_1.yaml is an home assistant automation which is trigged by a simple script
The python code is a an cut down version of python called SNAP that runs is a  Synapse Wireless https://www.synapsewireless.com/  
model SM700 or SM200 it receives and sends commands via 9600 baud UART (UART1 in HAcontrol31.py )
SW modles are now defunct and are replaced by RF220 and SM220 see https://abrupt-sheathbill.files.svdcdn.com/production/uploads/Synapse-Core-IoT-Platform-Flyer_v4-2.pdf
