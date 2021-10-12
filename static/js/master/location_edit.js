$(document).ready(function () {

    location_id = localStorage.getItem('location')
    $.ajax({
        type: 'get',
        url: '/locations/'+location_id,
        data: {

        },
        success: function(data) {
            $('#location').val(data.data.location);
            $('#location').focus();
            $('#address_line_1').val(data.data.address_line_1);
            $('#address_line_1').focus();
            $('#town').val(data.data.town);
            $('#town').focus();
            $('#country').val(data.data.country);
            $('#country').focus();
            $('#postal_code').val(data.data.postal_code);
            $('#postal_code').focus();
        },
        error: function(data) {
            console.log(data);
//                $('#error-msg').text(data.responseJSON.status);
            },
        });
});


function checkForm(form) {

     if ($("#location").val() == "") {
          $('#location').parent().append('<span class="error">Please enter first name.</span>').addClass("has-error");
          return false;
      }

      if ($("#address_line_1").val() == "") {
          $('#address_line_1').parent().append('<span class="error">Please enter last name.</span>').addClass("has-error");
          return false;
      }

      if ($("#town").val() == "") {
          $('#town').parent().append('<span class="error">Please enter age.</span>').addClass("has-error");
          return false;
      }

      if ($("#country").val() == "") {
          $('#country').parent().append('<span class="error">Please enter school name.</span>').addClass("has-error");
          return false;
      }

  }


$('#location_submit').on('click', function() {
   validation = checkForm();
    if (validation == false) {
      return false;
    }
    location_id = localStorage.getItem('location')

    let formData = new FormData($("#location-edit")[0]);

    var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)

    if (token == null){
      window.location.href = "/"
  }


    $.ajax({
        url: "/locations/"+location_id,
        method : "PUT",
        headers: { Authorization: 'Bearer ' + access.access },
        enctype: 'multipart/form-data',
        data : formData,
        contentType : false,
        processData: false,
        async : false,
        success: function (data) {
            console.log(data);
            window.location.href = "/location_list/"
        },
          error: function (data) {
            console.log(data);
          },
       });

});