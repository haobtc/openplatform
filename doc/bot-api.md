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

## API

### 文本消息

Content-Type: application/x-www-form-urlencoded

```
POST https://openapi.bixin.im/api/v2/bot.postText
```

参数：

| 名称(name) | 描述(description) |
| --------- | ----------------- |
| target_id | 发送对象的id|
| text | 发送文本 |
| request_id | 请求消息id 用uuid生成 |

返回：

```json
{
	"ok": true,
	"data": {
		"created_at": "2017-07-07T03:08:59.871191",
		"content_type": "text",
		"content": {
			"text": "text"
		},
		"sender": {
			"name": "bot_test",
			"nickname": "Ghost bot",
			"avatar_url": "https://openapi.bixin.im/res/vendor_fin_dollar2.png",
			"gender": "",
			"menu": [{
				"icon_url": "https://openapi.bixin.im/res/faq.png",
				"desc": "Test",
				"action": "bixin://postevent?event=index_view&text=Test&target_id=f2c5609ae91c4a2ab20c4b196aac9b4a&conv_type=bot"
			}],
			"btc_address": "1Har9AL8QyRuQ5DiLfm6kFndscbVR6ctHG",
			"desc": "Bixin Official Service",
			"id": "f2c5609ae91c4a2ab20c4b196aac9b4a",
			"conv_type": "bot"
		},
		"brief": "text",
		"request_id": "a573e676casa44259dc0ee29087adea23",
		"prev_id": 9363,
		"receiver": {
			"name": "echo",
			"nickname": "12555",
			"avatar_url": "https://openapi.bixin.im/upload/2017/05/11/6146c20c214745f3b29b73216fe47fd1.png",
			"gender": "male",
			"menu": [],
			"btc_address": "1vkJV6bnJdbjocerXjLJkc3tEsjmEjh94",
			"desc": "",
			"id": "a573e67b760a44259dc0ee29087ade72",
			"conv_type": "private"
		},
		"id": 9364,
		"is_mute": false,
		"conv_type": "bot"
	}
}
```
### 图片消息

Content-Type: multipart/form-data

```
POST https://openapi.bixin.im/api/v2/bot.postImage
```

参数：

| 名称(name) | 描述(description) |
| --------- | ----------------- |
| target_id | 发送对象的id|
| request_id | 请求消息id 用uuid生成 |
| conv_type | 会话类型, 可选[private,group] |
| file | image文件 |

返回：

```
{
	"ok": true,
	"data": {
		"content_type": "image",
		"conv_type": "bot",
		"sender": {
			"nickname": "Ghost bot",
			"avatar_url": "https://openapi.bixin.im/res/vendor_fin_dollar2.png",
			"conv_type": "bot",
			"name": "bot_test",
			"id": "f2c5609ae91c4a2ab20c4b196aac9b4a",
			"btc_address": "1Har9AL8QyRuQ5DiLfm6kFndscbVR6ctHG",
			"gender": "",
			"menu": [{
				"icon_url": "https://openapi.bixin.im/res/faq.png",
				"desc": "Test",
				"action": "bixin://postevent?event=index_view&text=Test&target_id=f2c5609ae91c4a2ab20c4b196aac9b4a&conv_type=bot"
			}],
			"desc": "Bixin Official Service"
		},
		"id": 10560,
		"request_id": "a1273e67b760a44259dc0ee29087ade722",
		"content": {
			"image_url": "https://openapi.bixin.im/upload/2017/07/07/a75955a4165e4b5990ea9559ce794f94.png",
			"image_height": 768,
			"thumb_height": 112,
			"thumb_url": "https://openapi.bixin.im/upload/2017/07/07/a75955a4165e4b5990ea9559ce794f94.png",
			"thumb_width": 200,
			"image_width": 1366
		},
		"prev_id": 10558,
		"receiver": {
			"nickname": "Echo",
			"avatar_url": "https://openapi.bixin.im/upload/2017/07/07/1adf8b1675e84435aa5e3c6a2202a825.png",
			"conv_type": "private",
			"name": "echo",
			"id": "a573e67b760a44259dc0ee29087ade72",
			"btc_address": "1vkJV6bnJdbjocerXjLJkc3tEsjmEjh94",
			"gender": "male",
			"menu": [],
			"desc": ""
		},
		"brief": "Image",
		"created_at": "2017-07-07T08:18:45.487664",
		"is_mute": false
	}
}
```
### select 消息

