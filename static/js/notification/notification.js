$(document).ready(function () {

    role = localStorage.getItem("role");
    if (role == "Customer") {
        $("#chat-button").hide();
    }
    $('.select.select2').select2();


    $.ajax({
        type: 'get',
        url: '/users/',
//        headers: { Authorization: 'Bearer ' + access_token.access },
        data: {

        },
        success: function(data) {
            jQuery.each(data.data, function (i, item) {
                $('#user').append("<option value=" + item.id +">" + item.first_name + "</option>")
            });
        },
        error: function(data) {
               if (data.status == 401){
                    setAccessToken();
               }
            },
        });

    var token = sessionStorage.getItem("UserDetails");
    var access_token = JSON.parse(token)
    $.ajax({
        type: 'get',
        url: '/notifications_data/',
        headers: { Authorization: 'Bearer ' + access_token.access },
        success: function(data) {
            
            jQuery.each(data.data, function (i, item) {
                $(".chat_notification").hide();
                html = `<tr>
                            <td>
                                <span style="text-align:left;">
                                <i aria-hidden="true" class="fa fa-bullhorn fa-lg"></i>
                                ${item.message}</span>
                                <span>
                                    ${item.created_date}
                                </span>
                            </td>
                        </tr>`
                $('#notifications-listing').append(html);
                $('#items').append("<li value=" + item.id +">" + item.from_user_id + ":"+  item.message + "</li>")
            });
        },
        error: function(data) {
               console.log(data);
               if (data.status == 401){
                    setAccessToken();
               }
            },
        });


    $.ajax({
        type: 'get',
        url: '/inbox_data/',
        headers: { Authorization: 'Bearer ' + access_token.access },
        success: function(data) {
            jQuery.each(data.data, function (i, item) {
                html = `<tr>
                            <td>
                                <span style="text-align:left;">
                                <img src=${item.receiver.avatar} height=40 width=40>
                                </span>
                            </td>
                            <td style="text-align:left;">
                                    ${item.message}<br>
                                    <a href="/chat/${item.sender.id}/${item.receiver.id}">View more</a>
                            </td>
                            <td>
                                 <span>
                                    ${item.timestamp}
                                </span>
                            </td>
                        </tr>`
                $('#inbox-listing').append(html);
            });
        },
        error: function(data) {
               console.log(data);
            },
        });


    $.ajax({
        type: 'post',
        url: '/notification_viewed/',
        headers: { Authorization: 'Bearer ' + access_token.access },
        success: function(data) {
            console.log(data);
        },
        error: function(data) {
               console.log(data);
            },
        });




 })


function sendNotification(){
    var token = sessionStorage.getItem("UserDetails");
    var access_token = JSON.parse(token)
    $.ajax({
        type: 'post',
        url: '/notifications_data/',
        headers: { Authorization: 'Bearer ' + access_token.access },
        data: {
            'message': $('#message').val(),
            'user_id': $('#user').val(),
        },
        success: function(data) {
            location.reload();
        },
        error: function(data) {
               console.log(data);
            },
        });
}