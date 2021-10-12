$(document).ready(function () {
    var token = sessionStorage.getItem("UserDetails");
    var access_token = JSON.parse(token)
    if (token == null){
        window.location.href = "/"
    }

    role = localStorage.getItem('role');
    if (role === "Super User"){
        $('.mobile').hide();
        $('.postcode').hide();
        $('.address').hide();
    }

    if (role == "Coach Manager") {
        $('.coachfile').css('display','block');
    }
    if (role == "Head Coach") {
        $('.coachfile').css('display','block');
    }

    var url = "/profile/"
    $.ajax({
        type: 'get',
        url: '/profile_data/',
        headers: { Authorization: 'Bearer ' + access_token.access },
        success: function(data) {
            if (role == "Super User"){
                localStorage.setItem('user_id', data.data.id);
                $('#userId').val(data.data.id);
                $('#profileImage').attr('src', data.data.avatar);
                $('#first_name').val(data.data.first_name);
                $('#last_name').val(data.data.last_name);
                $('#email').val(data.data.email);
            }
            else {
                localStorage.setItem('user_id', data.data.user.id);
                $('#userId').val(data.data.user.id);
                $('#profileImage').attr('src', data.data.user.avatar);
                $('#first_name').val(data.data.user.first_name);
                $('#last_name').val(data.data.user.last_name);
                $('#email').val(data.data.user.email);
                $('#mobile').val(data.data.mobile);
                $('#landline').val(data.data.landline);
                $('#post_code').val(data.data.postal_code);
                $('#address').val(data.data.address);
            }
        },
        error: function(data) {
            if(data.status == 401){
                getAccessToken(url);
            }
        },
    });
});

function checkForm(form) {
    if ($("#password").val().length < 12) {
       $('#password').parent().append('<span class="error">Password should be minimum 12 characters.</span>').addClass("has-error");
       return false;
    }
}

function checkPasswordMatch() {
    var password = $("#new_password").val();
    var confirmPassword = $("#confirm_password").val();

    if (password != confirmPassword)
        $("#divCheckPasswordMatch").html("Passwords do not match!");
    else
        $("#divCheckPasswordMatch").html("Passwords match.");
}

function allowEdit(){
     $("#first_name,#last_name,#mobile,#landline,#post_code,#address").attr("readonly", false);
     $('#first_name').focus();
}

$(document).on('submit', '#update-password', function (e) {
    var token = sessionStorage.getItem("UserDetails");
    var access_token = JSON.parse(token);
    let formData = new FormData($("#update-password")[0]);
    $.ajax({
        url: "/profile_data/",
        method : "POST",
        enctype: 'multipart/form-data',
        headers: { Authorization: 'Bearer ' + access_token.access },
        data : formData,
        contentType : false,
        processData: false,
        async : false,
        success: function (data) {
            console.log(data);
            window.location.href = "/dashboard/"
        },
        error: function (data) {
            console.log(data);
        },
    });
})