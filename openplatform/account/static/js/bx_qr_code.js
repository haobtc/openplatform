var ticking_interval = null;
var protocol = null;
var expired_at = null;
var ticking_interval = null;
var qr_refresh_img_url = null;
var qr_login_url = null;

function createQRCode(message) {
  var typeNumber = 10;
  var errorCorrectionLevel = 'L';
  var qr = qrcode(typeNumber, errorCorrectionLevel);
  qr.addData(message);
  qr.make();
  return qr;
}

function drawBXQRCode(data) {
  bx_login_url = data.protocol;

  var qr = createQRCode(bx_login_url);
  var img = $(qr.createImgTag())[0]
  document.getElementById('bxQRCodeImage').src = img.src;
  document.getElementById('bxQRCodeImage').onclick = null;
  document.getElementById('bxQRCodeImage').classList.remove("bx-qr-code");
}

function refresh_button(data){
  document.getElementById('login_button').href = data.protocol;
}

function getQRCode() {
  var query_url = location.protocol + "//" + location.host + '/account/qr_session/';
  $.get(query_url, function(resp) {
    var data = resp.result;
    if (data == undefined || data.expired_at == undefined || data.protocol == undefined) {
      console.error('error in getting qr code data');
    }
  }).done(function(resp) {
    var data = resp.result;
    protocol = data.protocol;
    expired_at = data.expired_at;
    if(from_device == 'phone'){
      refresh_button(data);
    }else{
      drawBXQRCode(data);
    }
  });
}

function checkQRCode() {
  var uuid = '';
  if (protocol != null && expired_at != null) {
    var uri = decodeURI(protocol);
    if(from_device == 'phone'){
      // bixin://login/confirm?url=http%3A%2F%2F192.168.1.121%3A8000%2Fqrcode%2F%3Fuuid%3Dweb%3Ad6c59710b80b43e2b7d6dd078393507f
      // need get url query
      url = getQueryString(uri, 'url');
      var qr_code_url = decodeURIComponent(url);
      uuid = getQueryString(qr_code_url, 'uuid')
    }else{
      uuid = getQueryString(uri, 'uuid');
    }
    checkQRCodeAuth(uuid);
  }
}

function getQueryString(full_url, field){
  var reg = new RegExp( '[?&]' + field + '=([^&#]*)', 'i' );
  var string = reg.exec(full_url);
  return string ? string[1] : null;
}

function checkQRCodeAuth(uuid) {
  var query_url = location.protocol + "//" + location.host + '/account/qr_session/?uuid=' + uuid;
  $.get(query_url, function(resp) {
  }).done(function(resp) {
    data = resp;
    if (data.ok == true) {
      next_url = getQueryString(window.location.href, 'next');
      if(next_url != null ){
        window.location = decodeURIComponent(next_url);
      }else {
        window.location = '/account/index/';
      }
    } else if (data.error == 'qr code expired') {
      clearInterval(ticking_interval);
      // refresh button protocol
      if(from_device == 'phone'){
        getQRCode();
        startInterval()
      }else{
        document.getElementById('bxQRCodeImage').src = qr_refresh_img_url;
        document.getElementById('bxQRCodeImage').onclick = function(){init_qr_code(qr_refresh_img_url, qr_login_url);};
        document.getElementById('bxQRCodeImage').classList.add("bx-qr-code");
      }
    }
  });
}


function startInterval() {
  ticking_interval = setInterval(checkQRCode, 1000);
}

function init_qr_code(refresh_img_url, login_url) {
  qr_refresh_img_url = refresh_img_url;
  qr_login_url = login_url;
  getQRCode();
  setTimeout(startInterval, 5000)
}

