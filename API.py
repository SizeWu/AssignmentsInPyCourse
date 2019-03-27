#!/usr/bin/python
import json
import urllib
from urllib import request
import urllib.parse


# ----------------------------------
# 从聚合数据获取合肥的天气信息
# ----------------------------------


def main():
    # 配置APPKey，在聚合网上申请到的
    appkey = "58e310dfad9690582a36720694b356f0"

    datadict = request1(appkey)  # 请求：默认GET，获取天气信息,将需要的信息写入这个字典
    print(datadict)


# 根据城市查询天气
def request1(appkey, m="GET", city='合肥'):
    datadict = {'today':                                           # 定义一个字典，用于获取需要的信息
                    {'date': '', 'week': '', 'lunar': '', 'pm25': '',
                     'dawn': {'weather': '', 'temp': '', 'wind': ''},
                     'day': {'weather': '', 'temp': '', 'wind': ''},
                     'night': {'weather': '', 'temp': '', 'wind': ''}
                     },
                'tomorrow':
                    {'date': '', 'week': '', 'lunar': '', 'pm25': '',
                     'dawn': {'weather': '', 'temp': '', 'wind': ''},
                     'day': {'weather': '', 'temp': '', 'wind': ''},
                     'night': {'weather': '', 'temp': '', 'wind': ''}
                     }
                }
    url = "http://op.juhe.cn/onebox/weather/query"
    params = {
        "cityname": city,   # 查询合肥的天气
        "key": appkey,      # 应用APPKEY
        "dtype": "json",    # 返回数据的格式为json
    }
    params = urllib.parse.urlencode(params)  # 将params编码
    if m == "GET":
        f = urllib.request.urlopen("%s?%s" % (url, params))  # url为打开的网址，params为提交的数据
    else:
        f = urllib.request.urlopen(url, params)

    content = f.read()
    res = json.loads(content)  # res为字典，信息太多，需要挑选一些
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            print('成功请求')
            i = 0
            for key in datadict.keys():
                datadict[key]['date'] = res['result']['data']['weather'][i]['date']
                datadict[key]['week'] = res['result']['data']['weather'][i]['week']
                datadict[key]['lunar'] = res['result']['data']['weather'][i]['nongli']
                for key1 in ['dawn', 'day', 'night']:
                    datadict[key][key1]['weather'] = res['result']['data']['weather'][i]['info'][key1][1]
                    datadict[key][key1]['temp'] = res['result']['data']['weather'][i]['info'][key1][2]
                    datadict[key][key1]['wind'] = res['result']['data']['weather'][i]['info'][key1][3]
                i += 1
            datadict['today']['pm25'] = res['result']['data']['pm25']['pm25']['pm25']
            datadict['tomorrow']['pm25'] = '无数据'
            datadict['city'] = city

            # print(res.keys())  #以下为测试时用的代码
            # print(res['result'].keys())
            # print(res['result']['data'].keys())
            # print('pm2.5', res['result']['data']['pm25'])
            # print(res['result']['data']['weather'][0])
            # print(res['result']['data']['weather'][1])
            # print(res['result']['data']['life'])
            # print(res["reason"])
            # print(res['result']['data']['realtime'].keys())
        else:
            print("%s:%s" % (res["error_code"], res["reason"]))
    else:
        print("request api error")
    return datadict







