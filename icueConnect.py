from cuesdk import CueSdk
from pprint import pprint
from inspect import getmembers
import time

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

    def setPriority(self,value):
        sdk.set_layer_priority(value)

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
