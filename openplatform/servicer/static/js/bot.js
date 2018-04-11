var ready = false;
function setConfig() {
  bixin.config({
    debug: 'true',
    vendorName: vendor_name, //vendor的名字，全网唯一
    timestamp: timestamp, //生成签名的时间戳
    nonce: nonce, //生成签名的随机串
    signature: sign, //签名，方法参见下条
    callback: callback, //vendor的callback地址
    jsApiList: ["openPay", "scanQRCode", "chooseContact", "openConv", "previewImage", "sendMiniArticle"], // 需要调用的api名字列表，如果有不支持的API，则调用bixin.error();
  });

  bixin.ready(function(){
    console.log("bixin.ready");
    ready = true;
  });
}

function chat(target_id, conv_type){
  bixin.openConv({
    targetId: target_id,
    convType: conv_type,
    success: function(res){
    },
    cancel: function(res){
    },
    fail: function(res) {
    }
  });
}

function scanQRCode(){
  bixin.scanQRCode({
      needResult: false, // 默认为false，扫描结果由币信处理，true则直接返回扫描结果
      //scanType: ["qrCode",], // 只需支持qrcode
      success: function (res) {
        var result = res.resultStr; // 当needResult 为 true 时，扫码返回的结果
       }
  });
}

function choose_contact(){
  bixin.chooseContact({
      type: "user",
      success: function(res) {
        console.log(res); // user object
      }
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

function pay(currency, address, amount, note, category, args){
  bixin.openPay({
    currency: currency,
    recipientAddr: address,
    amount: amount,
    note: note,
    category: category,
    args0: args,
    message: 'hello pay demo',
  success: function(res) {
    console.log('pay success');
  },
  error: function(err) {
  }
});
}

function open_chat(target_id, conv_type){
  if(!ready){
    setConfig();
  }
  setTimeout(_async_cancel=function(){
    chat(target_id, conv_type)
  },1000);
}

function open_scan(){
  if(!ready){
    setConfig();
  }
  setTimeout(_async_cancel=function(){
    scanQRCode();
  },1000);
}

function open_pay(currency, address, amount, note, category, args){
  if(!ready){
    setConfig();
  }
  setTimeout(_async_cancel=function(){
    pay(currency, address, amount, note, category, args);
  },1000);
}

function open_choose_contact(){
  if(!ready){
    setConfig();
  }
  setTimeout(_async_cancel=function(){
    choose_contact();
  },1000);
}

function share_article(url, bot_target_id, title, desc, image_url){
  if(!ready){
    setConfig();
  }
  setTimeout(_async_cancel=function(){
    bixin.chooseContact({
      success: function(contact) {

        var target_id = contact.targetId;
        var conv_type = contact.convType; //可选为: private, bot, group,

        send_min_article(url, bot_target_id, target_id, conv_type,
                         title, desc, image_url);
      }
    });
  },1000);
}
