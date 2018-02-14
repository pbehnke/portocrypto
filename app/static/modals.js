$( document ).ready(function() {
  // function when login is clicked, to prevent usual form submit and use
  // jquery .post to communicate with flask
  $("#loginUser").prop('required',true);
  $("#loginPw").prop('required',true);
  $('#loginForm').submit(function(event) {
    event.preventDefault();
    if ($('#loginSubmit').hasClass('disabled') === false) {
      $.post("/login", data=$('#loginForm').serialize(), function(data) {
        if (data.status == 'ok') {
          $('#loginModal').modal("hide");
          location.reload();
        }
        else {
          $('#loginUser').val("");
          $('#loginUser').attr("placeholder", data);
          $('#loginPw').val("");
          $('#loginPw').attr("placeholder", data)
          console.log(data)
        }
      });
    }
  })

  $("#registerUser").prop('required',true);
  $("#emailRegister").attr('type', "email");
  $("#emailRegister").attr('data-error', "This Email is invalid");
  $("#emailRegister").prop('required',true);
  $("#regPw").attr('data-minlength', "6");
  $("#regPw").prop('required',true);
  $('#registerForm').submit(function(event) {
    event.preventDefault();
    if ($('#regSubmit').hasClass('disabled') === false) {
      // handling one scrf_toḱen for multiple forms
      $('#csrf_register').val($('#csrf_token').val());
      $('#csrf_token').attr('id', 'csrf_login');
      $('#csrf_register').attr('id', 'csrf_token');

      $.post("/register", data=$('#registerForm').serialize(), function(data) {
        if (data.status == 'ok') {
          $('#regModal').modal("hide");
          $('#loginModal').modal("show");
          // location.reload();
        }
        else {
          console.log(data)
          if (data['email']) {
            $('#emailRegister').val("");
            $('#emailRegister').attr("placeholder", data['email'])
          }
          if (data['username']) {
            $('#registerUser').val("");
            $('#registerUser').attr("placeholder", data['username']);
          }
        }
      });
      $('#csrf_token').attr('id', 'csrf_register')
      $('#csrf_login').attr('id', 'csrf_token')
    }
  })

  $('#transSubmit').click(function(event) {
    event.preventDefault();
    if ($('#transSubmit').hasClass('disabled') === false) {
      $.post("/transaction", data=$('#transFormID').serialize(), function(data) {
        if (data.status == 'ok') {
          $('#transModal').modal("hide");
          $('#transFormID').validator('destroy')
          location.reload();
        }
        else {
          message = data;
          console.log(data['number'][0])
        }
      });
      $('#csrf_token').attr('id', 'csrf_trans');
      $('#csrf_login').attr('id', 'csrf_token');
    }
  })

  $('#transNumber').keyup(function(event) {
    var totalAmount = pprice * this.value
    $('#transTotal').text("Total: $" + totalAmount);

    if (buyOrSell === "S") {
      $('#transCash').text("Cash: $" + (allData.cash + totalAmount));
    } else {
      $('#transCash').text("Cash: $" + (allData.cash - totalAmount));
    }

    if ($('#transNumber').val() === "") {
      $('#transFormID').validator('destroy')
      $('#transFormID').validator()
    }

    if (this.value > allData.coinsnumber) {
      $('#maxCoins').css('color', '#f04124');
    } else {
      $('#maxCoins').css('color', '#222222');
    }

  })
  // adding required and data-error attribut workaround to prevent jinja error
  $("#transNumber").attr('data-error', 'Invalid Input');

  // change PW
  $("#newPW").attr('data-minlength', "6");
  $("#oldPW").prop('required',true);
  $("#newPW").prop('required',true);
  $('#changeSubmit').click(function(event) {
    event.preventDefault();
    if ($('#changeSubmit').hasClass('disabled') === false) {

      $('#csrf_change').val($('#csrf_token').val());
      $('#csrf_token').attr('id', 'csrf_login');
      $('#csrf_change').attr('id', 'csrf_token');

      $.post("/password", data=$('#changeForm').serialize(), function(data) {
        if (data.status == 'ok') {
          $('#changeModal').modal("hide");
          location.reload();
        }
        else {
          console.log(data);
        }
      });

      $('#csrf_token').attr('id', 'csrf_change');
      $('#csrf_login').attr('id', 'csrf_token');
    }
  })

})

function openTransModal(short){

  buyOrSell = short.charAt(0);
  var short = short.substring(2, );

  $('#csrf_trans').val($('#csrf_token').val());
  $('#csrf_token').attr('id', 'csrf_login');
  $('#csrf_trans').attr('id', 'csrf_token');

  $('#maxCoins').text("Max: 0");

  $('#transTotal').text("Total: $0.00");
  // $('#transCash').text("Cash: $0.00");

  $('#transNumber').attr('placeholder', '0.00')


  $.getJSON("http://coincap.io/page/" + short, function(coinInfo) {

    pprice = coinInfo.price;

    $('#transShort').val(short)
    $("#transPrice").val(coinInfo.price);
    $("#transPriceText").text("Price: $" + coinInfo.price);
    $('#transLong').val(coinInfo.display_name);
    $('#transNumber').attr('max', '0')

    // get info on users cash and max amount of coins
    $.post("/check", {price:coinInfo.price, short:short}, function(data) {
        allData = data
        $('#transCash').text("Cash: $" + allData.cash);

        if(buyOrSell === 'B') {
          $('#bOs').val(false)
          $("#transTitle").text("Buy " + coinInfo.display_name);
          $("#transSubmit").val("Buy");
          max = allData.cash / coinInfo.price
          $('#maxCoins').text("Max: $" + max);
          $('#transNumber').attr('max', max)
          $("#transNumber").prop('required',true);
        }

        if(buyOrSell === 'S') {
          $('#bOs').val(true)
          $("#transTitle").text("Sell " + coinInfo.display_name);
          $("#transSubmit").val("Sell");
          $('#maxCoins').text('Max: ' + allData.coinsnumber)
          $('#transNumber').attr('max', allData.coinsnumber)
          $("#transNumber").prop('required',true);
        }

      });

    // make sure input field is empty and form is unvalidated
    $('#transNumber').val("")
    $('#transFormID').validator('destroy')
    $('#transFormID').validator()

    // open modal window
    $("#transModal").modal("show");
  })

}
