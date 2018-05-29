# 币信支付

币信支付拥有在不同的应用场景下完成支付的能力，涉及对话支付，JS支付，扫码支付，本地App唤起支付。对于不同的支付场景，我们这边提供了不同的支付协议，可根据不同的需求使用这些相关的支付功能。

币信还提供了对数字货币地址的支付和针对某个用户或Vendor(指定Target_id)的支付。

## 币信支付协议

### 1. 支付Schema:

对地址转账:

```
bixin://currency_transfer/?target_addr={}&amount={}&currency={}&category={}&message={}&order_id={}&transfer_type={}
```
amount，category，order_id, transfer_type均为optional

例如：

```
bixin://currency_transfer/?target_addr=16kUc5B48qnASbxeZTisCqTNx6G3DPXuKn&amount=1&currency=BTC&category=test

```

此外还可以增加额外的自定义参数(可选)。自定义参数不超过10个。 自定义参数格式必须是以"x-"开头，比如

```
bixin://currency_transfer/?target_addr=16kUc5B48qnASbxeZTisCqTNx6G3DPXuKn&amount=1&currency=BTC&x-name=your-name&x-title=your-title
```
对币信平台内部地址转账，会走0手续费实时到账的方式，对于外部地址，币信会走链上的转账(建议转账都币信内部转账)。

amount，category，order_id, transfer_type均为optional

例如：

```
bixin://currency_transfer/?target_id=b620ea4e87b0e5d3f12dd15c97a&conv_type=private&amount=1&currency=BTC&category=test
```

也可以自定义参数，规则同上。

可参考[demo](../openplatform/servicer/views.py)

### 2. JS-SDK

```
function pay(address, amount, note, category, order_id, transfer_type, your_args){
  bixin.openPay({
    amount: amount,
    recipientAddr: address,
    note: note,
    category: category,
    message: 'hello pay demo',
    order_id: '123323',
    transfer_type: 'spend',
    // your args, for example
    // 'x-name': 'your name',
    success: function(res) {
      console.log('pay success');
    },
    error: function(err) {
    }
  });
}
```

可参考[demo](../openplatform/servicer/static/js/bot.js)

## 使用

网页支付，扫码支付，JS-SDK支付，原生App支付代码可参考[demo1](../openplatform/servicer/views.py), [demo2](../openplatform/servicer/static/js/bot.js), [demo3](openplatform/servicer/templates/detail.html)

所有成功支付成功后都会触发币信平台的Event事件推送([参考](./币信消息推送机制.md))，第三方可根据推送消息来进行下一步的操作。

## 附录

### 支付流程图

![image](https://raw.githubusercontent.com/haobtc/openplatform/master/images/openplatform_pay.png)
