$("#child_edit").hide();

$.ajax({
  type: "get",
  url: "/student_parent_count/",
  success: function(data){
    html = `Parents(${data[0].total_customer})`
    $("#parent_count").append(html);  
    html = `Children(${data[0].total_student})`
    $("#child_count").append(html);  
  }
})

var whichScope;

var tableLoad = $(document).ready(function () {
  
  $('#customer-datatable').removeAttr('width').DataTable({
    dom: 'frtlip',
    "processing": true,
    "serverSide": true,
    "ajax": {
      "url": "/customers/",
      "type": "GET",

      "error": function (data) {

        if (data.status == 401) {
          let get_url = "/dashboard//"

        } else {
          console.log(data);
        }
      }
    },
    "columns": [{
      "data": null,
      render: function (data, type, row, meta) {
        return meta.row + meta.settings._iDisplayStart + 1;
      }
    },
    {
      "data": 'profile_image',
      "render": function (data) {

        if (data) {
          return '<img src="' + data + '"    style="width: 100px;height: 80px;">';
        } else {
          return 'No data'
        }
      }
    },
    { "data": "first_name" },
    { "data": "last_name" },
    { "data": "status" },
    { "data": "town" },
    { "data": "postal_code" },
    { "data": "address" },
    {
      "data": "id",
      "render": function (data) {
        //    console.log(data)

        var all_perms = '<button class="edit_btn" id=' + data + ' onclick=editUser(' + data + ') style="width:70px;"><i class="fa fa-edit">Edit</i></button> <button href="#deleteEmployeeModal" onclick="setUser(' + data + ')" class="delete" data-id="' + data + '" data-toggle="modal" style="width:70px;"><i class="fa fa-trash" aria-hidden="true"></i> Delete</button>'
        var edit_view = '<button class="edit_btn" id=' + data + ' onclick=editUser(' + data + ') style="width:70px;"><i class="material-icons prefix">Edit</i></button> <button class="view_btn" id=' + data + ' onclick=deleteUser(id) style="width:70px;"><i class="material-icons prefix">visibility</i></button>'
        var only_view = '<button class="view_btn" id=' + data + ' onclick=editUser(' + data + ') style="width:70px;"><i class="material-icons prefix">visibility</i></button>'

        return all_perms

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
  var table = $("#customer-datatable").dataTable().api();

  // table.columns.adjust().draw();
  // Grab the datatables input box and alter how it is bound to events
  $(".dataTables_filter input")
    .unbind() // Unbind previous default bindings
    .bind("input", function (e) { // Bind our desired behavior
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

// console.log(parent_count.length)
$.fn.dataTable.ext.errMode = function (settings, helpPage, message) {
  console.log(message);
  M.toast({ html: message, classes: 'red rounded' })
};



var serial_number = 0;

function childListData(childs) {
  $("#courserows").html("");
  $.each(childs, function (idx, child) {
    serial_number = idx + 1;
    $("#courserows").append(
      "<tr><td>" +
        serial_number +
        "</td><td>" +
        child.first_name +
        "</td><td>" +
        child.last_name +
        "</td><td>" +
        child.birthdate +
        "</td><td>" +
        child.medical_issue +
        "</td><td>" +
        "<button  class='button1 update' onclick='editChild(" + child.id + ")'><i class='fa fa-edit'>Edit</i></button>" + "<button href='#deleteChildModel' onclick='setChild(" + child.id + ")' class='delete' data-id=" + child.id + " data-toggle='modal' style='width:70px;'><i class='fa fa-trash' aria-hidden='true'></i> Delete</button>" + 
        "</td></tr>"
    );
  });

  // $("table_id").show();
  $(document).ready(function () {
    $("#table_id").DataTable({
      columns: [
        {
          data: "id",
        },
        {
          data: "first_name",
        },
        {
          data: "last_name",
        },
        {
          data: "birthdate",
        },
        {
          data: "medical_issue",
        },
        {
          data: "action"
        },

      ],
    });
  });
}


var UserDetails = JSON.parse(sessionStorage.getItem("UserDetails")).access;

$.ajax({
  url: "/get_all_students/",
  type: "GET",
  data: {},
  headers: { Authorization: "Bearer " + UserDetails },
  error: function (err) {
    console.log("Error!", err);
  },
  success: function (data) {
    console.log("Success!");
    childListData(data.data);
  },
});


function editChild(id){
  whichScope = "whichScope"
  sessionStorage.setItem(whichScope, "child");

  window.location.href = "/customers_edit/"+id
}

function deleteChild(id){
  alert(id)
}


function parentTable(){
  $("#parent_table").show();
  $("#child_edit").hide();
}


function childTable(){

  $("#parent_table").hide();
  $("#child_edit").show();
 
}