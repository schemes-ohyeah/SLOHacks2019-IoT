from firebase import Collection

from flask import Flask
from flask import request

import mraa
import time
import threading

x = mraa.I2c(0)
x.address(0x6B)
time.sleep(0.01)
x.writeReg(0x22, 0x05)

print(x.readReg(0x0F))
x.writeReg(0x10, 0xC0)

light_on = False

app = Flask(__name__)

collection = Collection()

readings_list = []

@app.before_first_request
def light_thread():
    def run():
        global light_on
        while light_on:
            x_lsb = x.readReg(0x18)
            x_msb = x.readReg(0x19)
            x_final = (x_msb << 8) | x_lsb
            y_lsb = x.readReg(0x1A)
            y_msb = x.readReg(0x1B)
            y_final = (y_msb << 8) | y_lsb
            z_lsb = x.readReg(0x1C)
            z_msb = x.readReg(0x1D)
            z_final = (z_msb << 8) | z_lsb
            reading = (round(x_final * 0.00875, 3), round(y_final * 0.00875, 3), round(z_final * 0.00875, 3))
            global readings_list
            readings_list.append(reading)
            time.sleep(0.1)

    thread = threading.Thread(target=run)
    thread.start()

@app.route("/", methods=['GET', 'POST'])
def index():
    print("let's do gyroscope stuff lululul")
    print("done let's upload this stuff to google hahaha")
    #if request.method == 'POST':
    #    # begin recording
    #    global readings_list
    #    readings_list = []
    #    global light_on
    #    light_on = True
    #    command_id = request.values.get('command_id')
    #else:
    #    # end recording and upload attempt to subcollection for command
    #    global light_on
    #    light_on = False
    #    gyro_data = readings_list
    #    print(gyro_data)
    #    # collection.create_sub(command_id, gyro_data)
    return "Hello world!"

@app.route("/start")
def start():
    global readings_list
    readings_list = []
    global light_on
    light_on = True

@app.route("/stop")
def stop():
    global light_on
    light_on = False
    gyro_data = readings_list
    return gyro_data

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
