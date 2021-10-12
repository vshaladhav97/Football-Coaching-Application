
$(document).ready(function () {
    $.ajax({
        type: 'get',
        url: '/course_type/',
        data: {

        },
        success: function(data) {
            jQuery.each(data.data, function (i, item) {
                $('#course_type').append("<option value=" + item.id +">" + item.course_name + "</option>")
            });
        },
        error: function(data) {
            console.log(data);
//                $('#error-msg').text(data.responseJSON.status);
            },
        });

    $.ajax({
        type: 'get',
        url: '/event_type/',
        data: {

        },
        success: function(data) {
            jQuery.each(data.data, function (i, item) {
                $('#event_type').append("<option value=" + item.id +">" + item.type_name + "</option>")
            });
        },
        error: function(data) {
            console.log(data);
//                $('#error-msg').text(data.responseJSON.status);
            },
        });

    $.ajax({
        type: 'get',
        url: '/class_status/',
        data: {

        },
        success: function(data) {
            jQuery.each(data.data, function (i, item) {
                $('#class_status').append("<option value=" + item.id +">" + item.status_name + "</option>")
            });
        },
        error: function(data) {
            console.log(data);
//                $('#error-msg').text(data.responseJSON.status);
            },
        });

    $.ajax({
        type: 'get',
        url: '/months/',
        data: {

        },
        succesmanagement_courses_edit_pages: function(data) {
            jQuery.each(data.data, function (i, item) {
                $('#months').append("<option value=" + item.id +">" + item.month + "</option>")
            });
        },
        error: function(data) {
            console.log(data);
//                $('#error-msg').text(data.responseJSON.status);
            },
        });

    $.ajax({
        type: 'get',
        url: '/get_all_locations/',
        data: {

        },
        success: function(data) {
            jQuery.each(data.data, function (i, item) {
                $('.location').append("<option value=" + item.id +">" + item.location + "</option>")
            });
        },
        error: function(data) {
            console.log(data);
//                $('#error-msg').text(data.responseJSON.status);
            },
        });

//     $.ajax({
//         type: 'get',
//         url: '/get_all_coach/',
//         data: {

//         },
//         success: function(data) {
//             jQuery.each(data.data, function (i, item) {
//                 $('.coach').append("<option value=" + item.id +">" + item.first_name + "</option>")
//             });
//         },
//         error: function(data) {
//             console.log(data);
// //                $('#error-msg').text(data.responseJSON.status);
//             },
//         });


    course = localStorage.getItem('course')
    $.ajax({
        type: 'get',
        url: '/course_detail_data/'+course,
        data: {

        },
        success: function(data) {
            $('#course_description').val(data.data.course_description);
            $('#default_course_rate').val(data.data.default_course_rate);
            $('#start_date').val(data.data.start_date);
            $('#end_date').val(data.data.end_date);
            if(data.data.event_type != null){

                $('#event_type').val(data.data.event_type.id);
            }
            $('#course_type').val(data.data.course_type.id);
            $('#class_status').val(data.data.class_status.id);
            
// //            $('#school_name').val(data.message.school_name);
//             $('#class_status').val(data.data.class_status.id);
//             $('#class_status').focus();
            
//            $('#age-group').val(data.message.age_group.id);
            $('#select2-chosen-1').html(data.data.course_type.course_name);
            if(data.data.event_type != null){
                $('#select2-chosen-2').html(data.data.event_type.type_name);
            }
            $('#select2-chosen-3').html(data.data.class_status.status_name);
        },
        error: function(data) {
//            console.log(data);
                $('#error-msg').text(data.responseJSON.status);
            },
        });


    $(document).on('click', '.add', function(){
          html = `<tr>
                <td>
                    <select class="form-control location" id="location[]" name="location[]">
                        <option>Select Locations</option>
                    </select>
                </td>
                <td>
                    <select class="form-control coach" id="coach[]" name="coach[]">
                        <option>Select Coach</option>
                    </select>
                </td>
                <td>
                    <input type="text" class="form-control total_seats" id="total_seats[]" name="total_seats[]" name="total_seats[]">
                </td>
                <td>
                    <button type="button" name="remove" class="btn btn-danger btn-sm remove"><span class="glyphicon glyphicon-minus"></span>Remove</button>
                </td>
                </tr>`
          $('#coach-mapping').append(html);

          $.ajax({
        type: 'get',
        url: '/get_all_locations/',
        data: {

        },
        success: function(data) {
            jQuery.each(data.data, function (i, item) {
                $('.location').append("<option value=" + item.id +">" + item.location + "</option>")
            });
        },
        error: function(data) {
            console.log(data);
//                $('#error-msg').text(data.responseJSON.status);
            },
        });

            $.ajax({
        type: 'get',
        url: '/get_all_coach/',
        data: {

        },
        success: function(data) {
            jQuery.each(data.data, function (i, item) {
                $('.coach').append("<option value=" + item.id +">" + item.first_name + "</option>")
            });
        },
        error: function(data) {
            console.log(data);
//                $('#error-msg').text(data.responseJSON.status);
            },
        });
    });


     $(document).on('click', '.remove', function(){
          $(this).closest('tr').remove();
     });




    // $('#coach-mapping').append(html);
});


