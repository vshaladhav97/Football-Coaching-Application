$(document).ready(function () {
    var token = sessionStorage.getItem("UserDetails");
    var access_token = JSON.parse(token);

    $.ajax({
        type: 'get',
        url: '/get_all_documents/',
        headers: { Authorization: 'Bearer ' + access_token.access },
        data: {

        },
        success: function(data) {
            jQuery.each(data.data, function (i, item) {
                html = '<a target="_blank" href="'+ item.file_path + '"> Download "'+ item.file_path +'</a><br>';
                $('#document').append(html);
            });
        },
        error: function(data) {
                url = '/document/';
                getAccessToken(url);
               console.log(data);
        },
    });
})