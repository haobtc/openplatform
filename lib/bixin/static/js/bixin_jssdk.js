var userAgent = navigator.userAgent.toLowerCase();
console.log(userAgent);
var IS_ANDROID = -1 != userAgent.indexOf("android");
var IS_IOS = -1 != userAgent.indexOf("iphone") || -1 != userAgent.indexOf("ipad");


var ApiNames = {
  config: "config",
  openPay: "openPay",
  scanQRCode: "scanQRCode",
  chooseContact: "chooseContact",
  openConv: "openConv",
  previewImage: "previewImage",
  sendMiniArticle: "sendMiniArticle"
}

function onResultHandle(apiName, result, callback){
  var jo = JSON.parse(result);
  console.log("Bridge Return:" + JSON.stringify(jo));

  if (callback._complete) {
    callback._complete(jo);
    delete callback._complete;
  }

  var responseStatus = (jo.errMsg).substring(apiName.length + 1);
  switch(responseStatus){
    case "ok":
      callback.success && callback.success(jo);
      break;
    case "cancel":
      callback.cancel && callback.cancel(jo);
      break;
    default:
      callback.fail && callback.fail(jo);
      break;
  };
  callback.complete && callback.complete(jo);
}

function invoke(apiName, params, callback) {
  window.WebViewJavascriptBridge.callHandler(apiName, params,
    function(result){
      onResultHandle(apiName, result, callback);
    });
}

function getOpenPayParams(data) {
  params = {
    amount: data.amount,
    recipientAddr: data.recipientAddr,
    message: data.message,
    category: data.category,
    currency: data.currency,
    order_id: data.order_id,
    transfer_type: data.transfer_type,
  }
  var re = /^x-/;
  for(var k in data){
    if(re.test(k)){
      params[k] = data[k];
    }
  }
  return params
}

var ConfigCallBack = {
  _completeCallBacks: []
}

var GlobalState = {
  state: 0, //0为初始值，配置错误为-1，配置成功为1
  res: {}
}

bixin = {
  config: function(data){
    invoke(ApiNames.config, data,
     function(){
      ConfigCallBack._complete = function(res){
        GlobalState.state = 1;
      };

      var configCompleteCallBacks = ConfigCallBack._completeCallBacks;

      ConfigCallBack.success = function(res){
        for (var i = 0, length = configCompleteCallBacks.length; i < length; i++)
          configCompleteCallBacks[i]();
        ConfigCallBack._completeCallBacks = [];
      };
      ConfigCallBack.fail = function(res){
        ConfigCallBack._fail ? ConfigCallBack._fail(res) : GlobalState.state = -1;
      };

      ConfigCallBack.complete = function(res) {

      }
      return ConfigCallBack;
    }());
  },
  ready: function(callback) {
    if (GlobalState.state != 0) {
      callback()
    } else {
      ConfigCallBack._completeCallBacks.push(callback);
    }
  },
  error: function(callback) {
    if (GlobalState.state == -1) {
      callback(GlobalState.res);
    } else {
      ConfigCallBack._fail = callback;
    }
  },
  openPay: function(data){
    invoke(ApiNames.openPay, getOpenPayParams(data), data);
  },
  scanQRCode: function(data) {
    invoke(ApiNames.scanQRCode, {
      needResult: data.needResult ? true : false
    }, data);
  },
  chooseContact: function(data) {
    invoke(ApiNames.chooseContact, {
    }, data);
  },
  openConv: function(data) {
    var params = {
      targetId: data.targetId,
      convType: data.convType
    };
    if (data.hasOwnProperty('text')) {
      params['text'] = data.text;
    }
    if (data.hasOwnProperty('event')) {
      params['event'] = data.event;
    }

    invoke(ApiNames.openConv, params, data);
  },
  previewImage: function(data) {
    invoke(ApiNames.previewImage, {
      current: data.current,
      urls: data.urls
    }, data);
  },
  sendMiniArticle: function(data) {
    invoke(ApiNames.sendMiniArticle, {
      url: data.url,
      bot_id: data.bot_id,
      target_id: data.target_id,
      conv_type: data.conv_type,
      title: data.title,
      desc: data.desc,
      image_url: data.image_url
    }, data);
  }
}
