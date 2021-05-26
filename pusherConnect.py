import sys
import time
import pysher
#import logging
import json 
import os 
import PyQt5
import PyQt5.QtWidgets
import icueConnect
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
        #root = logging.getLogger()
        #root.setLevel(logging.INFO)
        #ch = logging.StreamHandler(sys.stdout)
        #root.addHandler(ch)
        #end logging
        global pusher_client
        global pusher_server
        pusher_server = pysher.Pusher(key=pusherKey, cluster=pusherCluster)
        pusher_server.connection.bind('pusher:connection_established', self.connect_handler)
        pusher_server.connect()
        pusher_client = pusher.Pusher(app_id=pusherID, key=pusherKey, secret=pusherSecret, cluster=pusherCluster)
        while True:
            # Do other things in the meantime here...
            time.sleep(1)

    def  my_func(self, *args, **kwargs):
        #print("processing Args:", args)
        #print("processing Kwargs:", kwargs)
        result = args[0]
        #print(result)
        result = json.loads(result)
        conn = icueConnect.icueConnect()
        conn.setPriority(255)#iCue's priority is 127
        if "RGB_PULSE" in result:
            RGB_val = result["RGB_PULSE"]
            conn.perform_pulse_effect(1000,RGB_val)
            conn.setPriority(0)
        elif "RGB_SOLID" in result:
            RGB_val = result["RGB_SOLID"]
            conn.solidColor(RGB_val)
        elif "RGB_RESET" in result:
            conn.setPriority(0)
        elif "Request_SubDevices" in result:
            print('Received From App')
            devices = conn.getDevicesIdMap()
            devices = str(devices)
            devices.encode()
            pusher_client.trigger(u'api_Callback', u'api_event', devices)
        del conn

    # We can't subscribe until we've connected, so we use a callback handler to subscribe when able
    def connect_handler(self, data):
        channel = pusher_server.subscribe('RGB_CONN')  # channel: RGB_CONN
        channel.bind('PULSE', self.my_func)            # event:   PULSE

"""
#example call
pusherConnect()
"""