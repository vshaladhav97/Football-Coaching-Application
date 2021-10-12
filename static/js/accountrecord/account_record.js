$(document).ready(function () {
    var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)

    if (token == null){
      window.location.href = "/"
    }
    var url = '/account_record/'

    $.ajax({
        type: 'get',
        url: '/account_record_data/',
        headers: { Authorization: 'Bearer ' + access.access },
        data: {},
        success: function(data) {
            jQuery.each(data.data, function (i, item) {

               html = `<li>
                        <div class="comments" style="padding: 10px;">
                              <p class="font-weight-bold">
                                ${item.user.first_name}
                                <span class=" text-muted font-weight-normal">
                                  ${item.created_on}
                                </span>
                              </p>
                            ${item.comment}
                        </div>
                    </li>`

                $('.list-items').append(html);
            });
        },
        error: function(data) {
            if(data.status == 401)
            {
                getAccessToken(url)
            }
            console.log(data);
//                $('#error-msg').text(data.responseJSON.status);
            },
        });

})


function addComment(){
    if ($("#comment").val() == "") {
          return false;
      }
    var comment = $('#comment').val();
    var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)
    $.ajax({
        type: 'post',
        url: '/account_record_data/',
        headers: { Authorization: 'Bearer ' + access.access },
        data: {
            'comment': comment,
        },
        success: function(data) {
            console.log(data);
            location.reload();
        },
        error: function(data) {
            console.log(data);
           },
        });
}
