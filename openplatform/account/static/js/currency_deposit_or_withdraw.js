var ticking_interval = null;

function create_qr_code(data){
  var typeNumber = 10;
  var errorCorrectionLevel = 'L';
  var qr = qrcode(typeNumber, errorCorrectionLevel);
  qr.addData(data);
  qr.make();
  return qr;
}

function draw_qr_code(id_select, data){
  var qr = create_qr_code(data);
  var img = $(qr.createImgTag())[0]
  document.getElementById(id_select).src = img.src;
}

function getQueryString(full_url, field){
  var reg = new RegExp( '[?&]' + field + '=([^&#]*)', 'i' );
  var string = reg.exec(full_url);
  return string ? string[1] : null;
}

function check_qr_code(data){
  var data = decodeURIComponent(data)
  var args = getQueryString(data, 'args').replace(/\+/, '');
  var json_args = JSON.parse(args);
  var deposit_id = json_args['deposit_id']

  $.ajax({
    url: '/assets/deposit_process/?deposit_id=' + deposit_id,
  }).done(function(resp){
    if(resp.ok && resp.result == 'success'){
      clearInterval(ticking_interval);
      alert('充值成功');
      window.location.href = '/account/index/';
    }
  })
}

function startInterval(result) {
  ticking_interval = setInterval(function(){
    check_qr_code(result);
  }, 3000);
}

function create_deposit(currency){
  if(!$('#deposit_modal').is(':visible')){
    $('#deposit_modal').modal('show');
    if(ticking_interval){
      clearInterval(ticking_interval);
    }

    $('#deposit_modal').on('shown.bs.modal', function (e) {
      $.ajax({
        url: '/assets/request_deposit/?currency=' + currency,
      }).done(function(resp){
        if(resp.ok){
          result = resp.result;
          draw_qr_code('deposit_qr_code', result);
          startInterval(result);
        }
      })
    })

    $('#deposit_modal').on('hidden.bs.modal', function(e){
      clearInterval(ticking_interval);
    })
  }
}

function create_withdraw(currency){
  if(!$('#withdraw_modal').is(':visible')){
    $('#withdraw_modal').modal('show');
  }
}

function submit_withdraw(){
  var currency = $('#withdraw_currency').val();
  var amount = $('#withdraw_amount').val();

  var data = {
    'currency': currency,
    'amount': amount,
  }

  $.ajax({
    url: '/assets/request_withdraw/',
    method: 'POST',
    data: data,
  }).done(function(resp){
    if(resp.ok){
      alert('提现请求已经提交');
      window.location.href = '/account/index/';
    }else{
      alert(resp.error[0]);
      window.location.href = '/account/index/';
    }
  })
}
