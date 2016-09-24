import requests
import json
from bs4 import BeautifulSoup

from .location import global_to_japan
from .config import JALAN_API_KEY as key

url = "http://jws.jalan.net/APIAdvance/StockSearch/V1/"

def _parse_to_plans(text):
    soup = BeautifulSoup(text, "lxml")

    ret = []

    for plan in soup.find_all("plan"):
        ret.append(plan)

    return ret


def get_plans(wx, wy, range=1):
    wx = float(wx)
    wy = float(wy)

    mjx, mjy = global_to_japan(wx, wy)

    q = {
        "key": key,
        "x": mjx,
        "y": mjy,
        "range": range
    }

    res = requests.get(url, params=q)

    plans = _parse_to_plans(res.text)

    return plans_to_json(plans)

def plans_to_json(plans):
    objects = []

    for plan in plans:
        obj = dict()
        obj["planname"] = plan.find("planname").text
        obj["roomname"] = plan.find("roomname").text
        obj["facilities"] = []
        for facility in plan.find_all("facility"):
            obj["facilities"].append(facility.text)
        objects.append(obj)

    return json.dumps(objects, indent=4)