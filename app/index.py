from flask import Flask
from flask import request
from api.jalan.search import get_plans
app = Flask(__name__)

@app.route("/api/v1/")
def hello():
    wx = request.args.get("x", "")
    wy = request.args.get("y", "")
    if wx or wy:
        return get_plans(wx, wy)
    return "bad request"

if __name__ == "__main__":
    app.run()