from flask import Flask
from flask import request
import json
from api.jalan.search import get_plans
app = Flask(__name__)

@app.route("/api/v1/")
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

if __name__ == "__main__":
    app.run()