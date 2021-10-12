// $(document).ready(function () {
//     // var course = localStorage.getItem('course')
//     var token = sessionStorage.getItem("UserDetails");
//     var access_token = JSON.parse(token)
//     if (token == null){
//         window.location.href = "/"
//     }

//     role = localStorage.getItem('role');
//     if (role === "Super User"){
//         $('.mobile').hide();
//         $('.postcode').hide();
//         $('.address').hide();
//     }

//     if (role == "Coach Manager") {
//         $('.coachfile').css('display','block');
//     }
//     if (role == "Head Coach") {
//         $('.coachfile').css('display','block');
//     }

//     var url = "/registration_part1/"
//     $.ajax({
//         type: 'get',
//         url: '/',
//         headers: { Authorization: 'Bearer ' + access_token.access },
//         success: function(data) {
//             if (role == "Super User"){
//                 localStorage.setItem('user_id', data.data.id);
//                 $('#userId').val(data.data.id);
//                 $('#profileImage').attr('src', data.data.avatar);
//                 $('#first_name').val(data.data.first_name);
//                 $('#last_name').val(data.data.last_name);
//                 $('#email').val(data.data.email);
//                 $('#mobile').val(data.data.mobile);
//                 $('#landline').val(data.data.landline);
//                 $('#post_code').val(data.data.postal_code);
//                 $('#address').val(data.data.address);
//             }
//             else {
//                 localStorage.setItem('user_id', data.data.user.id);
//                 $('#userId').val(data.data.user.id);
//                 $('#profileImage').attr('src', data.data.user.avatar);
//                 $('#first_name').val(data.data.user.first_name);
//                 $('#last_name').val(data.data.user.last_name);
//                 $('#email').val(data.data.user.email);
//                 $('#mobile').val(data.data.mobile);
//                 $('#landline').val(data.data.landline);
//                 $('#post_code').val(data.data.postal_code);
//                 $('#address').val(data.data.address);
//             }
//         },
//         error: function(data) {
//             if(data.status == 401){
//                 getAccessToken(url);
//             }
//         },
//     });
// });

// function checkForm(form) {
//     if ($("#password").val().length < 12) {
//        $('#password').parent().append('<span class="error">Password should be minimum 12 characters.</span>').addClass("has-error");
//        return false;
//     }
// }

// function checkPasswordMatch() {
//     var password = $("#new_password").val();
//     var confirmPassword = $("#confirm_password").val();

//     if (password != confirmPassword)
//         $("#divCheckPasswordMatch").html("Passwords do not match!");
//     else
//         $("#divCheckPasswordMatch").html("Passwords match.");
// }

// function allowEdit(){
//      $("#first_name,#last_name,#mobile,#landline,#post_code,#address").attr("readonly", false);
//      $('#first_name').focus();
// }



var counter = 0;
$(document).ready(function (){

    course = localStorage.getItem('course')
    $.ajax({
        type: 'get',
        url: '/edit_booking/'+course,
        // headers: { Authorization: 'Bearer ' + access.access },
        data: {},
        success: function(data) {
            $('#edit-booking').empty();
            console.log(data.data,"booking data");

            html = `BOOKINGS - ${data.data.course_type} - ${data.data.location}`
            $(`#booking_header`).append(html);
        } // success function ends here.

    });//ajax ends here

    }); //document.ready ends here

$(document).on('submit', '.customer-form', function (e) {
    var token = sessionStorage.getItem("UserDetails");
    var access_token = JSON.parse(token);

    alert("hello");
    // let formData = new FormData($("#update-password")[0]);
    $.ajax({
        url: "/registration_post/",
        method : "POST",
        enctype: 'multipart/form-data',
        headers: { Authorization: 'Bearer ' + access_token.access },
        data : formData,
        contentType : false,
        processData: false,
        async : false,
        success: function (data) {
            console.log(data);
            alert("data is added succesfully")
            // window.location.href = "/dashboard/"
        },
        error: function (data) {
            alert("data is not added succesfully")
            console.log(data);
        },
    });
})


var start_date 
$(document).ready(function (){

    course = localStorage.getItem('course')


    $.ajax({
        type: 'get',
        url: '/edit_booking/'+course,
        data: {

        },
        success: function(data) {

 
            $('#course_type').html(data.data.course_type);
            $('#start_date_with_day').html(data.data.start_date_with_day);
            $('#no_of_weeks').html(data.data.no_of_weeks);
            $('#default_course_rate').html(data.data.default_course_rate);
            $('#logo').attr('src',data.data.logo);
            $("#location").html(data.data.location);
            $("#day_filter").html(data.data.day_filter);
            $("#start_time").html(data.data.course_group);
            $("#end_time").html(data.data.course_group);
            $('#abcd').each(function(item){
                item.append(data.data.course_group.age)
            });

        },
        error: function(data) {
//            console.log(data);
                $('#error-msg').text(data.responseJSON.status);
            },
        });
    })


function go_back(){
    window.location.href = "/management_book_edit_page/"
}




function addCourse() {
    var token = sessionStorage.getItem("UserDetails");
    console.log("hello");
    var ab = localStorage.getItem("user_id");
    console.log(ab)
    // loan_limit = loan_limit - loan_amount;
    var access_token = JSON.parse(token)
    console.log(access_token.access)
    // localStorage.setItem('user_id', data.data.id);
    // localStorage.setItem('customer_id', data.data.id)
    var first_name = $("#first_name").val();
    var last_name = $("#last_name").val();
    var email = $("#email").val();
    var phone_number = $("#phone_number").val();
    var mobile = $("#mobile").val();
    var address = $("#address").val();
    var postcode = $("#postcode").val();

    var content={

        "user_id": localStorage.getItem("user_id"),
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "landline": phone_number,
        "mobile": mobile,
        "address": address,
        "postal_code": postcode,
    }
    $.ajax({
        url: "/registration_post/",
        method : "POST",
        // enctype: 'multipart/form-data',
        headers: { Authorization: 'Bearer ' + access_token.access },
        // data : formData,
        contentType : "application/json",
        processData: false,
        async : false,
        
        
        data: JSON.stringify(content),
        // type": "post",

        // "success": add_success
        success: function(data) {
            if($("#new-customer-checkbox").prop('checked') == true){
                localStorage.setItem("temporary_customer_form_id", data)
                window.location.href = "/registration_part2/"
            }
            else{
                alert("not checked");
            } 
        },
        error: function(data) {
            //            console.log(data);
            $('#error-msg').text(data.responseJSON.status);
            }
        // "error": add_error

    }); // ajax()
    // function add_success() {
    //     window.location.href = "/registration_part2/"
    // }

    // function add_error() {
    //     // window.location.href = "/management_book_edit_page/"
    //     alert("Could not add customer details!");
    //     return false
    // }

}


