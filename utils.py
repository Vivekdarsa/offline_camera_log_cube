from datetime import timedelta
import json
from api import add_log

def get_time_str(offline_since_time_obj):
    offline_since = ''
    if offline_since_time_obj.days > 0: 
        offline_since += str(offline_since_time_obj.days) + ' days'
    if offline_since_time_obj.seconds > 0: 
        time = str(timedelta(seconds=offline_since_time_obj.seconds)).split(':')
        if int(time[0]) > 0:
            if offline_since != '':
                offline_since += ', '
            offline_since += time[0] + ' hours'
        if int(time[1]) > 0:
            if offline_since != '':
                offline_since += ', '
            offline_since += time[1] + ' minutes'
    return offline_since


def add_offline_log(url, token, company, camera_id, sector, time_stamp):
    data = {
        "company": company,
        "camera_id": camera_id,
        "sector": sector,
        "time_stamp": time_stamp,
        "state": "offline"
    }
    add_log(url, token, data)
    return


def add_online_log(url, token, company, camera_id, sector, time_stamp):
    data = {
        "company": company,
        "camera_id": camera_id,
        "sector": sector,
        "time_stamp": time_stamp,
        "state": "online"
    }
    add_log(url, token, data)
    return


