### 签名

签名过程：

1. 使用vendor的access_token访问[https://bixin.im/platform/api/v1/ticket/jsapi](https://bixin.im/platform/api/v1/ticket/jsapi)获得jssdk_ticket（有效期7200秒）。

2. 将nonce, timestamp, jssdk_ticket, callback_url拼接起来获得签名。拼接时，首先对这四个参数进行字典排序，然后使用url键值对的格式将参数拼接成字符串（key_1=value_1&key_2=value_2...），参数名均为小写。最后使用SHA1对生成的字符串进行加密，即可获得认证所需要的签名。

签名代码示例

'''
import hashlib
import urllib

def create_signature(**kw):
    params = sorted(kw.items())
    url_encode = urllib.urlencode(params)

    h = hashlib.sha1()
    h.update(url_encode)
    sig = h.hexdigest()
    return sig

signature = create_signature(
    nonce='CgQLBgEA',
    timestamp=1499394832,
    jssdk_ticket='c1b9a4461e1c7574e4bd6c2e0d343c81d7e142b5',
    url='https://my.app.im/callback'
)

 ```

### 代码demo

[参考](https://github.com/haobtc/openplatform/blob/master/openplatform/servicer/views.py#L34-L41)
