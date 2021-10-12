function downloadCSV(){
    var token = sessionStorage.getItem("UserDetails");
    var access_token = JSON.parse(token)
    $.ajax({
        type: 'get',
        url: '/export_booked_classes/',
        headers: { Authorization: 'Bearer ' + access_token.access },
        data: {
            'message': $('#message').val(),
        },
        success: function(data) {
            location.replace("/export_booked_classes/");
        },
        error: function(data) {
               console.log(data);
            },
        });
}