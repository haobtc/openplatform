# 安装步骤

### Database

默认使用sqlite

```
python manage.py migrate
```

### Settings

在币信[https://bixin.com/openplatform/](https://bixin.com/openplatform/) 页面中获取你创建的vendor的相关信息，配置下面的参数：

```
APP_NAME = 'your-account'
VENDOR_SECRET = 'your-vendor-secret'
VENDOR_AES_KEY = 'your-aes-key'
BOT_ACCESS_TOKEN = 'your-bot-access-token'
BOT_AES_KEY = 'your-bot-aes-key'

```

### Nginx && Supervisor

```
sudo ln -s project_root/etc/nginx/default.conf /etc/nginx/conf.d/default.conf
sudo ln -s project_root/etc/supervisor.d/default.conf /etc/supervisor/conf.d/default.conf
```

### Start

```
sudo supervisord -c /etc/supervisor/supervisor.conf
```

### 创建menu

```
python manage.py create_bot_menu
```

## 网站展示

用户可以到网站[https://platformapidemo.bixin.com/](https://platformapidemo.bixin.com/),这里提供了登录，转账，提现和JS-SDK的相关功能，可以进行查看


## 服务号基础功能展示

可以通过币信App扫码，扫码关注下面这个Demo二维码：

![image](https://raw.githubusercontent.com/haobtc/openplatform/master/images/bot_demo_qrcode.png)

在这里创建了基础的menu和用户交互。
