import sys
import time
import pysher
import logging
import json
import jsonpickle
import os 
import PyQt5
import PyQt5.QtWidgets
import icueConnect
import helperGUI
import pusher


class pusherConnect:
    def __init__(self):
        if os.path.exists("./data.json"):
            with open('data.json', 'r') as openfile:
                json_object = json.load(openfile)
                pusherID = json_object["pusherAppID"]
                pusherKey = json_object["pusherKey"]
                pusherSecret = json_object["pusherSecret"]
                pusherCluster = json_object["pusherCluster"]
        #start a logging handler so we can see the raw communication data
        root = logging.getLogger()
        root.setLevel(logging.INFO)
        ch = logging.StreamHandler(sys.stdout)
        root.addHandler(ch)
        #end logging
        self.pusher_server = pysher.Pusher(key=pusherKey, cluster=pusherCluster)
        self.pusher_server.connection.bind('pusher:connection_established', self.__connect_handler)
        self.pusher_server.connect()
        try:
            self.pusher_client = pusher.Pusher(app_id=pusherID, key=pusherKey, secret=pusherSecret, cluster=pusherCluster)
        except ValueError as err:
            print("Pusher Connection Failed. Check Your Credentials!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        while True:
            # Do other things in the meantime here...
            time.sleep(1)

    def __my_func(self, *args, **kwargs):
        print("Processing Args:", args)
        #print("processing Kwargs:", kwargs)
        result = args[0]
        result = json.loads(result)
        conn = icueConnect.icueConnect()
        if "RGB_PULSE" in result:
            conn.requestControl()
            RGB_val = result["RGB_PULSE"]
            conn.perform_pulse_effect(1000,RGB_val)
            conn.releaseControl()
        elif "RGB_SOLID" in result:
            conn.requestControl()
            RGB_val = result["RGB_SOLID"]
            RGB_DEVICE = result["RGB_DEVICE"][0]
            if RGB_DEVICE == 0:
                conn.solidColor(RGB_val)
            else:
                conn.setLedsByDevice((RGB_DEVICE-1), RGB_val)
        elif "RGB_RESET" in result:
            conn.releaseControl()
        elif "Request_SubDevices" in result:
            devices = conn.getDevicesIdMap()
            devices = jsonpickle.encode(devices, unpicklable=False)
            print(f"Connected Devices: {devices}")
            self.pusher_client.trigger(u'api_Callback', u'api_event', devices)
        else:
            print(f"Unknown Request:\n{result}")
        del conn

    # We can't subscribe until we've connected, so we use a callback handler to subscribe when able
    def __connect_handler(self, data):
        channel = self.pusher_server.subscribe('RGB_CONN')  # channel: RGB_CONN
        channel.bind('PULSE', self.__my_func)               # event:   PULSE

"""
#example call
pusherConnect()
"""