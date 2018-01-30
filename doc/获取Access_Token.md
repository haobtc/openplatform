# Access Token

Access Token 是第三方和币信Vendor交互的唯一凭证，任何涉及到获取Vendor信息(转账、关注用户、数字货币地址等等)时必须携带Access Token, 默认有效期为三天。

### 获取Access Token

在创建vendor页面的右侧可以看到Vendor Secret, 使用Vendor Secret,调用API，即可获取币信分配的Access Token:

![image](https://raw.githubusercontent.com/haobtc/openplatform/master/images/vendor_secret.png)

调用API：

```
GET https://bixin.im/platform/token/?vendor=hello&secret=09cbdbb7be8a46dc8949c9818c5e9d6c
```

返回

```
{
    "access_token": "30e57a621fa2474c914ac7ca6c85cc18",
    "expire_in": 259200
}

```
