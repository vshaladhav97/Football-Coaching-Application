$(document).ready(function () {
    var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)

    if (token == null){
      window.location.href = "/"
  }


        $.ajax({
        type: 'get',
        url: '/get_all_students/',
        headers: { Authorization: 'Bearer ' + access.access },
        data: {

        },
        success: function(data) {
            jQuery.each(data.data, function (i, item) {
                $('#student').append("<option value=" + item.id +">" + item.first_name + "</option>")
            });
        },
        error: function(data) {
               console.log(data);
            },
        });

    $.ajax({
        type: 'get',
        url: '/get_all_locations/',
        data: {

        },
        success: function(data) {
            jQuery.each(data.data, function (i, item) {
                $('#location').append("<option value=" + item.id +">" + item.location + "</option>")
            });
        },
        error: function(data) {
               console.log(data);
            },
        });

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
    course = localStorage.getItem('booked_course')
    $.ajax({
        type: 'get',
        url: '/book_course/'+course,
        data: {

        },
        success: function(data) {
            $('#start_date').text(data.data.start_date);
            $('#end_date').text(data.data.end_date);
            $('#select2-chosen-3').html(data.data.student);
            $('#select2-chosen-4').html(data.data.course);
            $('#select2-chosen-5').html(data.data.location);
//            $('#select2-chosen-3').html(data.message.age_group.age_group_text);
        },
        error: function(data) {
            console.log(data);
//                $('#error-msg').text(data.responseJSON.status);
            },
        });
});


//function checkForm(form) {
//
//     if ($("#first_name").val() == "") {
//          $('#first_name').parent().append('<span class="error">Please enter first name.</span>').addClass("has-error");
//          return false;
//      }
//
//      if ($("#last_name").val() == "") {
//          $('#last_name').parent().append('<span class="error">Please enter last name.</span>').addClass("has-error");
//          return false;
//      }
//
//      if ($("#age").val() == "") {
//          $('#age').parent().append('<span class="error">Please enter age.</span>').addClass("has-error");
//          return false;
//      }
//
//      if ($("#school_name").val() == "") {
//          $('#school_name').parent().append('<span class="error">Please enter school name.</span>').addClass("has-error");
//          return false;
//      }
//
//      if ($("#age_group").val() == "0") {
//          $('#age_group').parent().append('<span class="error">Please select age group.</span>').addClass("has-error");
//          return false;
//      }
//  }
//
//
//$("#first_name,#last_name").on("keypress", function (event) {
//    var regex = new RegExp("^[a-zA-Z \b]+$");
//    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
//    if (!regex.test(key)) {
//      event.preventDefault();
//      return false;
//    }
//});
//
//$("#age").on("keypress keyup blur",function (event) {
//    $(this).val($(this).val().replace(/[^\d].+/, ""));
//    if ((event.which < 48 || event.which > 57)) {
//        event.preventDefault();
//    }
//});

$('#save_book').on('click', function() {
//   validation = checkForm();
//    if (validation == false) {
//      return false;
//    }
    booked_course = localStorage.getItem('booked_course')

    let formData = new FormData($("#book-course-edit")[0]);

    var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)

    if (token == null){
      window.location.href = "/"
  }


    $.ajax({
        url: "/book_course/"+booked_course,
        method : "PUT",
        headers: { Authorization: 'Bearer ' + access.access },
        enctype: 'multipart/form-data',
        data : formData,
        contentType : false,
        processData: false,
        async : false,
        success: function (data) {
            console.log(data);
            window.location.href = "/booked_courses_page/"
        },
          error: function (data) {
            console.log(data);
          },
       });

});