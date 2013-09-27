#!/usr/bin/env python
# coding=utf-8

import urllib, urllib2
import json

import public.applogging as logging


class GeoCoding(object):
    #'''wiki:https://developers.google.com/maps/documentation/geocoding/?hl=zh-CN&csw=1#GeocodingRequests'''
    def __init__(self, key = ' '):
        self.url_para = {'address': '', 
                 'sensor': 'false',
                 'language': 'zh-CN'}
        self.url = 'http://maps.googleapis.com/maps/api/geocode/json'
        self.geo_info_list = []
        
    def get_latlng_by_name(self, geo_name):
        '''利用google map api从网上获取city的经纬度。'''
        self.url_para['address'] = geo_name.encode('utf-8')
        arguments = urllib.urlencode(self.url_para)
        url_get_geo = self.url + '?' + arguments
        handler = urllib2.urlopen(url_get_geo)
        resp_data = handler.read()
        handler.close()
        st = self.parse_ret_json(resp_data)
        return self.geo_info_list

    def parse_ret_json(self, ret_str):
        '''
         解析从API上获取的XML数据。
        '''
        parse_st = False
        city_1 = ''
        city_2 = ''
        ret_json = json.loads(ret_str)
        if ret_json['status'] == 'OK':
            #get lat lng and addr
            for geo_info in ret_json['results']:
                #print(geo_info)
                geo_dict = {'lat': geo_info['geometry']['location']['lat'],
                            'lng': geo_info['geometry']['location']['lng'],
                            'addr': geo_info['formatted_address'],
                            'city':'',
                            'state_province':'',
                            'country':'',
                            'types': geo_info['types']}
                #get city state_provine country
                for addr_comp in geo_info['address_components']:
                    if 'country' in addr_comp['types']: 
                        geo_dict['country'] = addr_comp['long_name']
                    elif 'administrative_area_level_1' in addr_comp['types']:
                        geo_dict['state_province'] = addr_comp['long_name']
                    elif 'locality' in addr_comp['types'] or \
                         'administrative_area_level_2' in addr_comp['types']:
                        city_1 = addr_comp['long_name']
                    elif 'sublocality' in addr_comp['types'] or \
                         'administrative_area_level_3' in addr_comp['types']:
                        city_2 = addr_comp['long_name']
                    if city_2 != '':
                        geo_dict['city'] = city_2
                    else:
                        geo_dict['city'] = city_1
                self.geo_info_list.append(geo_dict) 
            parse_st = True
            logging.info(u'get geo info is: {0}'.format(self.geo_info_list))
        else:
            parse_st = False 
            logging.warning(u'return status if {0}'.format(ret_json['status']))
        return parse_st


if __name__ == '__main__':
    geo = GeoCoding()
    geo.get_latlng_by_name('南京')