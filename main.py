import time
import json
import nxppy
import picamera
from subprocess import Popen
from threading import Thread
from flask import Flask, request, send_from_directory
from os import path

app = Flask(__name__)
camera = picamera.PiCamera()

records = [ 
    {"id": 0, "url": "/assets/img_0.jpg"}        
]

data = {
    "0": "Zach's Card"     
}

currentProc = None

@app.route('/')
def start():
    return send_from_directory("client", "index.html")

@app.route('/js/<file_name>')
def send_js (file_name):
    return send_from_directory("client/js", file_name)


@app.route('/css/<file_name>')
def send_css (file_name):
    return send_from_directory("client/css", file_name)


@app.route('/assets/<file_name>')
def send_asset (file_name):
    return send_from_directory("assets", file_name)


@app.route('/data')
def send_data():
    return json.dumps(records)

@app.route('/add')
def add_figure():
    global records, data, camera
    mifare = nxppy.Mifare()
    print("Starting")
    while True:
        try:
            val = mifare.select()
            value = ""
            for i in range(64):
                try:
                    value += mifare.read_block(i)
                except Exception:
                    break
            time.sleep(1)
            name = path.join("assets", "img_{}.jpg".format(len(records)))
            camera.capture(name)
            data[str(len(records))] = value 
            records.append({"id": len(records), "url": name})
            return ""
        except Exception as e:
            print (e)
            pass
        time.sleep(1)
    time.sleep(4)

@app.route('/emu/<id_name>')
def start_emulation(id_name):
    global currentProc
    if currentProc is not None:
        currentProc.kill()
        currentProc = None
    try:
            currentProc = Popen(["explorenfc-cardemulation", "-t", data[id_name]]) 
    except Exception:
        pass
    return ""

@app.route('/cancel')
def stop_emulation():
    global currentProc
    if currentProc is not None:
        currentProc.kill()
    return ""

if __name__ == "__main__":
    app.run("0.0.0.0", 1337)
