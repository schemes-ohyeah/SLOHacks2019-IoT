from firebase import Collection

from flask import Flask
from flask import request

app = Flask(__name__)

collection = Collection()

@app.route("/", methods=['GET', 'POST']))
def index():
    print("let's do gyroscope stuff lululul")
    print("done let's upload this stuff to google hahaha")
    if request.method == 'POST':
        # begin recording
        'command_id' = request.values.get('command_id')
    else:
        # end recording and upload attempt to subcollection for command
        # gyro_data = some_recording
        # collection.create_sub(command_id, gyro_data)
        collection.dataup()
    return "Hello world!"

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)