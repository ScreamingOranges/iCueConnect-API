import sys
import time
import pysher
#import logging
import json 
import os 
import PyQt5
import PyQt5.QtWidgets
import icueConnect

class pusherConnect:
    def __init__(self):
        if(os.path.exists("./data.json")):
            with open('data.json', 'r') as openfile:
                json_object = json.load(openfile)
                pusherKey = json_object["pusherKey"]
        # Add a logging handler so we can see the raw communication data
        #root = logging.getLogger()
        #root.setLevel(logging.INFO)
        #ch = logging.StreamHandler(sys.stdout)
        #root.addHandler(ch)
        global pusher
        pusher = pysher.Pusher(pusherKey)
        pusher.connection.bind('pusher:connection_established', self.connect_handler)
        pusher.connect()
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
        del conn

    # We can't subscribe until we've connected, so we use a callback handler to subscribe when able
    def connect_handler(self, data):
        channel = pusher.subscribe('RGB_CONN')  # channel: RGB_CONN
        channel.bind('PULSE', self.my_func)          # event:   PULSE


#pusherConnect()