var tableLoad = $(document).ready(function() {
    var token = sessionStorage.getItem("UserDetails");

    if (token == undefined) {
        console.log();
    }
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
//                    let get_url = "/class_register/"
//                    getAccessToken(get_url);

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
            { "data": "group" },
            { "data": "start_time" },
            { "data": "venue_name" },
            { "data": "date" },
            {
                "data": null,
                render: function(data, type, row, meta) {

                    if (row.status == "scheduled"){
                        var all_perms = '<button class="edit_btn" id=' + row.id + ' onclick=saveStatus('+ row.id +',"present") style="width:70px;">Present</button> <button  onclick=saveStatus('+row.id+',"absent") class="delete" style="width:70px;">Absent</button>'
                    }
                    else
                    {
                        var all_perms = ''+row.status
                    }


                    var only_view = ''+row.status

//                    return all_perms
                    var userPermissions = localStorage.getItem("UserPermissions");
                    if (!jQuery.isEmptyObject(userPermissions)) {
                        var student_present_absent_button = userPermissions.includes('student_present_absent_button')
                        if (student_present_absent_button == true) {
                            return all_perms
                        }
                        else {
                            return only_view
                        }
                    } else {
                        return ''
                    }
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
    var table = $("#class-register-datatable").dataTable().api();
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

    $('#weekly').on('click', function () {
        table.search("Eve").draw();
    });

    $('#nursery').on('click', function () {
        table.search("Nur").draw();
    });

    $('#holiday').on('click', function () {
        table.search("Hol").draw();
    });

    $('#all').on('click', function () {
        table.search("").draw();
    });


});

function saveStatus(id, status) {
    var token = sessionStorage.getItem("UserDetails");

    if (token == undefined) {
        console.log();
    }
    var access = JSON.parse(token)
    $.ajax({
        url: "/class_register_data/",
        method : "POST",
        headers: { Authorization: 'Bearer ' + access.access },
        data : {
            'id': id,
            'status': status,
        },
        success: function (data) {
            console.log(data);
            location.reload();
        },
        error: function (data) {
            console.log(data);
        },
    });
}