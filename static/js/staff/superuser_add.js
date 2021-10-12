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
// if ($("#mobile").val() == "") {
//      $('#mobile').parent().append('<span class="error">Please enter mobile.</span>').addClass("has-error");
//      return false;
//  }
// if ($("#address").val() == "") {
//      $('#address').parent().append('<span class="error">Please enter address.</span>').addClass("has-error");
//      return false;
//  }
// if ($("#postal_code").val() == "") {
//      $('#postal_code').parent().append('<span class="error">Please enter postal code.</span>').addClass("has-error");
//      return false;
//  }
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
    window.location.href = "/staff_list/"
});

$(document).on('submit', '#superuser-add', function (e) {

    var url =  window.location.pathname;
    var id = url.substring(url.lastIndexOf('/') + 1);

    validation = checkForm();
    if (validation == false) {
      return false;
    }
    let formData = new FormData($("#superuser-add")[0]);
    $.ajax({
        url: "/super_user_add/",
        method : "POST",
        enctype: 'multipart/form-data',
        data : formData,
        contentType : false,
        processData: false,
        async : false,
        success: function (data) {
            window.location.href = "/super_user_list/"
            $('#myModal').show();
        },
        error: function (data) {
            console.log(data);
        },
    });
})
