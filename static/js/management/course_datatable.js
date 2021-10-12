
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
    $('#course-datatable').removeAttr('width').DataTable({
        dom: 'frtlip',
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/management_courses_data/",
            "type": "GET",
            "headers": { Authorization: 'Bearer ' + access.access },
            "error": function(data) {
                if (data.status == 401) {
                    let get_url = "/dashboard/"
//                    getaccessTokenForUrl(get_url);

                } else {
                    console.log(data);
//                    M.toast({ html: JSON.parse(data.responseText).message, classes: 'red rounded' })
                }
            }
        },
        "columns": [
            {
                "data": null,
                render: function(data, type, row, meta) {
                    return meta.row + meta.settings._iDisplayStart + 1;
                }
            },
            { "data": "course_type" },
            {'data': 'no_of_weeks'},
            {'data': 'completed'},
            { "data": "start_date" },
            { "data": "end_date" },
            { "data": "course_description" },
            { "data": "location" },
            { "data": "default_course_rate" },
            {
                "data": null,
                render: function(data, type, row, meta) {
                    var all_perms = '<button class="edit_btn" onclick=getCourse('+ row.id +') style="width:124px;"><i class="fa fa-edit"> </i> Edit</button> <button href="#deleteEmployeeModal" style="width:124px;" onclick="deleteCourse('+ row.id +')" class="delete" data-id="'+ row.id +'" data-toggle="modal"><i class="fa fa-trash" aria-hidden="true"></i> Delete</button>'
                    var edit_view = '<button class="edit_btn" onclick=getCourse('+ row.id +') style="width:124px;"><i class="fa fa-edit"> </i> Edit</button>'
                    var approval_view = '<button style="width:124px;" onclick=approveCourse('+ row.id +')>'+ row.class_status +'</button>'
                    if (row.class_status == "Approval Needed"){
                        var all_perms = '<button class="edit_btn" onclick=getCourse('+ row.id +') style="width:124px;"><i class="fa fa-edit"> </i> Edit</button> <button href="#deleteEmployeeModal" style="width:124px;" onclick="deleteCourse('+ row.id +')" class="delete" data-id="'+ row.id +'" data-toggle="modal"><i class="fa fa-trash" aria-hidden="true"></i> Delete</button><button onclick=approveCourse('+ row.id +') style="width:124px;">'+ row.class_status +'</button>'
                    }
                    var userPermissions = localStorage.getItem('UserPermissions')
                    if(!jQuery.isEmptyObject(userPermissions)){
                        var delete_course_flag = userPermissions.includes('delete_course_delete')
                        var edit_course_flag = userPermissions.includes('edit_course_get')
                        var approve_course_flag = userPermissions.includes('approve_course_get')

                        if (delete_course_flag == true && edit_course_flag == true && approve_course_flag == true) {
                            return all_perms
                        } else if (delete_course_flag == false && edit_course_flag == true && approve_course_flag == true) {
                            return edit_view
                        } else if (delete_course_flag == false && edit_course_flag == false && approve_course_flag == true) {
                            return approval_view
                        }
                    }
                    else {
                        return 'no action';
                    }
                }
            },

        ],
        "fnCreatedRow": function(nRow, aData, iDataIndex) {
              $('td', nRow).css('background-color', 'white');
        },
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
    var table = $("#course-datatable").dataTable().api();
    // var table = $('#user_datatable').DataTable();

    // table.columns.adjust().draw();
    // Grab the datatables input box and alter how it is bound to events
    $(".dataTables_filter input")
        .unbind() // Unbind previous default bindings
        .bind("input", function(e) { // Bind our desired behavior
            // If the length is 3 or more characters, or the user pressed ENTER, search
            if (this.value.length >= 1 || e.keyCode == 13) {
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

$.fn.dataTable.ext.errMode = function(settings, helpPage, message) {
    console.log(message);
};

function getCourse(id){
    localStorage.setItem('course',id)
    window.location.href = "/management_courses_edit_page/"
}

function deleteCourse(id){
    $('#course_id').val(id);
    id = $('#course_id').val();
}

function deleteCourseRecord(){
    var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)
    id = $('#course_id').val();
    $.ajax({
        type: 'delete',
        url: '/course_detail_data/'+id,
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

function approveCourse(id){
    var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)
    $.ajax({
        type: 'post',
        url: '/approve_course/'+id,
        headers: { Authorization: 'Bearer ' + access.access },
        success: function(data) {
            location.reload();
        },
        error: function(data) {
                console.log(data);
        },
    });
}
