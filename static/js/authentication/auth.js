function getAccessToken(url) {
    var token = sessionStorage.getItem("UserDetails");
    var refresh_token = JSON.parse(token);
    $.ajax({
        type: 'post',
        url: '/refresh/',
        data: {
            'refresh': refresh_token.refresh,
        },
        success: function (data) {
            var user_details = sessionStorage.getItem("UserDetails");
            var refresh = JSON.parse(user_details);
            refresh.access = data.access;
            sessionStorage.setItem("UserDetails", JSON.stringify(refresh));

            setTimeout(function () {
                window.location.href = url;
            }, 500);
        },
        error: function (data) {
            console.log(data);
            alert(data.responseText);
        },
    });
}


function setAccessToken() {
    var token = sessionStorage.getItem("UserDetails");
    var refresh_token = JSON.parse(token);
    $.ajax({
        type: 'post',
        url: '/refresh/',
        data: {
            'refresh': refresh_token.refresh,
        },
        success: function (data) {
            var user_details = sessionStorage.getItem("UserDetails");
            var refresh = JSON.parse(user_details);
            refresh.access = data.access;
            sessionStorage.setItem("UserDetails", JSON.stringify(refresh));
        },
        error: function (data) {
            console.log(data);
        },
    });
}



function IsEmail(email) {
    var regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if (!regex.test(email)) {
        return false;
    } else {
        return true;
    }
}

$('#twitter-button').on('click', function () {
    // Initialize with your OAuth.io app public key
    OAuth.initialize('HwAr2OtSxRgEEnO2-JnYjsuA3tc');
    // Use popup for OAuth
    OAuth.popup('twitter').then(twitter => {
        console.log('twitter:', twitter);
        // Prompts 'welcome' message with User's email on successful login
        // #me() is a convenient method to retrieve user data without requiring you
        // to know which OAuth provider url to call
        twitter.me().then(data => {
            console.log('data:', data);
            alert('Twitter says your email is:' + data.email + ".\nView browser 'Console Log' for more details");
        });
        // Retrieves user data from OAuth provider by using #get() and
        // OAuth provider url
        twitter.get('/1.1/account/verify_credentials.json?include_email=true').then(data => {
            console.log('self data:', data);
        })
    });
})

var email_id;
function login() {

    if (IsEmail($("#login_email").val()) == false) {
        $('#login_email').parent().append('<span class="error">Invalid email. </span>').addClass("has-error");
        return false;
    }
    var email = $("#login_email").val();
    email_id = $("#staticEmail").val();
    var password = $("#login_password").val();
 

    $.ajax({
        type: 'get',
        url: '/customer_id_search/' + email,
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
            window.location.href = "/dashboard/"


        },
        error: function (data) {
            
            $('#error-msg').text(data.responseJSON.status);
        },
    });
}




function signOut() {

    if (localStorage.getItem('authenticator') == "gmail") {
        var auth2 = gapi.auth2.getAuthInstance();
        auth2.signOut().then(function () {
            console.log('User signed out.');
        });
    }
    //    else
    //    {
    // var token = sessionStorage.getItem("UserDetails");
    // var access_token = JSON.parse(token)
    $.ajax({
        type: 'post',
        url: '/logout/',
        // headers: { Authorization: 'Bearer ' + access_token.access },
        // data: {
        //     "refresh": access_token.refresh,
        // },
        success: function (data) {
            localStorage.clear();
            sessionStorage.clear();
            console.log('--------------------------------------')
            console.log(data.data)
            window.location.href = "/"
        },
        error: function (data) {
            url = "/"
            getAccessToken(url);
            console.log(data.status)
        },
    });
    //    }
}

$("#myModal").on("hidden.bs.modal", function () {
    localStorage.clear();
    window.location.href = "/login/"
});

function changePassword() {
    var token = sessionStorage.getItem("UserDetails");
    var access_token = JSON.parse(token);
    var old_password = $('#old_password').val();
    var new_password = $('#new_password').val();
    $.ajax({
        type: 'post',
        url: '/change_password/',
        headers: { Authorization: 'Bearer ' + access_token.access },
        data: {
            "old_password": old_password,
            "new_password": new_password,
        },
        success: function (data) {
            console.log('--------------------------------------')
            console.log(data.data)
            $('#myModal').modal('show');

        },
        error: function (data) {
            alert(data.responseJSON.old_password);
            location.reload();
            console.log(data.responseJSON.old_password);
        },
    });
}
