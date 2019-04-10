import hashlib
import time
import requests
import property


def translate(query, fromLanguage='auto', toLanguage='zh'):
    urlBaiduTranslate = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    propBaidu = property.parse('config.properties')
    appid = propBaidu.get('APP_ID')
    sk = propBaidu.get('SECURITY_KEY')
    salt = int(round(time.time() * 1000))
    src = appid + query + str(salt) + sk
    m2 = hashlib.md5()
    m2.update(src.encode('utf-8'))
    try:
        responseBaidu = requests.get(urlBaiduTranslate,
                                     {
                                         'q': query,
                                         'from': fromLanguage,
                                         'to': toLanguage,
                                         'appid': appid,
                                         'salt': salt,
                                         'sign': m2.hexdigest()
                                     })
        json = responseBaidu.json()
        print(json)
    except Exception as err:
        print('Error Msg')
        print(err)
        s_open = open('log.txt', 'a+')
        s_open.write("\n\n" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "\n" + str(err) + "\n")
        s_open.close()
        return '错误:' + str(err)
    return json


def getTranslateValue(query, fromLanguage='auto', toLanguage='zh'):
    res = translate(query, fromLanguage, toLanguage)
    if 'error_code' in res:
        return str(res)
    elif '错误:' in res:
        return str(res)
    else:
        return res['trans_result'][0]['dst']
