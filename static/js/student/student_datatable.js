var tableLoad = $(document).ready(function() {
    var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)

    if (token == null) {
        window.location.href = "/login/"
    }
    // GetPermissions()
//    var userDetails = getValues('UserDetails')
//    var access = userDetails.access
//    $('#dropdownid').not('.disabled').formSelect();

//    if (localStorage.getItem("Supseruser") === "true") {
//        localStorage.removeItem("Superuser");
//    }
    $('#student-datatable').removeAttr('width').DataTable({
        dom: 'frtlip',
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/students/",
            "type": "GET",
            "headers": { Authorization: 'Bearer ' + access.access },
            "error": function(data) {
                // alert(data.status)
                if (data.status == 401) {
                    let get_url = "/student_list/"
                    getAccessToken(get_url);
                } else {
                    console.log(data);
//                    M.toast({ html: JSON.parse(data.responseText).message, classes: 'red rounded' })
                }
            }
        },
        "columns": [{
                "data": null,
                render: function(data, type, row, meta) {
                    return meta.row + meta.settings._iDisplayStart + 1;
                }
            },
            { "data": "first_name" },
            { "data": "last_name" },
            { "data": "age" },
            { "data": "school_name" },
            {
                "data": "id",
                "render": function(data) {
                    var all_perms = '<button class="edit_btn" onclick=getStudent('+ data +') style="width:70px;"><i class="fa fa-edit" aria-hidden="true"></i>Edit</button> <button href="#deleteEmployeeModal" onclick="deleteStudent('+ data +')" class="delete" data-id="'+ data +'" data-toggle="modal" style="width:70px;"><i class="fa fa-trash" aria-hidden="true"></i> Delete</button>'
                    return all_perms
//                    var retrievedData = localStorage.getItem("UserPermissions");
//                    var userPermissions = JSON.parse(retrievedData);
//
//                    if (!jQuery.isEmptyObject(userPermissions)) {
//
//                        var delete_user_flag = userPermissions.includes('delete_user_delete')
//                        var edit_user_flag = userPermissions.includes('edit_user_get')
//                        var view_user_flag = userPermissions.includes('view_user_get')
//
//                        if (delete_user_flag == true && edit_user_flag == true && view_user_flag == true) {
//                            return all_perms
//                        } else if (delete_user_flag == false && edit_user_flag == true && view_user_flag == true) {
//                            return edit_view
//                        } else if (delete_user_flag == false && edit_user_flag == false && view_user_flag == true) {
//                            return only_view
//                        }
//
//                    } else {
//                        return 'no action'
//                    }
                    // var all_perms = '<button class="edit_btn" id='+data+' onclick=getEditReport(id)><i class="material-icons prefix">mode_edit</i></button> <button class="view_btn" id='+data+' onclick=getViewReport(id)><i class="material-icons prefix">visibility</i></button><button class="delete_btn" id='+data+' onclick=getDeleteReport(id)><i class="material-icons prefix">delete</i></button> '
                    // return all_perms
                }
            },

        ],
        "columnDefs": [
            { "className": "dt-center", "targets": "_all" }
        ],
    });
    //lengthmenu -> add a margin to the right and reset clear
    $(".dataTables_length").css('clear', 'none');
    $(".dataTables_length").css('margin-right', '20px');

    //info -> reset clear and padding
    $(".dataTables_info").css('clear', 'none');
    $(".dataTables_info").css('padding', '0');
    // Call datatables, and return the API to the variable for use in our code
    // Binds datatables to all elements with a class of datatable
    var table = $("#student-datatable").dataTable().api();
    // var table = $('#user_datatable').DataTable();

    // table.columns.adjust().draw();
    // Grab the datatables input box and alter how it is bound to events
    $(".dataTables_filter input")
        .unbind() // Unbind previous default bindings
        .bind("input", function(e) { // Bind our desired behavior
            // If the length is 3 or more characters, or the user pressed ENTER, search
            if (this.value.length >= 3 || e.keyCode == 13) {
                // Call the API search function
                table.search(this.value).draw();
            }
            // Ensure we clear the search if they backspace far enough
            if (this.value == "") {
                table.search("").draw();
            }
            return;
        });


});

$.fn.dataTable.ext.errMode = function(settings, helpPage, message) {
    console.log(message);
};

function getStudent(id){
    localStorage.setItem('student',id)
    window.location.href = "/student_edit/"
}

function deleteStudent(id){
    $('#student_id').val(id);
    id = $('#student_id').val();
}

function deleteStudentRecord(){
     var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)
    id = $('#student_id').val();
    $.ajax({
        type: 'delete',
        url: '/students/'+id,
        headers: { Authorization: 'Bearer ' + access.access },
        data: {

        },
        success: function(data) {
            location.reload();
        },
        error: function(data) {
                console.log(data);
        },
    });
}
