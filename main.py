import network
import urequests
import time
import ntptime
import ujson
import machine

# Config

SSID = "iPhone (Mateusz)"
PASSWORD = "12345678"
ENDPOINT = "http://srv3.enteam.pl:3012/insert"
INTERVAL = 1

# App


def info(*message):
    output = ""
    for msg in message:
        output += str(msg)
    print("[INFO] " + output)


info("Starting Propane and LPG Detector")
info("Authors: Mateusz Woźniak, Maciej Pawłowski")

wifi = network.WLAN(network.STA_IF)
if not wifi.isconnected():
    print("connecting to network...")
    wifi.active(True)
    wifi.connect(SSID, PASSWORD)
    while not wifi.isconnected():
        pass

info("Connected to WIFI. Network config: ", wifi.ifconfig())

try:
    ntptime.settime()
except Exception as e:
    print(e)
    machine.reset()
    
info("Time synchronized: ", time.localtime())

def insert(propane_level, ammonia_level):
    timestamp = time.time()
    post_data = ujson.dumps({
        "propane_level": propane_level,
        "ammonia_level": ammonia_level,
        "measured_at": timestamp,
    })
    info("Sending data: ", post_data)
    res = urequests.post(ENDPOINT, headers={"content-type": "application/json"}, data=post_data).json()

# insert(36, 11)

def read_propane_level():
    return 37

def read_ammonia_level():
    return 42

info("Starting main loop with interval: ", INTERVAL)

while True:
    try:
        insert(read_propane_level(), read_ammonia_level())
    except Exception as e:
        print(e)
    time.sleep(INTERVAL)
    if not wifi.isconnected():
        machine.reset()
