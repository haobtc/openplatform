# 闪电网络
币信开放平台目前还在内测阶段，仅支持闪电网络收款，如有需要接入，请先与币信客服联系。

### 创建invoice
```
POST https://bixin.com/platform/api/v1/lightning/invoice/create
```

相关参数介绍：

| 名称(name) | 描述(description) |
| ---------  | ---------------- |
| currency   | 必填，只支持BTC |
| amount     | 选填，默认值0 |
| memo       | 选填 |

返回：
```
{
    "status": "PENDING",
    "ok": true,
    "created_at": "2019-04-25T12:26:36.798Z",
    "id": "ad1b880d49ee4bb9bade34718ad21918",
    "amount": "1",
    "invoice": "lnbc10n1pwvrfmupp5lf9admrmnlxwh2lfhl8x88lr9e38rq5ypwrqclft4e40384nxxx",
    "memo": ""
}
```

注意：
1. invoice有效期1小时，过期将不能使用。
2. 一个invoice只能使用一次。
3. invoice amount不填默认0，数量将由付款方填写。
4. invoice amount最大值目前只支持到1000000聪


### 查看invoice详情
```
GET https://bixin.com/platform/api/v1/lightning/invoice/detail?access_token=5c83073ecd0d444480a59a&id=xxx
```

相关参数介绍：

| 名称(name) | 描述(description) |
| --------- | ----------------- |
| id        | 必填.  |

返回：
```
{
    "status": "SUCCESS",
    "ok": true,
    "created_at": "2019-04-25T12:26:36.798Z",
    "expired_at": "2019-04-25T13:26:36.798Z",
    "id": "ad1b880d49ee4bb9bade34718ad21918",
    "amount": "1",
    "invoice": "lnbc10n1pwvrfmupp5lf9admrmnlxwh2lfhl8x88lr9e38rq5ypwrqclft4e40384nxxx",
    "memo": ""
}
```
status状态分为 PENDING，EXPIRED，SUCCESS


### 获取invoice列表
```
GET https://bixin.com/platform/api/v1/lightning/invoice/list?access_token=5c83073ecd0d444480a59a7ed34cde3c&since=1556243129
```
相关参数介绍：

| 名称(name) | 描述(description) |
| --------- | ----------------- |
| since     | 选填. 时间戳格式 1556243129 |

返回：

```
{
    "ok": true,
    "result": [
        {
            "status": "PENDING",
            "created_at": "2019-04-25T12:25:42.152Z",
            "expired_at": "2019-04-25T13:25:42.152Z",
            "id": "6e7cde1868764cb8a74e5f6a0e78b1bb",
            "amount": "0",
            "invoice": "lnbc10n1pwvrfmupp5lf9admrmnlxwh2lfhl8x88lr9e38rq5ypwrqclft4e40384nxxx",
            "memo": ""
        },
        {
            "status": "PENDING",
            "created_at": "2019-04-25T12:26:36.798Z",
            "expired_at": "2019-04-25T13:25:42.152Z",
            "id": "ad1b880d49ee4bb9bade34718ad21918",
            "amount": "1",
            "invoice": "lnbc10n1pwvrfmupp5lf9admrmnlxwh2lfhl8x88lr9e38rq5ypwrqclft4e40384nxxx",
            "memo": ""
        }
    ]
}
```
