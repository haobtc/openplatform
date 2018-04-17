## JS SDK 使用
币信JS-SDK是币信开放平台面向网页开发者提供的基于微信内的网页开发工具包。通过使用币信JS-SDK，网页开发者可借助币信高效地使用支付，扫码，转账等币信原生App的功能，为币信用户提供更优质的网页体验。

## 账号
登陆币信开放平台，注册Vendor应用。在编辑查看Vendor应用页面可以看到Vendor的应用账号名称。

## 通过config接口注入权限验证配置
JS-SDK的页面必须先注入配置信息，否则将无法调用(同一个url仅需调用一次，对于变化url的SPA的web app可在每次url变化时进行调用)。

### config 配置

``` js

<script src="https://bixin.im/static/js/bixin-js.1.0.1.js"></script>
<script>
bixin.config({
  debug: true,
  vendorName: 'my_first_bixin_app', //vendor的名字，全网唯一
  timestamp: 1499394832, //生成签名的时间戳
  nonce: 'CgQLBgEA', //生成签名的随机串
  signature: 'da39a3ee5e6b4b0d3255bfef95601890afd80709', //签名，方法参见附录
  callback: 'https://my.app.im/callback', //vendor的callback地址
  jsApiList: ['openPay'], // 需要调用的api名字列表，如果有不支持的API，则调用bixin.error();
});
</script>

```

币信支持调用的jsApiList分别为: openPay(打开支付),scanQRCode(调用扫码),chooseContact(打开联系列表),openConv(打开聊天对话框),previewImage(预览图片)。

关于签名生成的逻辑和代码详见本页面的附录

### config 验证结果

验证成功:

```
bixin.ready(function() {
    // ....
});
```

验证失败:

```
bixin.error(function(res) {
    // .....
});
```

## API介绍

### 调用币信支付

```
bixin.openPay({
      nonce: '',
      signature: '',
      amount: '1.05',
      recipientAddr: '15Rxxxxx',
      note: 'pay to friend'，
      category: data.category,
      order_id: data.order_id,
      message: data.message,
      transfer_type: data.transfer_type,
      //商户可自定义参数，我们后端会做保存
      // 可自定义多个参数，参数个数不超过10个
      //自定义参数的格式是以"x-"开头，比如
      // 'x-name': 'your-name'
      success: function(res) {
      },
      error: function(err) {
         // 各种错误，包括用户取消支付
         // TODO: 错误信息
      }
});
```
recipientAddr 是收款方的地址。

### 调用币信扫码

```
bixin.scanQRCode({
    needResult: false, // 默认为false，扫描结果由币信处理，true则直接返回扫描结果
    //scanType: ["qrCode",], // 只需支持qrcode
    success: function (res) {
      var result = res.resultStr; // 当needResult 为 true 时，扫码返回的结果
     }
});
```

### 调用联系人列表

```
bixin.chooseContact({
    success: function(contact) {
      var target_id = contact.targetId
      var conv_type = contact.conv_type
      // 其他信息还包括: name, title, avatarUrl
    }
});
```
### 打开对话框

#### 打开并发送文本(文本为空时则不发送自定义内容)

```
bixin.openConv({
    targetId: target_id,
    convType: conv_type,
    text: text
    success: function(res){
    },
    cancel: function(res){
    },
    fail: function(res) {
    }
});

```

#### 打开并发送事件(发送事件时，必须携带文本)

```
bixin.openConv({
    targetId: target_id,
    convType: conv_type,
    event: event,
    text: text,
    success: function(res){
    },
    cancel: function(res){
    },
    fail: function(res) {
    }
});

```

#### 转发消息内容给某个联系人或群组

```
bixin.sendMiniArticle({
    url: url, // 用户点击可访问的url
    bot_id: bot_target_id, // 商户自己的bot target id
    target_id: user_target_id, // 接受者的target id
    conv_type: conv_type, // 支持两种类型：private, group
    title: title,
    desc: desc,
    image_url: image_url,
    success: function(res){
      console.log(res);
    }
});
```
如果让用户选择联系人之后再对选择的人或者群组转发可使用chooseContact在调用sendMiniArticle

```
function share_article(url, bot_target_id, title, desc, image_url){
  env_exec(function(){
    bixin.chooseContact({
      success: function(contact) {

        var target_id = contact.targetId;
        var conv_type = contact.convType; //可选为: private, bot, group,

        send_min_article(url, bot_target_id, target_id, conv_type,
                         title, desc, image_url);
      }
    });
  })
}
```
### 代码demo

[参考](https://github.com/haobtc/openplatform/blob/master/openplatform/servicer/static/js/bot.js)
