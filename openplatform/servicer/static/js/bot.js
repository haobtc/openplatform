var ready = false;
function env_exec(func) {

  if(ready){
    func();
    return
  }

  bixin.config({
    debug: 'true',
    vendorName: vendor_name, //vendor的名字，全网唯一
    timestamp: timestamp, //生成签名的时间戳
    nonce: nonce, //生成签名的随机串
    signature: sign, //签名
    callback: callback, //vendor的callback地址
    jsApiList: ["openPay", "scanQRCode", "chooseContact", "openConv", "previewImage", "sendMiniArticle", "openC2bPay", "openC2bDeposit"], // 需要调用的api名字列表，如果有不支持的API，则调用bixin.error();
  });

  bixin.ready(function(){
    console.log("bixin.ready");
    ready = true;
    func();
  });
}

function send_min_article(url, bot_target_id, user_target_id, conv_type, title, desc, image_url){
  bixin.sendMiniArticle({
    url: url,
    bot_id: bot_target_id,
    target_id: user_target_id,
    conv_type: conv_type,
    title: title,
    desc: desc,
    image_url: image_url,
    success: function(res){
      console.log(res);
    }
  });
}

function open_chat(target_id, conv_type, event, text){
  env_exec(function(){
    if(event && text){
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
    }else{
      bixin.openConv({
        targetId: target_id,
        convType: conv_type,
        text: text,
        success: function(res){
        },
        cancel: function(res){
        },
        fail: function(res) {
        }
      });
    }
  })
}

function open_scan(){
  env_exec(function(){
    bixin.scanQRCode({
        needResult: false, // 默认为false，扫描结果由币信处理，true则直接返回扫描结果
        //scanType: ["qrCode",], // 只需支持qrcode
        success: function (res) {
          var result = res.resultStr; // 当needResult 为 true 时，扫码返回的结果
         }
    });
  })
}

function open_pay(currency, address, amount, note, category, message){
  env_exec(function(){
    bixin.openPay({
      currency: currency,
      recipientAddr: address,
      amount: amount,
      category: category,
      message: message,
      success: function(res) {
        console.log('pay success');
      },
      error: function(err) {
      }
    });
  })
}

function open_pay_with_order(currency, address, amount, category, message, order_id, transfer_type){
  env_exec(function(){
    bixin.openPay({
      currency: currency,
      recipientAddr: address,
      amount: amount,
      category: category,
      message: message,
      order_id: order_id,
      transfer_type: transfer_type,
      success: function(res) {
        console.log('pay success');
      },
      error: function(err) {
      }
    });
  })
}

function open_pay_with_order_args(currency, address, amount, category, message, order_id, transfer_type, your_args){
  env_exec(function(){
    bixin.openPay({
      currency: currency,
      recipientAddr: address,
      amount: amount,
      category: category,
      message: message,
      order_id: order_id,
      transfer_type: transfer_type,
      'x-name': your_args,
      success: function(res) {
        console.log('pay success');
      },
      error: function(err) {
      }
    });
  })
}

function open_c2b_pay(currency, address, amount, message, memo){
  env_exec(function(){
    bixin.openC2bPay({
      currency: currency,
      recipientAddr: address,
      amount: amount,
      message: message,
      memo: memo,
      success: function(res) {
        console.log('c2b pay success');
      },
      error: function(err) {
      }
    });
  })
}

function open_c2b_deposit(currency, address, message, memo){
  env_exec(function(){
    bixin.openC2bDeposit({
      currency: currency,
      recipientAddr: address,
      message: message,
      memo: memo,
      success: function(res) {
        console.log('c2b deposit success');
      },
      error: function(err) {
      }
    });
  })
}

function open_choose_contact(){
  env_exec(function(){
    bixin.chooseContact({
        success: function(contact) {
          console.log(contact); // user object
        }
    });
  })
}

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
