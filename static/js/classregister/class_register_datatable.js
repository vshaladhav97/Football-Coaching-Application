var tableLoad = $(document).ready(function() {
    var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)
    // GetPermissions()
//    var userDetails = getValues('UserDetails')
//    var access = userDetails.access
//    $('#dropdownid').not('.disabled').formSelect();

//    if (localStorage.getItem("Supseruser") === "true") {
//        localStorage.removeItem("Superuser");
//    }
    $('#class-register-datatable').removeAttr('width').DataTable({
        dom: 'frtlip',
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/class_register_data/",
            "type": "GET",
            "headers": { Authorization: 'Bearer ' + access.access },
            "error": function(data) {
                // alert(data.status)
                if (data.status == 401) {
                    let get_url = "/class_register/"
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
            { "data": "location" },
            { "data": "address_line_1" },
            { "data": "town" },
            { "data": "country" },
            {
                "data": "id",
                "render": function(data) {
                    var all_perms = '<button class="edit_btn" style="width:70px;" onclick=getLocation('+ data +')><i class="fa fa-edit"></i>Edit</button> <button href="#deleteEmployeeModal" style="width:70px;" onclick="deleteLocation('+ data +')" class="delete" data-id="'+ data +'" data-toggle="modal"><i class="fa fa-trash" aria-hidden="true"></i> Delete</button>'
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
    var table = $("#location-datatable").dataTable().api();
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

function getLocation(id){
    localStorage.setItem('location',id)
    window.location.href = "/location_edit/"+id
}

function deleteLocation(id){
    $('#location_id').val(id);
    id = $('#location_id').val();
}

function deleteLocationRecord(){
     var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)
    id = $('#location_id').val();
    $.ajax({
        type: 'delete',
        url: '/locations/'+id,
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
