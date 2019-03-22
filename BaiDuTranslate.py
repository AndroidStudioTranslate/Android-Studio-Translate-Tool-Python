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
    responseBaidu = requests.get(urlBaiduTranslate,
                                 {
                                     'q': query,
                                     'from': fromLanguage,
                                     'to': toLanguage,
                                     'appid': appid,
                                     'salt': salt,
                                     'sign': m2.hexdigest()
                                 })
    return responseBaidu.json()


def getTranslateValue(query, fromLanguage='auto', toLanguage='zh'):
    return translate(query, fromLanguage, toLanguage)['trans_result'][0]['dst']
