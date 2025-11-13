'''
 demonstrating HolyIOT button press
 with a specific address
 
 for mfg_id, resp_data in result.manufacturer():
                #print(f"MAC:{result.device.addr_hex()} MFG_ID:{mfg_id} MFG_DATA:{mfg_data}")
                print(f"MFG_ID:{mfg_id} MFG_DATA:{mfg_data}")
                ##print(' * ')
'''

import aioble
import asyncio
import time
import machine
ver ="ble_switch3.py 111125"
Led = machine.Pin(15,machine.Pin.OUT)
Light = machine.Pin(18,machine.Pin.OUT)

sw_state = True
async def scan():
    global sw_state
    # adjust duration_ms, interval_ window_us for optimum response
    async with aioble.scan(30000, interval_us=30000, window_us=30000, active=True) as scanner:
        async for result in scanner:
            #print(result.resp_data)
            if len(result.resp_data) > 4 and result.resp_data[1] == 9:
                address = result.device
                #print (result.device, result.resp_data[29])
                if address.addr.hex() == "e50a330c2d32" :
                    if result.resp_data[29] == 1:
                      time.sleep(0.08)  # switch bounce
                      if sw_state:
                          Light.on()
                          Led.off()
                          print("on")
                      else:
                        Led.on()
                        Light.off()
                        print("off")
                      sw_state = sw_state ^ True
                        
                
            

while True:
    asyncio.run(scan())
    time.sleep(0.3)