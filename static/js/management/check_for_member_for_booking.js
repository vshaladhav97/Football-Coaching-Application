$(document).ready(function () {
    
}); //document.ready ends here

var email_id;
function login() {

    if (IsEmail($("#staticEmail").val()) == false) {
        $('#staticEmail').parent().append('<span class="error">Invalid email. </span>').addClass("has-error");
        return false;
    }
    var email = $("#staticEmail").val();
    email_id = $("#staticEmail").val();
    var password = $("#inputPassword").val();
    //    if ($("#inputPassword").val().length < 12) {
    //        $('#inputPassword').parent().append('<span class="error">Password should be minimum 12 characters. </span>').addClass("has-error");
    ////        toastr.error("Password should be minimum 12 characters");
    //        return false;
    //    }

    $.ajax({
        type: 'get',
        url: '/customer_id_search/' + email_id,
        data: {

        },
        success: function (data) {
            localStorage.setItem("customer_id", data.data[0].id)

        },
        error: function (data) {

            $('#error-msg').text(data.responseJSON.status);
        },
    });

    $.ajax({
        type: 'post',
        url: '/login/',
        data: {
            "email": email,
            "password": password,
        },
        success: function (data) {
            console.log(data);
            localStorage.setItem("user_id", data.data.user);
            sessionStorage.setItem("UserDetails", data.data.tokens);
            localStorage.setItem('UserPermissions', data.data.user_permissions);
            localStorage.setItem('role', data.role);
            console.log('--------------------------------------')
            console.log(data.data)
            if (localStorage.getItem("course_type_name") == "Nursery")
                window.location.href = "/order_summary/"
            else if (localStorage.getItem("course_type_name") == "Evening Development"){
                window.location.href = "/child_selection_for_payement/"
            }
            else{
                window.location.href = "/week_booking/"
        }

        
        },
        error: function (data) {

            $('#error-msg').text(data.responseJSON.status);
        },
    }); 
}

function GoToCustomerRegistration() {
    window.location.href = "/customer_registration_part_1/"
}
document.getElementById("check_out_process").className = course_type_id;