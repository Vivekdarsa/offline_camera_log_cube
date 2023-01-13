from datetime import datetime, timedelta
import json
from dateutil import parser
from pytz import timezone
from time import sleep

from api import get_cameras, get_sectors, get_floors, get_facilities
from gmail import send_mail
from html_mail_body import html_str
from utils import get_time_str

offline_cam_dict = {}
cam_status_dict = {}

with open('config.json','r') as conf_file:
    conf_data = json.load(conf_file)

sectors_dict = {}
floors_dict = {}
facilities_dict = {}

for client, data in conf_data.items():
    sectors = get_sectors(data['url'], data['token'])
    for sector in sectors:
        sectors_dict[sector['id']] = sector

    floors = get_floors(data['url'], data['token'])
    for floor in floors:
        floors_dict[floor['id']] = floor

    facilities = get_facilities(data['url'], data['token'])
    for facility in facilities:
        facilities_dict[facility['id']] = facility


def get_facility_from_sector(sector):
    return facilities_dict[floors_dict[sectors_dict[sector]['floor']]['facility']]['facility_name']


while True:
    # for client, data in conf_data.items():
    #     if client not in offline_cam_dict:
    #         offline_cam_dict[client] = {}

    #     if client not in cam_status_dict:
    #         cam_status_dict[client] = {}

        cameras = get_cameras(data['url'], data['token'])
        for cam in cameras:
            if cam['active'] and cam['preview_time'] != None:
                utc_time_obj = parser.isoparse(cam['preview_time'])
                last_preview_time = utc_time_obj.astimezone(timezone('Asia/Kolkata')).replace(tzinfo=None)
                if (datetime.now() - last_preview_time).total_seconds() > 15*60:
                    if cam['camera_id'] not in offline_cam_dict[client]:
                        offline_cam_dict[client][cam['camera_id']] = {'name':cam['name'], 'last_online': last_preview_time, 'mailing_status':False, 'sector': cam['sector']}
                    if cam['camera_id'] not in cam_status_dict[client]:
                        cam_status_dict[client][cam['camera_id']] = {'name':cam['name'], 'status':[{'last_online': last_preview_time, 'status': 'offline'}]}
                    else:
                        cam_status_dict[client][cam['camera_id']]['status'].append({'last_online': last_preview_time, 'status': 'offline'})
                else:
                    if cam['camera_id'] in offline_cam_dict[client]:
                        offline_cam_dict[client].pop(cam['camera_id'])
                    if cam['camera_id'] not in cam_status_dict[client]:
                        cam_status_dict[client][cam['camera_id']] = {'name':cam['name'], 'status':[{'last_online': last_preview_time, 'status': 'online'}]}
                    else:
                        cam_status_dict[client][cam['camera_id']]['status'].append({'last_online': last_preview_time, 'status': 'online'})


    print('**********', datetime.now())
    # for client, cams in offline_cam_dict.items():
        # mail_str = ''
        # for cam, cam_data in cams.items():
            # if cam_data['mailing_status'] is False:
                # print(cam_data['name'], cam_data['mailing_status'])
                # mail_str += cam_data['name'] + '\n'
                # cam_data['mailing_status'] = True
        # if mail_str != '':
            # print('sending mail to', client, datetime.now())
            # print(mail_str)
            # send_mail(mail_str, conf_data[client]['mail_address'])

    # for client, cams in offline_cam_dict.items():
    #     mail_str = ''
    #     for cam, cam_data in cams.items():
    #         offline_since = (datetime.now() - cam_data['last_online']).total_seconds()/3600
    #         mail_str += cam_data['name'] + ' offline since ' + str(int(offline_since)) + ' hours' +'\n'
    #     if mail_str != '':
    #         print('sending mail to', client, datetime.now())
    #         # print(mail_str)
    #         send_mail(mail_str + fixed_mail_footer, client, conf_data[client])

    for client, cams in offline_cam_dict.items():
        table_data = ''
        for cam, cam_data in cams.items():
            offline_since_time_obj = datetime.now() - cam_data['last_online']
            offline_since = get_time_str(offline_since_time_obj)
            table_data += '<tr><td style="border: 1px solid orange">{0}</td> \
                            <td style="border: 1px solid orange">{1}</td> \
                            <td style="border: 1px solid orange">{2}</td></tr>' \
                            .format(cam_data['name'], get_facility_from_sector(cam_data['sector']), (offline_since))
        if table_data != '':
            print('sending mail to', client, datetime.now())
            # send_mail(html_str(table_data), client, conf_data[client])

    test_data = cam_status_dict['APS']
    if datetime.now() >= datetime(2022,1,30, 9,30):
        test_dict = {}
        for cam, cam_data in test_data.items():
                cam_ = cam
                a = []
                b = []
                for status in cam_data['status']:
                    if status['status'] == 'online':
                        a.append(status['last_online'])
                    else:
                        if len(a)>0:
                            b.append([a[0], a[-1]])
                        a = []
                if len(a)>1:
                    b.append([a[0], a[-1]])

        test_dict[cam_] = {'data':b}
        print(test_dict[cam_]);exit()
        with open("sample.json", "w") as outfile:
            json.dump(test_dict, outfile)
    
    print(a)

    sleep(15*60)



