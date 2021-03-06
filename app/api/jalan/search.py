import requests
import json

from bs4 import BeautifulSoup
from datetime import datetime

from .location import global_to_japan, japan_to_global
from .config import JALAN_API_KEY as key
from ..google.geometry import get_distance

url = "http://jws.jalan.net/APIAdvance/StockSearch/V1/"

def _parse_to_plans(text):
    soup = BeautifulSoup(text, "lxml")

    ret = []

    for plan in soup.find_all("plan"):
        ret.append(plan)

    return ret


def get_hotel_stocks(hotel_id):
    stock_serach_url = "http://jws.jalan.net/APIAdvance/StockSearch/V1/"

    now = datetime.now()

    stay_date = now.strftime("%Y%m%d")

    q = {
        "key": key,
        "h_id": hotel_id,
        "stay_date": "20161001"
    }

    req = requests.get(stock_serach_url, params=q)

    soup = BeautifulSoup(req.text, "lxml")
    if soup.find("numberofresults").text == "0":
        return None

    if soup.find("stock").text == "":
        return 11
    else:
        return soup.find("stock").text


def extract_stockless_hotels(objects):
    indexed = set()
    ret = list()

    for obj in objects:
        id = obj["hotelid"]
        num = get_hotel_stocks(id)
        if num:
            obj["stock"] = num
            ret.append(obj)

    return ret

def get_plans(wx, wy, range=1):
    wx = float(wx)
    wy = float(wy)

    mjx, mjy = global_to_japan(wx, wy)

    q = {
        "key": key,
        "x": mjx,
        "y": mjy,
        "range": range,
        "count": 100
    }

    res = requests.get(url, params=q)

    plans = _parse_to_plans(res.text)

    objects = plans_to_objects(plans)

    objects = extract_deplicated_hotels(objects)

    for obj in objects:
        x = obj["x"]
        y = obj["y"]

        distance = get_distance(wx, wy, x, y)
        obj["distance"] = distance["distance"]
        obj["duration"] = distance["duration"]

    objects.sort(key=lambda o: o["distance"])

    objects = extract_stockless_hotels(objects)

    return json.dumps(objects)


def _extract_from_plan(plan, obj, s):
    try:
        obj[s] = plan.find(s).text
    except:
        obj[s] = ""


def extract_deplicated_hotels(objects):
    indexed = set()
    ret = list()

    for obj in objects:
        hotelname = obj["hotelname"]
        if hotelname in indexed:
            pass
        else:
            indexed.add(hotelname)
            ret.append(obj)

    return ret


def plans_to_objects(plans):
    objects = []

    for plan in plans:
        obj = dict()
        _extract_from_plan(plan, obj, "planname")
        _extract_from_plan(plan, obj, "plancd")
        _extract_from_plan(plan, obj, "roomname")
        _extract_from_plan(plan, obj, "roomcd")
        _extract_from_plan(plan, obj, "plandetailurl")
        _extract_from_plan(plan, obj, "plancommondetailurl")
        _extract_from_plan(plan, obj, "plancheckin")
        _extract_from_plan(plan, obj, "plancheckout")
        _extract_from_plan(plan, obj, "splyperiodstrday")
        _extract_from_plan(plan, obj, "splyperiodendday")
        _extract_from_plan(plan, obj, "planpictureurl")
        _extract_from_plan(plan, obj, "planpicturecaption")
        _extract_from_plan(plan, obj, "meal")
        _extract_from_plan(plan, obj, "ratetype")
        _extract_from_plan(plan, obj, "samplerate")
        _extract_from_plan(plan, obj, "servicechangerate")
        _extract_from_plan(plan, obj, "hotelid")
        _extract_from_plan(plan, obj, "hotelname")
        _extract_from_plan(plan, obj, "postcode")
        _extract_from_plan(plan, obj, "hoteladdress")
        _extract_from_plan(plan, obj, "area")
        _extract_from_plan(plan, obj, "region")
        _extract_from_plan(plan, obj, "prefecture")
        _extract_from_plan(plan, obj, "largearea")
        _extract_from_plan(plan, obj, "smallarea")
        _extract_from_plan(plan, obj, "hoteltype")
        _extract_from_plan(plan, obj, "hoteldetailurl")
        _extract_from_plan(plan, obj, "hotelcatchcopy")
        _extract_from_plan(plan, obj, "hotelcaption")
        _extract_from_plan(plan, obj, "pictureurl")
        _extract_from_plan(plan, obj, "picturecaption")
        _extract_from_plan(plan, obj, "x")
        _extract_from_plan(plan, obj, "y")
        _extract_from_plan(plan, obj, "hotelnamekana")
        _extract_from_plan(plan, obj, "numberofratings")
        _extract_from_plan(plan, obj, "rating")

        _x = int(obj["x"])
        _y = int(obj["y"])
        obj["x"], obj["y"] = japan_to_global(_x, _y)

        obj["facilities"] = []
        for facility in plan.find_all("facility"):
            obj["facilities"].append(facility.text)
        objects.append(obj)

    return objects
