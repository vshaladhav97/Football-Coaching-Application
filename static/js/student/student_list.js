$(document).ready(function () {
    var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)

    if (token == null) {
        window.location.href = "/login/"
    }


    $.ajax({
        type: 'get',
        url: '/students/',
        headers: { Authorization: 'Bearer ' + access.access },
        data: {},
        success: function(data) {
            jQuery.each(data.data, function (i, item) {
               html = '<tr>'+
//                      '<td>'+
//                      '<span class="custom-checkbox">'+
//                      '<input type="checkbox" id="checkbox1" name="options[]" value="1">'+
//                      '<label for="checkbox1"></label>'+
//                      '</span>'+
//                      '</td>'+
                      '<td>'+ item.first_name +'</td>'+
                      '<td>'+ item.last_name +'</td>'+
                      '<td>'+ item.age +'</td>'+
                      '<td>'+ item.school_name +'</td>'+
                      '<td>'+
                      '<a onclick="getStudent('+ item.id +')"  ata-toggle="modal"><i class="fa fa-pencil"></i>Edit</a>'+
                      '<br>'+
                      '<a href="#deleteEmployeeModal" onclick="deleteStudent('+ item.id +')" class="delete" data-id="'+ item.id +'" data-toggle="modal"><i class="fa fa-trash" aria-hidden="true"></i>Delete</a>'+
                      '</td>'+
                      '</tr>'

                $('#student-list').append(html);
            });
        },
        error: function(data) {
            console.log(data);
//                $('#error-msg').text(data.responseJSON.status);
            },
        });
});



