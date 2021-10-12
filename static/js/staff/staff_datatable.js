var tableLoad = $(document).ready(function() {
    $('#staff-datatable').removeAttr('width').DataTable({
        dom: 'frtlip',
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/staff/",
            "type": "GET",
//            "headers": { Authorization: 'Bearer ' + access },
            "error": function(data) {
                // alert(data.status)
                if (data.status == 401) {
                    let get_url = "/dashboard//"
//                    getaccessTokenForUrl(get_url);

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
            { "data": "email" },
            { "data": "mobile" },
            {
                "data": "id",
                "render": function(data) {
                    var all_perms = '<button class="edit_btn" id=' + data + ' onclick=editStaff('+ data +') style="width:70px;"><i class="fa fa-edit">Edit</i></button> <button href="#deleteStaffModal" onclick="setStaff('+ data +')" class="delete" data-id="'+ data +'" data-toggle="modal" style="width:70px;"><i class="fa fa-trash" aria-hidden="true"></i> Delete</button>'
                    var edit_view = '<button class="edit_btn" id=' + data + ' onclick=editStaff('+ data +') style="width:70px;"><i class="material-icons prefix">Edit</i></button> <button class="view_btn" id=' + data + ' onclick=deleteStaff(id) style="width:70px;"><i class="material-icons prefix">visibility</i></button>'
                    var only_view = '<button class="view_btn" id=' + data + ' onclick=editStaff('+ data +') style="width:70px;"><i class="material-icons prefix">visibility</i></button>'

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
    var table = $("#staff-datatable").dataTable().api();
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
    M.toast({ html: message, classes: 'red rounded' })
};