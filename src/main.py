from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    x = "Hello World!"
    return x


if __name__ == "__main__":
    app.run(debug=True)
