from flask import Flask
from flask import request
import json
from api.google.geometry import get_distance
from api.jalan.search import get_plans, get_hotel_stocks
app = Flask(__name__)

@app.route("/api/v1/hotels")
def hello():
    wx = request.args.get("x", "")
    wy = request.args.get("y", "")
    human = request.args.get("human", False)
    if wx or wy:
        if human:
            return str(json.loads(get_plans(wx, wy)))
        else:
            return get_plans(wx, wy)
    return "bad request"


@app.route("/api/v1/dia")
def dia():
    return json.dumps({"status": "not implemented"})


@app.route("/")
def good():
    return "thanks"


if __name__ == "__main__":
    app.debug = True
    app.run()