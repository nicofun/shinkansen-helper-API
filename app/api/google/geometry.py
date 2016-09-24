import requests
import json
import sys

from .config import GOOGLE_API_KEY as key

url = "https://maps.googleapis.com/maps/api/distancematrix/json"

def get_distance(ox, oy, dx, dy):
    q = {
        "key": key,
        "origins": "{},{}".format(ox, oy),
        "destinations": "{},{}".format(dx, dy),
        "mode": "walking"
    }

    ret = requests.get(url, params=q)
    obj = json.loads(ret.text)

    ret = dict()
    try:
        ret["distance"] = obj["rows"][0]["elements"][0]["distance"]["value"]
        ret["duration"] = obj["rows"][0]["elements"][0]["duration"]["value"]
    except:
        print("Geometry Parse Error", file=sys.stderr)

    return ret

if __name__ == "__main__":
    get_distance("41.773767", "140.726450", "41.77717972917574", "140.72969903531035")