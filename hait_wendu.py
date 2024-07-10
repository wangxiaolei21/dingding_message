from datetime import datetime, timezone, timedelta
import requests,json
# 定义UTC+8时区
tz_utc_8 = timezone(timedelta(hours=8))

url=r"https://oapi.dingtalk.com/robot/send?access_token=76b01a6c051e6fe73651c631158e6cd3b3ef948631be776c1a90b5d16d457bb3"
def get_message(xiaoxi:str, quantizhaohuan=0):
    tou={"Content-Type":"application/json; charset=utf-8"}
    neirong={"msgtype":"text",
             "text":{"content":xiaoxi},
             "at":{
                 "atMobiles":[],
                 "isAtAll":quantizhaohuan  #为1则@所有人
                   }
             }
    messagebody=json.dumps(neirong)
    print(messagebody)
    result=requests.post(url=url, data=messagebody,headers=tou)
    print(result.text)
      
# 获取东8区的当前日期和时间
now_utc_8 = datetime.now(tz_utc_8)
before_15fenzhong = now_utc_8 + timedelta(minutes=-15)

# 打印年月日
jieshu=now_utc_8.strftime('%Y-%m-%d %H:%M:%S')
kaishi=before_15fenzhong.strftime('%Y-%m-%d %H:%M:%S')

wangzhi="http://api.ubibot.cn/channels/5375/feeds?end="+jieshu+"&field=field1&" \
         "start="+kaishi+"&timezone=Asia/Shanghai&token_id=29309311ec0442938879a986409a4e69"
#print(wangzhi)
jieguo=requests.get(url=wangzhi).json()
if 'error' in jieguo.values():
    print(jieguo['errorCode']+":"+jieguo['desp'])
    print('每个小时最多只能获取数据5次')
    jg="每个小时最多只能获取数据5次"
else:
    for i in jieguo['feeds']:
        print(i['created_at'].split('+')[0].replace('T',' '), " %.1f℃"%i['field1'] )
        wendu="%.1f℃"%i['field1']
        jg="数据中心温度：%s (%s)"%(wendu,jieshu)
        print(jg)
get_message(jg,0)
