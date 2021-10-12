$(document).ready(function () {
    var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)

    $.ajax({
        type: 'get',
        url: '/get_all_customers/',
        data: {

        },
        success: function(data) {
            jQuery.each(data.data, function (i, item) {
                $('#customer_id').append("<option value=" + item.id +">" + item.first_name + "</option>")
            });
        },
        error: function(data) {
               console.log(data);
            },
        });

    var data = JSON.parse(localStorage.getItem("course_detail"));

//    if (data !== null){
//        var qty = data[0].qty;
//        if(parseInt(qty) > 0){
//            $('#course').append("<option value=" + data[0].course_id +" selected>" + data[0].course_type + "</option>")
//        }
//    }
//    else{
        role = localStorage.getItem('role')

        if (role == "Customer"){
            $.ajax({
                type: 'get',
                url: '/get_purchased_courses/',
                headers: { Authorization: 'Bearer ' + access.access },
                success: function(data) {
                    jQuery.each(data.data, function (i, item) {
                        $('#course').append("<option value=" + item.course.course_type.id +">" + item.course.course_type.course_name + "</option>")
                    });
                },
                error: function(data) {
                     console.log(data);
                    },
            });
        }


        if (role !== "Customer"){
            $.ajax({
                type: 'get',
                url: '/course_data/',
                data: {

                },
                success: function(data) {
                    jQuery.each(data.data, function (i, item) {
                        $('#course').append("<option value=" + item.id +">" + item.course_type.course_name + "</option>")
                    });
                },
                error: function(data) {
                       console.log(data);
                    },
                });
            }
//    }



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
});

function checkForm(form) {

    if ($('#course').val() == null){
        $('#course_error').text("Please purchase course");
        return false
    }


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


    let formData = new FormData($("#student-add")[0]);

    var location_id = localStorage.getItem("location_id");

    formData.append('location', location_id);

    var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)

    if (token == null){
      window.location.href = "/"
    }


    $.ajax({
        url: "/students/",
        method : "POST",
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