$(document).ready(function () {
    var url =  window.location.pathname;
    var id = url.substring(url.lastIndexOf('/') + 1);
    $.ajax({
        type: 'get',
        url: '/super_user/'+id,
        data: {

        },
        success: function(data) {
            $('#email').focus();
            $('#email').val(data.data.email);
            $( "#first_name" ).focus();
            $('#first_name').val(data.data.first_name);
            $( "#last_name" ).focus();
            $('#last_name').val(data.data.last_name);
//            $('#mobile').focus();
//            $('#mobile').val(data.data.mobile);
//            $('#landline').focus();
//            $('#landline').val(data.data.landline);
//            $('#address').focus();
//            $('#address').val(data.data.address);
//            $('#postal_code').focus();
//            $('#postal_code').val(data.data.postal_code);
        },
        error: function(data) {
            console.log(data);
//                $('#error-msg').text(data.responseJSON.status);
            },
        });
});


function IsEmail(email) {
    var regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if (!regex.test(email)) {
      return false;
    } else {
      return true;
    }
  }

//function isValidPostcode(p) {
//    var postcodeRegEx = /[A-Z]{1,2}[0-9]{1,2} ?[0-9][A-Z]{2}/i;
//    return postcodeRegEx.test(p);
//}

function checkForm(form) {
    if (IsEmail($("#email").val()) == false) {
       $('#email').parent().append('<span class="error">Please enter email.</span>').addClass("has-error");
       return false;
    }
    if ($("#first_name").val() == "") {
          $('#first_name').parent().append('<span class="error">Please enter first name.</span>').addClass("has-error");
          return false;
      }
    if ($("#last_name").val() == "") {
          $('#last_name').parent().append('<span class="error">Please enter last name.</span>').addClass("has-error");
          return false;
      }
}

$("#first_name,#last_name").on("keypress", function (event) {
var regex = new RegExp("^[a-zA-Z \b]+$");
var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
if (!regex.test(key)) {
  event.preventDefault();
  return false;
}
});

$("#mobile,#landline").on("keypress keyup blur",function (event) {
$(this).val($(this).val().replace(/[^\d].+/, ""));
if ((event.which < 48 || event.which > 57)) {
    event.preventDefault();
}
});

$("#myModal").on("hidden.bs.modal", function () {
    location.reload();
});

$(document).on('submit', '#superuser-edit', function (e) {

    var url =  window.location.pathname;
    var id = url.substring(url.lastIndexOf('/') + 1);

    validation = checkForm();
    if (validation == false) {
      return false;
    }
    let formData = new FormData($("#superuser-edit")[0]);
    $.ajax({
        url: "/super_user/"+id,
        method : "PUT",
        enctype: 'multipart/form-data',
        data : formData,
        contentType : false,
        processData: false,
        async : false,
        success: function (data) {
            window.location.href = "/super_user_list/"
        },
        error: function (data) {
            console.log(data);
        },
    });
})
