#import nxppy
import time

from threading import Thread

from flask import Flask

app = Flask(__name__)

records = {}

@app.route('/')
def start():
	return "test"

def monitor_records():
	global records
	mifare = nxppy.Mifare()
	print("Starting")
	while True:
		try:
			val = mifare.select()
			for i in range(64):
				print mifare.read_block(i)
		except Exception:
			pass
		time.sleep(1)

#monitor_records()
monitor = Thread(target = monitor_records)
#monitor.start()
app.run('0.0.0.0', 1337)
