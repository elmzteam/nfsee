import time
import json
from subprocess import Popen
from threading import Thread
from flask import Flask, request, send_from_directory
from os import path

app = Flask(__name__)

records = [ 
    {"id": 1, "url": "/assets/img_1.jpg"}        
]

data = {
    "1": "Zach's Card"     
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
    import nxppy
    import picamera
    camera = picamera.PiCamera()
    global records, data
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
            records.push({"id": len(records), url: name})
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
