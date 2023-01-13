import requests
import json

def get_cameras(url, token):
    headers = {'content-type': 'application/json',
               'Authorization': 'Token ' + token}
    request_url = "{0}/api/camera".format(url)
    response = requests.get(request_url, headers=headers)
    return response.json()


def get_sectors(url, token):
    headers = {'content-type': 'application/json',
               'Authorization': 'Token ' + token}
    request_url = "{0}/api/sector".format(url)
    response = requests.get(request_url, headers=headers)
    return response.json()


def get_floors(url, token):
    headers = {'content-type': 'application/json',
               'Authorization': 'Token ' + token}
    request_url = "{0}/api/floor".format(url)
    response = requests.get(request_url, headers=headers)
    return response.json()


def get_facilities(url, token):
    headers = {'content-type': 'application/json',
               'Authorization': 'Token ' + token}
    request_url = "{0}/api/facility".format(url)
    response = requests.get(request_url, headers=headers)
    return response.json()


def get_client_list(url, token):
    headers = {'content-type': 'application/json',
               'Authorization': 'Token ' + token}
    request_url = "{0}/api/offline_camera_email_config_all".format(url)
    response = requests.get(request_url, headers=headers)
    return response.json()


def add_log(url, token, data):
    headers = {'content-type': 'application/json',
               'Authorization': 'Token ' + token}
    request_url = "{0}/api/log/camera/".format(url)
    json_data = json.dumps(data)
    response = requests.post(request_url, headers=headers, data=json_data)
    return response


def get_token(url, data):
    request_url = "{0}/api/auth/token/login/".format(url)
    response = requests.post(request_url, data=data)
    return response.json()