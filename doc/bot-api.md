## Bot API

Bot API可以让服务号和用户互动。用户在服务号内发生动作时，币信服务器会向指定的Bot Callback地址发送用户的动作信息。第三方服务通过解析用户的动作行为，通过Bot API来和用户进行交互：回复文本、图片、选择事件、填写表单、广播图文等等。

## Bot初始化

在Vendor页面中可以查看到详细的Bot信息：

![image](https://raw.githubusercontent.com/haobtc/openplatform/master/images/bot_info_key.png)

Bot Access Token是和币信交互的凭证。
Bot AES Key和币信交互的数据加密Key。

创建一个Bot:

``` python

class Bot(object):
    def __init__(self, name=settings.APP_NAME,
                 bot_access_token=settings.BOT_ACCESS_TOKEN,
                 bot_aes_key=settings.BOT_AES_KEY):

        self.name = name
        self.bot_access_token = bot_access_token
        self.bot_aes_key = bot_aes_key

        self.pc = Prpcrypt(self.bot_aes_key)
        self.evt = None

bot = Bot()

```

[详细参考代码](./../lib/bixin/bot.py)


## 服务号 API列表 

[请参考](https://documenter.getpostman.com/view/2077000/6tc3iyY)
