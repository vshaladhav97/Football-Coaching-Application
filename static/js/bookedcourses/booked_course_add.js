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

//       $('.select2').select2({
//
//        });

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


  $("#myModal").on("hidden.bs.modal", function () {
    window.location.href = "/booked_courses_page/"
    });

$('#save_book').on('click', function() {

    let formData = new FormData($("#book-course-add")[0]);

    var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)

    if (token == null){
      window.location.href = "/"
  }


    $.ajax({
        url: "/book_courses_add/",
        method : "POST",
        headers: { Authorization: 'Bearer ' + access.access },
        enctype: 'multipart/form-data',
        data : formData,
        contentType : false,
        processData: false,
        async : false,
        success: function (data) {
            console.log(data);
            window.location.href = "/booked_courses_page/"
            $('#myModal').modal('show');

        },
          error: function (data) {
            url = "/booked_courses_page/"
            getAccessToken()
            console.log(data);

          },
       });

});