import requests,json
import math
#! https://restapi.amap.com/v4/ip?key=8599324053ca7fd6b1245e997b45dd12&ip=60.208.131.66
key="8599324053ca7fd6b1245e997b45dd12"


def qqMapTransBMap(lng, lat):
    x_pi = 3.14159265358979324 * 3000.0 / 180.0
    x=lng
    y = lat
    z = math.sqrt(x * x + y * y) + 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) + 0.000003 * math.cos(x * x_pi)
    lngs = z * math.cos(theta) + 0.0065
    lats = z * math.sin(theta) + 0.006
    result={"lng":lngs,"lat":lats}
    return result

def ipAddress(ip):
    ip_address=ip
    if ip_address !='': 
        data={"key":key,"ip":ip_address}
        url="https://restapi.amap.com/v4/ip"
        location_res=requests.get(url=url,params=data)
        #? location_json=location_res.text
        location_json=json.loads(location_res.text)
        print (location_json)
        if location_json['errcode']==0:
            #{'data': {'pcd': {'city': '杭州市', 'cityCode': '330100', 'county': '拱墅区', 'countyCode': '330105', 'province': '浙江省', 'provinceCode': '330000'}, 'lng': 120.16142, 'confidence': 1.0, 'source': 'IPPredict', 'time': '2019-07-22 16:15:27', 'lat': 30.2936}, 'errcode': 0, 'errdetail': None, 'errmsg': 'OK', 'ext': None}
            lng=location_json['data']['lng']
            lat=location_json['data']['lat']
            city=location_json['data']['pcd']['city']
            county=location_json['data']['pcd']['county']
            province=location_json['data']['pcd']['province']
            time=location_json['data']['time']
            #print (location)
            gd_location={"地址":province+city+county,"纬度":lng,"经度":lat,"更新时间":time}
            gd_url="https://uri.amap.com/marker?position=%f,%f"%(lng,lat)
            bd_location=qqMapTransBMap(lng,lat)
            bd_url="http://api.map.baidu.com/geocoder?location=%f,%f&coord_type=bd09ll&output=html&src=webapp.baidu.openAPIdemo"%(bd_location["lat"],bd_location["lng"])
            #http://api.map.baidu.com/geocoder?location=30,120&coord_type=gcj02&output=html&src=webapp.baidu.openAPIdemo
            return "定位结果: "+str(gd_location)+'\n'+'点击查看具体位置(高德地图):\n'+"%s"%(gd_url)+"\n"+"点击查看具体位置(百度地图):\n"+"%s"%(bd_url)
        else:
            return '查询无效(数据库无此ip/ip地址不合法/非中国ip地址/操你妈又瞎j8输数据不会用别nm用)'
    else:
        return "不输ip地址你查你🐴呢?"
