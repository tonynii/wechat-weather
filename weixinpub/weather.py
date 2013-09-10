#!/usr/bin/env python
# coding=utf-8

import urllib2
import json

import public.applogging as logging
import public.config as config

api_key = config.API_KEY['wunderground']

geolookup_url ='http://api.wunderground.com/api/%s/geolookup/lang:CN/q/%s,%s.json'
forecast_url = 'http://api.wunderground.com/api/%s/forecast/lang:%s/q/%s,%s.json'

class Weather(object):
    
    def __init__(self):
        pass
    
    def getweatherbydegree (self, longitude, latitude):
        #url_geo = geolookup_url % (api_key, latitude, longitude)
        #geo_rep = urllib2.urlopen(url_geo)
        #geo_string = geo_rep.read()
        #geo_rep.close()
        #geo_json = json.loads(geo_string)
        #logging.debug(geo_json)
        #if 'error' in geo_json['response']:
        #    logging.error(geo_json)
        #    return "查询位置失败(1)，请重试！"
        #try:
        #    country_iso3166 = geo_json['location']['country_iso3166']
        #    city = geo_json['location']['city']
        #except:
        #    logging.exception(geo_json)
        #    return "查询位置失败(2)，请重试！"
        
        url_forecast =forecast_url % (api_key, 'CN', latitude, longitude)
        forecast_rep = urllib2.urlopen(url_forecast)
        forecast_string = forecast_rep.read()
        forecast_rep.close()
        forecast_json = json.loads(forecast_string)
        if 'error' in forecast_json['response']:
            logging.error(forecast_json)
            return "查询位置失败(3)，请重试！"
        try:
            forecast_date = forecast_json['forecast']['txt_forecast']['date']
        except:
            logging.exception(forecast_json)
            return "查询天气失败(4)，请重试！"
        ret_str = []
        for i in range(0,6):
            icon_url = forecast_json['forecast']['txt_forecast']['forecastday'][i]['icon_url']
            title = forecast_json['forecast']['txt_forecast']['forecastday'][i]['title']
            fcttext = forecast_json['forecast']['txt_forecast']['forecastday'][i]['fcttext_metric']
            ret_str.append([title,fcttext,icon_url])
        return ret_str
        #return "您所在区域天气如下:\n\n%s\n发布时间: %s\n数据来自: The Weather Channel" % (city.encode('utf-8'),ret_str.encode('utf-8'), forecast_date.encode('utf-8'))
        
    
if __name__ == '__main__':
    x = Weather()
    #113.358803 23.134521
    print x.getweatherbydegree(32.040000,118.780000)
    
    ##f = urllib2.urlopen('http://api.wunderground.com/api/085a81c8e61e5d5f/geolookup/conditions/lang:CN/q/IA/Cedar_Rapids.json')
    #f = urllib2.urlopen('http://api.wunderground.com/api/085a81c8e61e5d5f/geolookup/lang:CN/q/32.040000,118.780000.json')
    #url = forecast_url % (api_key, 'CN', 'Xiaolingwei')
    ##f = urllib2.urlopen('http://api.wunderground.com/api/085a81c8e61e5d5f/forecast/lang:CN/q/CN/Xiaolingwei.json')
    ##f = urllib2.urlopen(url)
    #json_string = f.read()
    #print(json_string)
    #parsed_json = json.loads(json_string)
    #location = parsed_json['location']['country_iso3166']
    #temp_f = parsed_json['location']['city']
    #print "Current temperature in %s is: %s" % (location.encode('utf-8'), temp_f.encode('utf-8'))
    #f.close()