Content-Type: application/json

```
POST https://openapi.bixin.im/api/v2/bot.postSelect
```

参数：

| 名称(name) | 描述(description) |
| --------- | ----------------- |
| target_id | 发送对象的id|
| request_id | 请求消息id 用uuid生成 |
| conv_type | 会话类型, 可选[private,group] |
| text | 发送文本 |
| select | 消息内容为数组[{'desc': '', 'image_url': '', 'image_width': '', 'image_height': '', 'action': ''}] |

返回：

```
{
	"ok": true,
	"data": {
		"created_at": "2017-07-07T03:51:23.330868",
		"content_type": "select",
		"content": {
			"text": "text",
			"select": [{
					"desc": "desc",
					"image_url": "image_url",
					"image_width": "image_width",
					"image_height": "image_height",
					"action": "bixin://postevent/?target_id=f2c5609ae91c4a2ab20c4b196aac9b4a&conv_type=bot&text=desc&event=action"
				},
				{
					"desc": "desc2",
					"image_url": "imgae_url2",
					"image_width": "image_width2",
					"image_height": "image_height2",
					"action": "bixin://postevent/?target_id=f2c5609ae91c4a2ab20c4b196aac9b4a&conv_type=bot&text=desc2&event=action2"
				}
			]
		},
		"sender": {
			"name": "bot_test",
			"nickname": "Ghost bot",
			"avatar_url": "https://openapi.bixin.im/res/vendor_fin_dollar2.png",
			"gender": "",
			"menu": [{
				"icon_url": "https://openapi.bixin.im/res/faq.png",
				"desc": "Test",
				"action": "bixin://postevent?event=index_view&text=Test&target_id=f2c5609ae91c4a2ab20c4b196aac9b4a&conv_type=bot"
			}],
			"btc_address": "1Har9AL8QyRuQ5DiLfm6kFndscbVR6ctHG",
			"desc": "Bixin Official Service",
			"id": "f2c5609ae91c4a2ab20c4b196aac9b4a",
			"conv_type": "bot"
		},
		"brief": "text",
		"request_id": "a573a17a0asess251dc0ee29087adea23",
		"prev_id": 9369,
		"receiver": {
			"name": "echo",
			"nickname": "12555",
			"avatar_url": "https://openapi.bixin.im/upload/2017/05/11/6146c20c214745f3b29b73216fe47fd1.png",
			"gender": "male",
			"menu": [],
			"btc_address": "1vkJV6bnJdbjocerXjLJkc3tEsjmEjh94",
			"desc": "",
			"id": "a573e67b760a44259dc0ee29087ade72",
			"conv_type": "private"
		},
		"id": 9370,
		"is_mute": false,
		"conv_type": "bot"
	}
}
```

### 文章消息

Content-Type: application/x-www-form-urlencoded

```
POST https://openapi.bixin.im/api/v2/bot.postArticle
```

参数：

| 名称(name) | 描述(description) |
| --------- | ----------------- |
| target_id | 发送对象的id|
| request_id | 请求消息id 用uuid生成 |
| conv_type | 会话类型, 可选[private,group] |
| title | artilce 消息标题 |
| desc | artilce 消息标描述 |
| image_url | 背景图片url |
| action | 跳转连接或者 event |

返回：

```
{
	"ok": true,
	"data": {
		"created_at": "2017-07-07T03:35:44.246799",
		"content_type": "article",
		"content": {
			"desc": "desc描述",
			"image_url": "https://bixin.im/static/images/logo_scroll@2x.21af7c9605c2.png",
			"background": "https://bixin.im/static/images/logo_scroll@2x.21af7c9605c2.png",
			"title": "title标题",
			"action": "bixin://webview_auth/?url=https://bixin.im&bot_id=f2c5609ae91c4a2ab20c4b196aac9b4a"
		},
		"sender": {
			"name": "bot_test",
			"nickname": "Ghost bot",
			"avatar_url": "https://openapi.bixin.im/res/vendor_fin_dollar2.png",
			"gender": "",
			"menu": [{
				"icon_url": "https://openapi.bixin.im/res/faq.png",
				"desc": "Test",
				"action": "bixin://postevent?event=index_view&text=Test&target_id=f2c5609ae91c4a2ab20c4b196aac9b4a&conv_type=bot"
			}],
			"btc_address": "1Har9AL8QyRuQ5DiLfm6kFndscbVR6ctHG",
			"desc": "Bixin Official Service",
			"id": "f2c5609ae91c4a2ab20c4b196aac9b4a",
			"conv_type": "bot"
		},
		"brief": "Article",
		"request_id": "a573e4760as144259dc0ee29087adea23",
		"prev_id": 9366,
		"receiver": {
			"name": "echo",
			"nickname": "12555",
			"avatar_url": "https://openapi.bixin.im/upload/2017/05/11/6146c20c214745f3b29b73216fe47fd1.png",
			"gender": "male",
			"menu": [],
			"btc_address": "1vkJV6bnJdbjocerXjLJkc3tEsjmEjh94",
			"desc": "",
			"id": "a573e67b760a44259dc0ee29087ade72",
			"conv_type": "private"
		},
		"id": 9369,
		"is_mute": false,
		"conv_type": "bot"
	}
}
```


