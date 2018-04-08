## Vendor-API 使用
使用Vendor Api可以获取关注Vendor的相关用户信息和对Vendor资金的一些相关操作。所有对vendor的操作必须携带access_token。[获取access_token demo](./获取Access_Token.md)

## 获取用户信息

```
GET https://bixin.im/platform/api/v1/user/:userid?access_token=30e57a621fa2474c914ac7ca6c85cc18

```

返回：

```json
{
    "username": "freeza",
    "vendor.BTC.hold": "10",
    "vendor.CNY.hold": "0",
    "vendor.CNY.cash": "0",
    "fullname": "freeza91",
    "id": 1,
    "vendor.BTC.cash": "10"
}
```

## 获取用户关注列表


```
 GET https://bixin.im/platform/api/v1/user/list?access_token=30e57a621fa2474c914ac7ca6c85cc18
```

参数：

| 名称(name) | 描述(description) |
| --------- | ----------------- |
| access_token | API Token|
| offset | default 0 |
| limit | default 100 |

返回：

```
{
    "has_more": false,
    "items": [
        {
            "username": "freeza",
            "vendor.BTC.hold": "10",
            "vendor.CNY.hold": "0",
            "vendor.CNY.cash": "0",
            "fullname": "freeza91",
            "id": 1,
            "vendor.BTC.cash": "10"
        },
    ],
    "offset": 0
}
```

## 获取Vendor的地址

```
GET https://bixin.im/platform/api/v1/address/list?access_token=30e57a621fa2474c914ac7ca6c85cc18
```

参数：

| 名称(name) | 描述(description) |
| --------- | ----------------- |
| currency | 'BTC', 'ETH'|
| offset | default 0 |
| limit | default 100 |

返回

```
{
    "has_more": false,
    "items": [
        "1Mxk2PtNkCY8GspiSRnhmEzDqJw1mDo6M1",
        "1Mxk2PtNkCY8GspiSRnhmEzDqJw1mso6Ms"
    ],
    "offset": 0
}
```

## 对Vendor提现

```
POST https://bixin.im/platform/api/v1/withdraw/create
```

参数：

| 名称(name) | 描述(description) |
| --------- | ----------------- |
| access_token | API Token |
| user | 必填，数字 |
| currency | 必填 |
| amount | 必填 |
| client_uuid | 必填 |
| reply_transfer_id | 选填 |
| note | 选填 |
| category | 选填 |
| args | 选填 |

返回：

```
{
    "status": "SUCCESS",
    "vendor": "hello",
    "args": {},
    "currency": "BTC",
    "user.id": 1,
    "id": 13,
    "category": "",
    "client_uuid": "40e57a621fa2474c914ac7ca6c85cc18",
    "note": "",
    "amount": "-1",
    "reply_transfer_id": 0
}
```

## 获取某笔转账信息
```
GET https://bixin.im/platform/api/v1/transfer/145654?access_token=30e57a621fa2474c914ac7ca6c85cc18
```

返回：
```
{
    "status": "SUCCESS",
    "vendor": "hello",
    "args": { },
    "currency": "BTC",
    "user.id": 1,
    "id": 13,
    "category": "",
    "client_uuid": "12e57a621fa2474c914ac7ca6c85cc18",
    "note": "",
    "amount": "-1",
    "reply_transfer_id": 0
}
```

## 获取转账列表

```
GET https://bixin.im/platform/api/v1/transfer/list?access_token=30e57a621fa2474c914ac7ca6c85cc18
```

查询参数:

| 名称(name) | 描述(description) |
| --------- | ----------------- |
| access_token | API Token |
| offset | 选填。 default 0 |
| limit | 选填。 default 100 |
| order | 选填。 default asc |
| status | 选填。 'ADMIN_REQUIRED'、'ADMIN_DENIED'、'SUCCESS'。 default is all |
| type | 选填。 'deposit', 'withdraw' |


返回：

```
{
    "has_more": false,
    "items": [
        {
            "status": "SUCCESS",
            "vendor": "hello",
            "args": { },
            "currency": "BTC",
            "user.id": 1,
            "id": 13,
            "category": "",
            "client_uuid": "12e57a621fa2474c914ac7ca6c85cc18",
            "note": "",
            "amount": "-1",
            "reply_transfer_id": 0
        }
    ],
    offset: 0
}
```
