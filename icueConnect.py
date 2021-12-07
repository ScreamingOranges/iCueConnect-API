import cuesdk
import time

class icueConnect:
    def __get_available_leds(self):
        leds = list()
        device_count = self.__sdk.get_device_count()
        for device_index in range(device_count):
            led_positions = self.__sdk.get_led_positions_by_device_index(device_index)
            leds.append(led_positions)
            self.__deviceToLed[device_index] = led_positions
            dev = self.__sdk.get_device_info(device_index)
        return leds

    #returns a dictionary. key=channelDevice.type & value=list of leds in channelDevices in channel
    #example output: subDevices = {"LL_Fan": [16, 16, 16, 16], "HD_Fan": [12]}
    def getSubDevices(self, device):
        devInfo = self.__sdk.get_device_info(device)
        channelDevices = {}
        for channel in devInfo.channels:
            cDevices = []
            devName = ""
            for cDevice in channel.devices:
                cDevices.append(cDevice.led_count)
                devName = str(cDevice.type).replace("CorsairChannelDeviceType.","")
            if devName in channelDevices.keys():
                devName = devName + "2"
                channelDevices[devName] = cDevices
            else:
                channelDevices[devName] = cDevices
        return channelDevices

    def setSubDeviceLeds(self, device, subDevice, RGB_val):
        devInfo = self.__sdk.get_device_info(device)
        channelLeds = {}
        for channel in devInfo.channels:
            devName = ""
            ledCount = 0
            for cDevice in channel.devices:
                devName = str(cDevice.type).replace("CorsairChannelDeviceType.","")
                ledCount = ledCount + cDevice.led_count
            if devName in channelLeds.keys():
                devName = devName + "2"
                channelLeds[devName] = ledCount
            else:
                channelLeds[devName] = ledCount

        if len(devInfo.channels) > 1:
            cIndex = list(channelLeds.keys()).index(subDevice)+1
            cIndex = "C"+str(cIndex)
            for led in self.__deviceToLed[device]:
                if cIndex in str(led):
                    self.__deviceToLed[device][led] = (RGB_val[0],RGB_val[1],RGB_val[2])
        else:
            for led in self.__deviceToLed[device]:
                self.__deviceToLed[device][led] = (RGB_val[0],RGB_val[1],RGB_val[2])
        self.__sdk.set_led_colors_buffer_by_device_index(device, self.__deviceToLed[device])
        self.__sdk.set_led_colors_flush_buffer()

    def getDeviceInfo(self,device):
        return self.__sdk.get_device_info(device)

    def getDevicesIdMap(self):
        deviceMap = {}
        devices = self.__sdk.get_devices()
        for device in range(len(devices)):
            deviceMap[device] = devices[device].model
        return deviceMap

    def setLedsByDevice(self, device,RGB_val):
        for led in self.__deviceToLed[device]:
            self.__deviceToLed[device][led] = (RGB_val[0],RGB_val[1],RGB_val[2])
        self.__sdk.set_led_colors_buffer_by_device_index(device, self.__deviceToLed[device])
        self.__sdk.set_led_colors_flush_buffer()

    def requestControl(self):
        self.__sdk.request_control()

    def releaseControl(self):
        self.__sdk.release_control()

    def perform_pulse_effect(self,wave_duration,RGB_val):
        time_per_frame = 25
        x = 0
        cnt = len(self.__all_leds)
        dx = time_per_frame / wave_duration
        while x < 2:
            val_R = int((1 - (x - 1)**2) * int(RGB_val[0]))
            val_G = int((1 - (x - 1)**2) * int(RGB_val[1]))
            val_B = int((1 - (x - 1)**2) * int(RGB_val[2]))
            for di in range(cnt):
                device_leds = self.__all_leds[di]
                for led in device_leds:
                    device_leds[led] = (val_R, val_G, val_B)
                self.__sdk.set_led_colors_buffer_by_device_index(di, device_leds)
            self.__sdk.set_led_colors_flush_buffer()
            time.sleep(time_per_frame / 1000)
            x += dx
        time.sleep(.05)

    def solidColor(self,RGB_val):
        cnt = len(self.__all_leds)
        for di in range(cnt):
            device_leds = self.__all_leds[di]
            for led in device_leds:
                #print(led)
                device_leds[led] = (RGB_val[0],RGB_val[1],RGB_val[2])
            self.__sdk.set_led_colors_buffer_by_device_index(di, device_leds)
        self.__sdk.set_led_colors_flush_buffer()

    def delayedSolidColor(self, interval,RGB_val):
        cnt = len(self.__all_leds)
        for di in range(cnt):
            device_leds = self.__all_leds[di]
            for led in device_leds:
                device_leds[led] = (RGB_val[0],RGB_val[1],RGB_val[2])
                time.sleep(interval)
                self.__sdk.set_led_colors_buffer_by_device_index(di, device_leds)
                self.__sdk.set_led_colors_flush_buffer()

    def __init__(self):
        self.__deviceToLed = {}
        self.__devicesIdMap = {}
        self.__sdk = cuesdk.CueSdk()
        connected = self.__sdk.connect()
        if not connected:
            err = self.__sdk.get_last_error()
            print("Handshake failed: %s" % err)
            return
        self.__all_leds = self.__get_available_leds()
        self.__devicesIdMap = self.getDevicesIdMap()
        if not self.__all_leds:
            return      


##example call##
#conn = icueConnect()
#red = [255,0,0]
#green = [0,255,0]
#blue = [0,0,255]
#devices = conn.getDevicesIdMap()
#
#
##print id to device mapping
#for key in range(len(devices)):
#    print("ID:"+str(key)+" | Device:"+str(devices[key]))
#conn.solidColor(red)
#
#
#device = input("Choose device By ID:")
#conn.setLedsByDevice(int(device),green)
#
#
#subDevices = conn.getSubDevices(int(device))
#for subDevice, ledCount in subDevices.items():
#    print(subDevice+" |", ledCount)
#subDevice = input("Enter subDevice Name:")
#conn.setSubDeviceLeds(int(device), subDevice, blue)
#input("Press Any Key To Exit..")
#del conn