### 广播文本

Content-Type: application/x-www-form-urlencoded

```
POST https://openapi.bixin.im/api/v2/bot.broadcastText
```

参数：

| 名称(name) | 描述(description) |
| --------- | ----------------- |
| text | 发送文本 |

返回：

```
{"ok": true}

```

### 广播图片

Content-Type: multipart/form-data

```
POST https://openapi.bixin.im/api/v2/bot.broadcastImage
```

参数：

| 名称(name) | 描述(description) |
| --------- | ----------------- |
| file | image文件 |

返回：

```
{"ok": true}

```

### 广播文章

Content-Type: application/x-www-form-urlencoded

```
POST https://openapi.bixin.im/api/v2/bot.broadcastArticle
```

参数：

| 名称(name) | 描述(description) |
| --------- | ----------------- |
| target_id | 发送对象的id|
| request_id | 请求消息id 用uuid生成 |
| conv_type | 会话类型, 可选[private,group] |
| title | artilce 消息标题 |
| desc | artilce 消息标描述 |
| image_url | 背景图片url |
| action | 跳转连接或者 event |

返回：

```
{"ok": true}
```

### 广播置顶消息

Content-Type: application/x-www-form-urlencoded

```
POST https://openapi.bixin.im/api/v2/bot.broadcastSticky
```

参数：

| 名称(name) | 描述(description) |
| --------- | ----------------- |
| text | 文本|
| action_text | action文本 |
| action | 跳转连接或者 event  |
| closable | 是否关闭 取值为0(False),1(True) |

返回：

```
{"ok": true}
```

### 广播select消息

Content-Type: application/json

```
POST https://openapi.bixin.im/api/v2/bot.broadcastSelect
```

参数：

| 名称(name) | 描述(description) |
| --------- | ----------------- |
| target_id | 发送对象的id|
| request_id | 请求消息id 用uuid生成 |
| conv_type | 会话类型, 可选[private,group] |
| select | 消息内容为数组: ['desc': '', 'image_url': '', 'action': '跳转连接或者event'] |

返回：

```
{"ok": true}
```

### 获取粉丝用户信息

```
GET https://openapi.bixin.im/api/v2/bot.getFollowers
```

返回：

```json
{
    "ok": true,
    "data": {
        "followers": [
            {
                "username": "echo",
                "id": "a573e67b760a44259dc0ee29087ade72",
                "nickname": "heid"
            },
            {
                "username": "ttttt",
                "id": "c94aa4caa38444f6bd7b4c86e10e5c3e",
                "nickname": "wqfas"
            }
        ]
    }
}
```

### 收款消息

Content-Type: application/x-www-form-urlencoded

```
POST https://openapi.bixin.im/api/v2/bot.postPaymentRequest
```

参数：

| 名称(name) | 描述(description) |
| --------- | ----------------- |
| target_id | 发送对象的id|
| request_id | 请求消息id 用uuid生成 |
| conv_type | 会话类型, 可选[private,group] |
| file | image文件 |
| btc_address|  vendor的比特币地址|
| message| 备注内容|
| amount_btc| 收款BTC数量|
| arg0|  arg[0-9]自定义参数|

返回：

