from firebase import Collection

from flask import Flask, request
from flask_cors import CORS

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

CORS(app)

readings_list = []
command_id: str = ""


@app.before_first_request
def light_thread():
    def run():
        global light_on, readings_list

        while True:
            if light_on:
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
                readings_list.append(reading)
                time.sleep(0.1)

    thread = threading.Thread(target=run)
    thread.start()


@app.route("/", methods=['GET', 'POST'])
def index():
    global light_on
    if request.method == "POST":
        if light_on:
            return "", 400
        else:
            return start(request.get_json().get("command_id"))
    else:
        if not light_on:
            return "", 400
        else:
            return stop()


def start(cmd):
    """
    Begins recording of gryo data to the global readings_list
    """
    global readings_list, light_on, command_id
    command_id = cmd
    readings_list = []
    light_on = True
    return "", 201


def stop():
    """
    End recording and upload attempt to subcollection for command
    """
    global light_on, readings_list
    light_on = False
    gyro_data = readings_list
    collection = Collection()
    a = collection.create_sub(command_id, gyro_data)
    print("collection response", a)
    return a


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
