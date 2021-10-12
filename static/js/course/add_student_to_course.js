$(document).ready(function () {

    var bookedId = localStorage.getItem('bookedCourse')

    if (bookedId !== null){
        $('#bookedCourse'+bookedId).css('display', "block");
    }

    var data = JSON.parse(localStorage["course_detail"]);
    var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)

    var qty = data[0].qty;
    var i;
    for (i = 0; i < parseInt(qty); i++) {
               html = '<tr>'+
                      '<td>'+
                      '<select class="select select-minimal student" data-placeholder="Select an option" id="student'+ i +'"  onchange="student('+ i +')" data-dropdown-class="select-minimal-dropdown" style="min-width: 124px">'+
                       '<option value="newest first" selected="">Student</option>'+
                      '</select>'+
                      '</td>'+
                      '<td>'+ data[0].course_type +'</td>'+
                      '<td>'+
                      '<button class="btn btn-primary" id="bookCourse'+ i +'" onclick="bookCourse('+ data[0].course_id +' ,'+ i +')">Book</button>'+
                      '<button class="btn btn-primary" id="bookedCourse'+ i +'" style="display:none;">Already Booked</button>'+
                      '</td>'+
                      '</tr>'

                $('#student-list').append(html);
            }
    $.ajax({
        type: 'get',
        url: '/get_all_students/',
        headers: { Authorization: 'Bearer ' + access.access },
        data: {},
        success: function(data) {
            jQuery.each(data.data, function (i, item) {
             $('.student').append("<option value=" + item.id +">" + item.first_name + "</option>")
            });
        },
        error: function(data) {
//            console.log(data);
                $('#error-msg').text(data.responseJSON.status);
            },
        });
})


function student(id){
    localStorage.setItem('student',id);
}

function bookCourse(id, bookId){
    var token = sessionStorage.getItem("UserDetails");
    var location = localStorage.getItem('location_id')
    var access = JSON.parse(token)
    student = localStorage.getItem('student');
    var studentVal = $("#student"+student).val();
    $.ajax({
        type: 'post',
        url: '/book_course/',
        headers: { Authorization: 'Bearer ' + access.access },
        data: {
            'student': studentVal,
            'course': id,
            'location': location,
        },
        success: function(data) {
            console.log(data);
            $('#bookCourse'+bookId).hide();
            $('#bookedCourse'+bookId).css('display', "block");
            localStorage.setItem('bookedCourse', bookId);
            var course_detail = JSON.parse(localStorage.course_detail);
            course_detail[0].qty = course_detail[0].qty - 1
            console.log(course_detail[0].qty);
            localStorage.setItem("course_detail", JSON.stringify(course_detail));
            localStorage.removeItem('course_id');
        },
        error: function(data) {
                $('#error-msg').text(data.responseJSON.status);
        },
    });
}