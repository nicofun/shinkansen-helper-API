import requests
import json
import datetime

def get_dia():

    dia = {
        "weekday": [
            (6, 35),
            (7, 34),
            (9, 31),
            (10, 49),
            (12, 44),
            (13, 35),
            (14, 44),
            (15, 35),
            (16, 17),
            (17, 21),
            (18, 36),
            (19, 37),
            (20, 39),
            (21, 59)
        ],
        "sunday": [
            (6, 35),
            (7, 34),
            (9, 31),
            (10, 49),
            (12, 44),
            (13, 35),
            (14, 44),
            (15, 35),
            (16, 17),
            (17, 21),
            (18, 36),
            (19, 37),
            (20, 39),
            (21, 59)
        ]
    }
    now = datetime.datetime.now()
    if now.weekday() == 5:
        return {}
    elif now.weekday() == 6:
        return dia["sunday"]
    else:
        return dia["weekday"]

def get_next_shinkansen_time():
    dia = get_dia()
    now = datetime.datetime.now()
    for time in sorted(dia, key=lambda k: k[0]):
        shin_time = datetime.datetime(now.year, now.month, now.day, time[0], time[1])
        sa = (shin_time - datetime.datetime.now()).total_seconds()
        print("{}:{}".format(time[0], time[1]))
        if sa > 0:
            return "{}:{}".format(time[0], time[1])


def main():
    print("yes we can.")
    return get_next_shinkansen_time()