import time

from flask import Flask
app = Flask(__name__)


@app.route("/")
def index():
    print("let's do gyroscope stuff lululul")
    time.sleep(3)
    print("done let's upload this stuff to google hahaha")
    return "Hello world!"


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
