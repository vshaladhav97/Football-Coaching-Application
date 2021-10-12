$(document).on('submit', '#update-role', function (e) {
    var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)
    var access_token = JSON.parse(access)

    var role = $('input[name="role"]:checked').attr('id');

    let formData = new FormData($("#update-role")[0]);

        $.ajax({
        url: "/update_role/",
        method : "POST",
        headers: { Authorization: 'Bearer ' + access_token.access },
        enctype: 'multipart/form-data',
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