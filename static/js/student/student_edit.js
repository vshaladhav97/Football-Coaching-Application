$(document).ready(function () {

     $.ajax({
        type: 'get',
        url: '/age_group/',
        data: {

        },
        success: function(data) {
            jQuery.each(data.data, function (i, item) {
                $('#age-group').append("<option value=" + item.id +">" + item.age_group_text + "</option>")
            });
        },
        error: function(data) {
//            console.log(data);
                $('#error-msg').text(data.responseJSON.status);
            },
        });
    student = localStorage.getItem('student')
    $.ajax({
        type: 'get',
        url: '/students/'+student,
        data: {

        },
        success: function(data) {
            $('#first_name').val(data.data.first_name);
            $('#last_name').val(data.data.last_name);
            $('#age').val(data.data.age);
            $('#school_name').val(data.data.school_name);
            $('#age-group').val(data.data.age_group.id);
            $('#select2-chosen-3').html(data.data.age_group.age_group_text);
        },
        error: function(data) {
//            console.log(data);
                $('#error-msg').text(data.responseJSON.status);
            },
        });
});


function checkForm(form) {

     if ($("#first_name").val() == "") {
          $('#first_name').parent().append('<span class="error">Please enter first name.</span>').addClass("has-error");
          return false;
      }

      if ($("#last_name").val() == "") {
          $('#last_name').parent().append('<span class="error">Please enter last name.</span>').addClass("has-error");
          return false;
      }

      if ($("#age").val() == "") {
          $('#age').parent().append('<span class="error">Please enter age.</span>').addClass("has-error");
          return false;
      }

      if ($("#school_name").val() == "") {
          $('#school_name').parent().append('<span class="error">Please enter school name.</span>').addClass("has-error");
          return false;
      }

      if ($("#age_group").val() == "0") {
          $('#age_group').parent().append('<span class="error">Please select age group.</span>').addClass("has-error");
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

$("#age").on("keypress keyup blur",function (event) {
    $(this).val($(this).val().replace(/[^\d].+/, ""));
    if ((event.which < 48 || event.which > 57)) {
        event.preventDefault();
    }
});

$('#student_registration').on('click', function() {
   validation = checkForm();
    if (validation == false) {
      return false;
    }
    student = localStorage.getItem('student')

    let formData = new FormData($("#student-add")[0]);

    var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)

    if (token == null){
      window.location.href = "/"
  }


    $.ajax({
        url: "/students/"+student,
        method : "PUT",
        headers: { Authorization: 'Bearer ' + access.access },
        enctype: 'multipart/form-data',
        data : formData,
        contentType : false,
        processData: false,
        async : false,
        success: function (data) {
            console.log(data);
            window.location.href = "/student_list/"
        },
          error: function (data) {
            console.log(data);
          },
       });

});