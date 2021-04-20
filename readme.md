"""
ONLY THESE PACKAGE VERSIONS WORKED
pip install --force-reinstall websocket-client==0.48.0
pusher                      3.0.0    
Pysher                      1.0.3
six                         1.15.0

JSON EXAMPLE
{"RGB_SOLID":[0,0,0]}
"""


pyinstaller main.py --clean --win-private-assemblies -n iCueConnect --log-level=DEBUG -w -F -p "C:\Users\danie\AppData\Local\Programs\Python\Python38\Lib\site-packages" --add-data "C:\Users\danie\AppData\Local\Programs\Python\Python38\Lib\site-packages\cuesdk;cuesdk" --add-data "E:\PersonalProjects\iCUE Connect\iCuePyPhoneSERVER\icon.png;iCuePyPhoneSERVER" --icon="E:\PersonalProjects\iCUE Connect\iCuePyPhoneSERVER\icon.ico" 