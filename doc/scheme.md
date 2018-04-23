## Bixin Scheme 使用

Bixin Scheme是用来唤起币信app内相关功能的协议。

## 支付协议

可参考[支付](./payments.md)

## 对话框协议

```
bixin://conversation/?target_id={}&conv_type={} [ &text={} ] [ &event={} 如果有 event 必须有 text]
```

1. event 和 text 是可选参数
2. conv_type 支持类型为: priate(用户和用户之间), group(用户和聊天群组之间)
3. 如果有配置了event, 则必须添加text

## 授权登录协议

```
bixin://login/confirm/?url={}
```

此处的url应为(需要进行urlencode):

```
https://login.bixin.im/?uuid={vendor_name}:{your-token}
```

举例：

```
bixin://login/confirm?url=https%3A%2F%2Flogin.bixin.im%2Fqrcode%2F%3Fuuid%3Dvendor_demo%3Afe07ce4768d842b7842e0ca4c722b6ba
```