function addRow(){
     html = `<tr>
                <td>
                    <select class="form-control location" id="location[]" name="location[]">
                        <option>Select Locations</option>
                    </select>
                </td>
                <td>
                    <select class="form-control coach" id="coach[]" name="coach[]">
                        <option>Select Coach</option>
                    </select>
                </td>
                <td>
                    <input type="text" class="form-control total_seats" id="total_seats" name="total_seats" name="total_seats[]">
                </td>
                <td>
                    <button onclick="addRow();" type="button">Add</button>
                </td>
                </tr>`


    $('#coach-mapping').append(html);

        $.ajax({
        type: 'get',
        url: '/get_all_locations/',
        data: {

        },
        success: function(data) {
            jQuery.each(data.data, function (i, item) {
                $('.location').append("<option value=" + item.id +">" + item.location + "</option>")
            });
        },
        error: function(data) {
            console.log(data);
//                $('#error-msg').text(data.responseJSON.status);
            },
        });

    $.ajax({
        type: 'get',
        url: '/get_all_coach/',
        data: {

        },
        success: function(data) {
            jQuery.each(data.data, function (i, item) {
                $('.coach').append("<option value=" + item.id +">" + item.first_name + "</option>")
            });
        },
        error: function(data) {
            console.log(data);
//                $('#error-msg').text(data.responseJSON.status);
            },
        });

    return false;

}


$('#course_submit').on('click', function() {

    months = $('#months').val()
    locations = []
    $('.location').each(function(){
           var count = 1;
           if($(this).val() == '')
           {
            // error += "<p>Select location at "+count+" Row</p>";
            return false;
           }
           locations.push($(this).val())
           count = count + 1;
    });
    coachs = []
    $('.coach').each(function(){

           var count = 1;
        //    alert($(this).val())
           if($(this).val() == '')
           {
            // error += "<p>Select coach at "+count+" Row</p>";
            return false;
           }
           coachs.push($(this).val())
           count = count + 1;
    });
    total_seats = []
    $('.total_seats').each(function(){
           var count = 1;
           if($(this).val() == '')
           {
            // error += "<p>Select coach at "+count+" Row</p>";
            return false;
           }
           total_seats.push($(this).val())
           count = count + 1;
    });
//   validation = checkForm();
//    if (validation == false) {
//      return false;
//    }



    let formData = new FormData($("#course-edit")[0]);

    formData.set('months', months);
    formData.set('locations', locations);
    formData.set('coachs', coachs);
    formData.set('total_seats', total_seats);
    for(var pair of formData.entries()) {
        console.log(pair[0]+ ', '+ pair[1]);
     }


    var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)

    if (token == null){
      window.location.href = "/"
  }

    course = localStorage.getItem('course')
    $.ajax({
        url: "/course_edit_functionality/" + course,
        method : "PUT",
        headers: { Authorization: 'Bearer ' + access.access },
        enctype: 'multipart/form-data',
        data : formData,
        contentType : false,
        processData: false,
        async : false,
        success: function (data) {
            console.log(data);
            window.location.href = "/listing/"
        },
          error: function (data) {
            console.log(data);
          },
       });

});