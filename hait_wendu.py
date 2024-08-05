from datetime import datetime, timezone, timedelta
import requests, json
import hashlib


def sha256_hash(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def get_token(user, pwd):
    login_url = r"https://api.ubibot.cn/accounts/login"
    shuju = {
        "expire_in_seconds": "2592000",
        "password": sha256_hash(pwd),
        "password_type": "sha256",
        "username": user
    }
    jieguo = requests.post(url=login_url, data=shuju).json()
    print("token_id:", jieguo['token_id'])
    print("过期时间:", jieguo['expire_time'])
    return jieguo['token_id']


def send_message(xiaoxi: str, quantizhaohuan=0):
    dingding_url = r"https://oapi.dingtalk.com/robot/send?access_token=76b01a6c051e6fe73651c631158e6cd3b3ef948631be776c1a90b5d16d457bb3"
    tou = {"Content-Type": "application/json; charset=utf-8"}
    neirong = {"msgtype": "text",
               "text": {"content": xiaoxi},
               "at": {
                   "atMobiles": [],
                   "isAtAll": quantizhaohuan  # 为1则@所有人
               }
               }
    messagebody = json.dumps(neirong)
    print(messagebody)
    result = requests.post(url=dingding_url, data=messagebody, headers=tou)
    print(result.text)


def make_message(token: str):
    # 定义UTC+8时区
    tz_utc_8 = timezone(timedelta(hours=8))
    # 获取东8区的当前日期和时间
    now_utc_8 = datetime.now(tz_utc_8)
    before_15fenzhong = now_utc_8 + timedelta(minutes=-15)

    # 打印年月日
    jieshu = now_utc_8.strftime('%Y-%m-%d %H:%M:%S')
    kaishi = before_15fenzhong.strftime('%Y-%m-%d %H:%M:%S')

    wangzhi = "http://api.ubibot.cn/channels/5375/feeds?end=" + jieshu + "&field=field1&" \
                                                                         "start=" + kaishi + "&timezone=Asia/Shanghai&token_id=" + token
    print(wangzhi)
    jieguo = requests.get(url=wangzhi).json()
    jg = "未能成功获取到温度数据。 "+jieshu
    if 'error' in jieguo.values():
        print(jieguo['errorCode'] + ":" + jieguo['desp'])
        print('每个小时最多只能获取数据5次')
        jg = "每个小时最多只能获取数据5次"
    else:
        for i in jieguo['feeds']:
            print(i['created_at'].split('+')[0].replace('T', ' '), " %.1f℃" % i['field1'])
            wendu = "%.1f℃" % i['field1']
            jg = "数据中心温度：%s (%s)" % (wendu, jieshu)
            print(jg)
    send_message(jg, 0)


if __name__ == '__main__':
    yonghuming = "zhenweiw@qq.com"
    mima = "jkxjkx309"
    token = get_token(yonghuming, mima)
    make_message(token)
