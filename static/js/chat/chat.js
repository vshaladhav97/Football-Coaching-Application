$(document).ready(function () {
    var token = sessionStorage.getItem("UserDetails");
    var access_token = JSON.parse(token)

    $.ajax({
        type: 'get',
        url: '/chat_users/',
        headers: { Authorization: 'Bearer ' + access_token.access },
        success: function(data) {
            jQuery.each(data.data, function (i, item) {
                html = `<a href="/chat/${data.user}/${item.id}" id="user${item.id}">
                         <article class="post-classic">
                            <div class="post-classic-aside">
                                <img src="${item.avatar}" alt="" style="border-radius: 50%;height:60px;width:60px;">
                            </div>
                            <div class="post-classic-main">
                              <p class="post-classic-title">
                                ${item.first_name}
                              </p>
                            </div>
                        </article>
                        </a>`
                $('#chat-users').append(html);
            });
        },
        error: function(data) {
            console.log(data);
           },
        });
});

var text_box = '<div class="card-panel right" style="width: 75%; position: relative">' +
        '<div style="position: absolute; top: 0; left:3px; font-weight: bolder" class="title">{sender}</div>' +
        '{message}' +
        '</div>';

function scrolltoend() {
    $('#board').stop().animate({
        scrollTop: $('#board')[0].scrollHeight
    }, 800);
}

function send(sender, receiver, message) {
    $.post('/api/messages/', '{"sender": "'+ sender +'", "receiver": "'+ receiver +'","message": "'+ message +'" }', function (data) {
        console.log(data);
        var box = text_box.replace('{sender}', "You");
        box = box.replace('{message}', message);
        $('#board').append(box);
        scrolltoend();
    })
}

function receive() {
    var url = $(location).attr('href');
    parts = url.split("/");
    receiver_id = parts[parts.length-2];
    sender_id = parts[parts.length-3];
    var token = sessionStorage.getItem("UserDetails");
    var access_token = JSON.parse(token)
    headers = { Authorization: 'Bearer ' + access_token.access }
     $.ajax({
        type: 'get',
        url: '/api/messages/'+ sender_id + '/' + receiver_id,
        headers: { Authorization: 'Bearer ' + access_token.access },
        success: function(data)  {
            console.log(data);
            if (data.length !== 0)
            {
                jQuery.each(data, function (i, item) {
                    html  =  `<div id=${item.id} class="chat_list" style="width:100%;background-color:white;float:left">
                              <div class="chat_people">
                                <div class="chat_img_sent_from"> <img src="${item.sender.avatar}" alt="profile" style="border-radius: 50%;height:60px;width:60px;"> </div>
                                <div class="chat_ib_from">
                                  <h5><span class="chat_date">${item.timestamp}</span></h5>

                                </div>
                                <div class="chat_msg">
                                  <h5>${item.sender.first_name}</h5>
                                  <span>${item.message}</span>
                                </div>
                              </div>
                            </div>`
                    $('#board').append(html);
                    scrolltoend();
                });
            }
        },
        error: function(data) {
            if (data.status == 401) {
                setAccessToken();
            }
            console.log(data);
           },
    })
}
