$(document).ready(function () {
    var url = $(location).attr('href'),
    parts = url.split("/"),
    receiver_id = parts[parts.length-2];
    sender_id = parts[parts.length-3];
    var token = sessionStorage.getItem("UserDetails");
    var access_token = JSON.parse(token)

    $.ajax({
        type: 'get',
        url: '/messages/'+sender_id+'/'+receiver_id+'/',
        headers: { Authorization: 'Bearer ' + access_token.access },
        success: function(data) {
            jQuery.each(data.data, function (i, item) {

             if (item.sender.id == data.user) {
             html = `<div id=${item.id} class="chat_list" style="width:100%;float:right;background-color:#00ff7e33">
                  <div class="chat_people">
                    <div class="chat_img"> <img src="${item.sender.avatar}" alt="profile" style="border-radius: 50%;height:60px;width:60px;"> </div>
                    <div class="chat_ib">
                      <h5><span class="chat_date">${item.timestamp}</span></h5>
                    </div>
                    <div class="chat_msg">
                      <h5>You</h5>
                      <span>${item.message}</span>
                    </div>
                  </div>
                </div>`
             }
             else {
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
             }
                $('#board').append(html);
                scrolltoend();
            });
        },
        error: function(data) {
            if(data.status == 401){
                getAccessToken(url);
            }
            console.log(data);
           },
        });




    $.ajax({
        type: 'get',
        url: '/chat_history/'+sender_id+'/'+receiver_id+'/',
        headers: { Authorization: 'Bearer ' + access_token.access },
        success: function(data) {
            jQuery.each(data.data, function (i, item) {
                if (item.message != ""){
                    html = `<tr>
                            <td>${i}</td>
                            <td>
                                <u><a href="#" onclick="scrollToDiv(${item.id});">Your conversation with ${item.receiver.first_name} </a></u>
                            </td>
                        <tr>`
                        $('#chat-history').append(html);
                    }
                });
            },
        error: function(data) {
            if(data.status == 401){
                getAccessToken(url);
            }
            console.log(data);
           },
        });
});

    function scrollToDiv(id) {
        var container = $('#board');
        var scrollTo = $("#"+id);
        console.log(scrollTo);
            // Calculating new position
            // of scrollbar
            var position = scrollTo.offset().top
                - container.offset().top
                + container.scrollTop();

            // Animating scrolling effect
            container.animate({
                scrollTop: position
            });
//        $('#board').animate({
//            scrollTop: $('#'+id).offset().top + $('#'+id).height() / 2
//        });
    }