```json
{
    "ok": true,
    "data": {
        "is_mute": false,
        "brief": "Payment Request",
        "content": {
            "content_type": "payment_request",
            "target_id": "a573e67b760a44259dc0ee29087ade72",
            "action": "bitcoin:1248bTMWvsKyetnw9LZ9bH6XSnjCTA3YUD?amount=0.1&message=hello%26msg&arg1=12342342&arg9=13112999",
            "conv_type": "private",
            "desc": "100,000 Bits",
            "comment": "Bixin Payment Request"
        },
        "created_at": "2017-08-14T08:40:47.984493",
        "content_type": "payment_request",
        "request_id": "acs32cs23casa44259dc0sas29081ccs232",
        "id": 83093,
        "sender": {
            "gender": "",
            "nickname": "bot nickname",
            "desc": "",
            "id": "53b0e04dfaf749c3939c3c6614fa41de",
            "menu": [],
            "conv_type": "bot",
            "name": "bot12345678",
            "avatar_url": "https://bixin.im/media/openplatform/2017/07/17/pECXyQZz7u8SuvFr.png",
            "btc_address": "1PgwDda8KuhyZJDeypm94WbDhoz4b7GJqi"
        },
        "conv_type": "bot",
        "prev_id": 83089,
        "receiver": {
            "gender": "male",
            "nickname": "heid",
            "desc": "",
            "id": "a573e67b760a44259dc0ee29087ade72",
            "menu": [],
            "conv_type": "private",
            "name": "echo",
            "avatar_url": "https://bixin.im/upload/2017/07/14/348c0df261ff487698f797d416b4a847.png",
            "btc_address": "1vkJV6bnJdbjocerXjLJkc3tEsjmEjh94"
        }
    }
}
```

### form消息

Content-Type: application/json

```
POST https://openapi.bixin.im/api/v2/bot.postForm
```

参数：

| 名称(name) | 描述(description) |
| --------- | ----------------- |
| target_id | 发送对象的id|
| request_id | 请求消息id 用uuid生成 |
| form | 详见form wiki |
| title | 文章Title |
| category | 类型（用于显示账单, 可选)|

返回：

```json
{
    "data": {
        "request_id": "1473e3b718asaasdfa123e290872322",
        "id": 83100,
        "sender": {
            "id": "f2c5609ae91c4a2ab20c4b196aac9b4a",
            "avatar_url": "https://openapi.bixin.im/res/vendor_fin_dollar2.png",
            "nickname": "Ghost bot",
            "btc_address": "1Har9AL8QyRuQ5DiLfm6kFndscbVR6ctHG",
            "gender": "",
            "desc": "",
            "conv_type": "bot",
            "name": "bx_bot_ghost",
            "menu": []
        },
        "created_at": "2017-08-15T03:46:34.895666",
        "receiver": {
            "id": "a573e67b760a44259dc0ee29087ade72",
            "avatar_url": "https://openapi.bixin.im/upload/2017/07/14/348c0df261ff487698f797d416b4a847.png",
            "nickname": "heid",
            "btc_address": "1vkJV6bnJdbjocerXjLJkc3tEsjmEjh94",
            "gender": "male",
            "desc": "",
            "conv_type": "private",
            "name": "echo",
            "menu": []
        },
        "prev_id": 83097,
        "content": {
            "id": "put-any-id-in-it",
            "title": "A title as you see",
            "form": [
                {
                    "placeholder": "Im placeholder",
                    "type": "num",
                    "name": "field-1",
                    "prefix": "desc1",
                    "label": "Im Label",
                    "suffix": "Bits"
                },
                {
                    "type": "text",
                    "value": "Im Default",
                    "name": "field-2",
                    "prefix": "desc2"
                },
                {
                    "type": "bool",
                    "value": "true",
                    "name": "field-3",
                    "prefix": "Im toggle"
                },
                {
                    "type": "date",
                    "value": "2011-03-98",
                    "name": "field-4",
                    "prefix": "Im toggle"
                },
                {
                    "options": {
                        "opt2": "Bob",
                        "opt1": "Alice"
                    },
                    "type": "select",
                    "required": true,
                    "label": "field3",
                    "name": "field-6"
                }
            ]
        },
        "brief": "form",
        "conv_type": "bot",
        "is_mute": false,
        "content_type": "form"
    },
    "ok": true
}
```


### 设置Menu

Content-Type: application/json

```
POST https://openapi.bixin.im/api/v2/bot.setMenu
```

参数：

| 名称(name) | 描述(description) |
| --------- | ----------------- |
| desc | 描述字典（支持多语言: en_US, zh_Hans) |
| action |  跳转连接或者 event 如: https://bixin.im |
| icon_url |  图标url |

返回：

```
{ 'ok': True }
```
