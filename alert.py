from datetime import datetime, timedelta
import json
from dateutil import parser
from pytz import timezone
from time import sleep
from threading import Thread

from api import get_cameras, get_sectors, get_floors, get_facilities
from utils import add_offline_log, add_online_log


class OfflineAlert(Thread):
    def __init__(self, conf_data, url, token):
        Thread.__init__(self)
        
        self.conf_data = conf_data
        self.conf_data['url'] = url
        self.conf_data['token'] = token

        self.sectors_dict = {}
        self.floors_dict = {}
        self.facilities_dict = {}
    
    def get_facility_name_from_sector(self, sector):
        try:
            return self.facilities_dict[self.floors_dict[self.sectors_dict[sector]['floor']]['facility']]['facility_name']
        except Exception as e:
            return None
    
    def get_facility_id_from_sector(self, sector):
        try:
            return self.facilities_dict[self.floors_dict[self.sectors_dict[sector]['floor']]['facility']]['id']
        except Exception as e:
            return None

    def run(self):

        sectors = get_sectors(self.conf_data['url'], self.conf_data['token'])
        for sector in sectors:
            self.sectors_dict[sector['id']] = sector

        floors = get_floors(self.conf_data['url'], self.conf_data['token'])
        for floor in floors:
            self.floors_dict[floor['id']] = floor
        
        facilities = get_facilities(self.conf_data['url'], self.conf_data['token'])
        for facility in facilities:
            self.facilities_dict[facility['id']] = facility

        offline_cam_dict = {}
        cam_status_dict = {}
    
        while True:
            
            cameras = get_cameras(self.conf_data['url'], self.conf_data['token'])
            for cam in cameras:
                if cam['active'] and \
                    cam['preview_time'] != None and \
                    cam['sector'] != None and \
                    len(cam['modes']) > 0 and \
                    cam['modes'][0]['mode'] in self.conf_data['modes'] and \
                    self.get_facility_id_from_sector(cam['sector']) in self.conf_data['facilities']:
                        
                    utc_time_obj = parser.isoparse(cam['preview_time'])
                    last_preview_time = utc_time_obj.astimezone(timezone('Asia/Kolkata')).replace(tzinfo=None)
                    if (datetime.now() - last_preview_time).total_seconds() > 15*60:
                        if cam['camera_id'] not in offline_cam_dict:
                            offline_cam_dict[cam['camera_id']] = {'name':cam['name'], 'last_online': last_preview_time, 'mailing_status':False, 'sector': cam['sector']}
                            print('adding offline log', datetime.now(), self.conf_data['company_name'])
                            add_offline_log(self.conf_data['url'], self.conf_data['token'], self.conf_data['company'], cam['camera_id'], cam['sector'], cam['preview_time'])
                        if cam['camera_id'] not in cam_status_dict:
                            cam_status_dict[cam['camera_id']] = {'name':cam['name'], 'status':[{'last_online': last_preview_time, 'status': 'offline'}]}
                        else:
                            cam_status_dict[cam['camera_id']]['status'].append({'last_online': last_preview_time, 'status': 'offline'})
                    else:
                        if cam['camera_id'] in offline_cam_dict:
                            offline_cam_dict.pop(cam['camera_id'])
                            print('adding online log', datetime.now(), self.conf_data['company_name'])
                            add_online_log(self.conf_data['url'], self.conf_data['token'], self.conf_data['company'], cam['camera_id'], cam['sector'], cam['preview_time'])
                        if cam['camera_id'] not in cam_status_dict:
                            cam_status_dict[cam['camera_id']] = {'name':cam['name'], 'status':[{'last_online': last_preview_time, 'status': 'online'}]}
                        else:
                            cam_status_dict[cam['camera_id']]['status'].append({'last_online': last_preview_time, 'status': 'online'})


            sleep(900)




