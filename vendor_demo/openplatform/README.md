# 安装步骤

### Database

默认使用sqlite

```
python manage.py migrate bixin
```

### Settings

在币信https://bixin.com/openplatform/页面中获取你创建的vendor的相关信息，配置下面的参数：

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
