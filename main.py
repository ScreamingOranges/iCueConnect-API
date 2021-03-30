from cuesdk import CueSdk
from pprint import pprint
from inspect import getmembers
import sys, getopt
import time
import pysher
import websocket
import logging
import json 

"""
ONLY THESE PACKAGE VERSIONS WORKED
pip install --force-reinstall websocket-client==0.48.0
pusher                      3.0.0    
Pysher                      1.0.3
six                         1.15.0

JSON EXAMPLE
{"RGB_SOLID":[0,0,0]}
"""


class icueConnect:
    def get_available_leds(self):
        leds = list()
        device_count = sdk.get_device_count()
        for device_index in range(device_count):
            led_positions = sdk.get_led_positions_by_device_index(device_index)
            leds.append(led_positions)
            dev = sdk.get_device_info(device_index)
            #print(dev.__dict__['model'])
            #print(type(dev.__dict__['model']))
            #pprint(getmembers(dev))
            if dev.__dict__['model'] == 'Lighting Node Pro' and dev.__dict__['led_count'] == 76:
                self.ll120s = device_index
        return leds

    def perform_pulse_effect(self,wave_duration,RGB_val):
        time_per_frame = 25
        x = 0
        cnt = len(all_leds)
        dx = time_per_frame / wave_duration
        while x < 2:
            val_R = int((1 - (x - 1)**2) * int(RGB_val[0]))
            val_G = int((1 - (x - 1)**2) * int(RGB_val[1]))
            val_B = int((1 - (x - 1)**2) * int(RGB_val[2]))
            for di in range(cnt):
                device_leds = all_leds[di]
                for led in device_leds:
                    device_leds[led] = (val_R, val_G, val_B)
                sdk.set_led_colors_buffer_by_device_index(di, device_leds)
            sdk.set_led_colors_flush_buffer()
            time.sleep(time_per_frame / 1000)
            x += dx
        time.sleep(.05)

    def solidColor(self,RGB_val):
        cnt = len(all_leds)
        for di in range(cnt):
            device_leds = all_leds[di]
            for led in device_leds:
                #print(led)
                device_leds[led] = (RGB_val[0],RGB_val[1],RGB_val[2])
            sdk.set_led_colors_buffer_by_device_index(di, device_leds)
        sdk.set_led_colors_flush_buffer()

    def __init__(self):
        global sdk
        global all_leds
        global devices
        sdk = CueSdk()
        connected = sdk.connect()
        if not connected:
            err = sdk.get_last_error()
            print("Handshake failed: %s" % err)
            return
        devices = sdk.get_devices()
        #print(devices)
        all_leds = self.get_available_leds()
        if not all_leds:
            return      


# Add a logging handler so we can see the raw communication data
root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
root.addHandler(ch)
pusher = pysher.Pusher("3b584ee38d8b91d475cd")

def  my_func(*args, **kwargs):
    print("processing Args:", args)
    #print("processing Kwargs:", kwargs)
    result = args[0]
    print(result)
    result = json.loads(result)
    conn = icueConnect()
    sdk.set_layer_priority(255)#iCue's priority is 127
    if "RGB_PULSE" in result:
        RGB_val = result["RGB_PULSE"]
        conn.perform_pulse_effect(1000,RGB_val)
        sdk.set_layer_priority(0)
    elif "RGB_SOLID" in result:
        RGB_val = result["RGB_SOLID"]
        conn.solidColor(RGB_val)
    del conn

# We can't subscribe until we've connected, so we use a callback handler
# to subscribe when able
def connect_handler(data):
    channel = pusher.subscribe('RGB_CONN')  # channel: RGB_CONN
    channel.bind('PULSE', my_func)          # PULSE:   PULSE

pusher.connection.bind('pusher:connection_established', connect_handler)
pusher.connect()

while True:
    # Do other things in the meantime here...
    time.sleep(1)