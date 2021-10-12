// var start_date
// $(document).ready(function (){

//     course = localStorage.getItem('course')

//     $.ajax({
//         type: 'get',
//         url: '/edit_booking/'+course,
//         data: {

//         },
//         success: function(data) {

//             $('#course_type').html(data.data.course_type);
//             $('#start_date_with_day').html(data.data.start_date_with_day);
//             $('#no_of_weeks').html(data.data.no_of_weeks);
//             $('#default_course_rate').html(data.data.default_course_rate);
//             $('#logo').attr('src',data.data.logo);
//             $("#location").html(data.data.location);
//             $("#day_filter").html(data.data.day_filter);
//             $("#start_time").html(data.data.course_group);
//             $("#end_time").html(data.data.course_group);
//             $('#abcd').each(function(item){
//                 item.append(data.data.course_group.age)
//             });

//         },
//         error: function(data) {
// //            console.log(data);
//                 $('#error-msg').text(data.responseJSON.status);
//             },
//         });
//     })

$(document).ready(function (){

  course = localStorage.getItem('course')
  $.ajax({
      type: 'get',
      url: '/edit_booking/'+course,
      // headers: { Authorization: 'Bearer ' + access.access },
      data: {},
      success: function(data) {
          $('#edit-booking').empty();
          console.log(data.data,"booking data");

          html = `BOOKINGS - ${data.data.course_type} - ${data.data.location}`
          $(`#booking_header`).append(html);
      } // success function ends here.

  });//ajax ends here

  }); //document.ready ends here


ase = localStorage.getItem("email");
var counter = 0;
$(document).ready(function () {
  course = localStorage.getItem("course");
  var customer_id = localStorage.getItem("customer_id")
  $.ajax({
    type: "get",
    url: "/edit_booking/" + course,
    // headers: { Authorization: 'Bearer ' + access.access },
    data: {},
    success: function (data) {
      $("#edit-booking").empty();
      console.log(data.data, "booking data");
      var age_groups = []
      jQuery.each(data.data.course_group, function (i, item) {
        console.log(item);
        age_groups.push(item.age.id)


        counter = counter + 1;
        html = `<div class="col-md-3" >
                            <div style="color:black;">Child ${counter}</div>
                            <div class="card-header child-header" >
                                <table style="width:100%">
                                    <tr style="display: flex; flex-direction: column;">
                                        <td>Start time - ${item.start_time} to ${item.end_time}</td>
                                        <td>Group ${counter}</td>
                                        <td>Age: ${item.age.age}</td>
                                    </tr>

                                </table>
                            </div>
                            <div class="card-body child-body">
                                <div style="margin-bottom:2px;">
                                <label>First name:</label>
                                <input type="text" id="first_name_${i}" style="width:60%; border:none;">
                                </div>
                                <div style="margin-bottom:2px;">
                                <label>Last name:</label>
                                <input type="text" id="last_name_${i}" style="width:61%; border:none;">
                                </div>
                                <div style="margin-bottom:2px;">
                                <label>DOB:</label>
                                <input type="date" id="dob_${i}" style="width:79%; border:none;">
                                </div>
                                <div style="margin-bottom:2px;">
                                <label>Allergies/Medial condition:</label>
                                <input type="text" id="medical_issue_${i}" style="width: 98%; border:none;">
                                </div>
                            </div>
                        </div>
                `;
        $("#child_infos").append(html);
      });
      localStorage.setItem('age_groups', age_groups)
      var age_group_detail = localStorage.getItem("age_groups")

    } // success function ends here

  }); //ajax ends here
}); //document.ready ends here


function go_back() {

  window.location.href = "/registration_part1/";
}
// 


function addChild() {
  var age_group_detail = localStorage.getItem("age_groups")
  var array = age_group_detail.split(',');
  var token = sessionStorage.getItem("UserDetails");
  console.log("hello");

  var access_token = JSON.parse(token)
  course = localStorage.getItem("course");
  console.log(access_token.access)

  var i;
  for (i = 0; i < array.length; i++) {
    var first_name = $("#first_name_" + i).val();
    var last_name = $("#last_name_" + i).val();
    var birthdate = $("#dob_" + i).val();
    var medical_issue = $("#medical_issue_" + i).val();
    var content = {

      "customer_id": localStorage.getItem("temporary_customer_form_id"),
      "age_group": array[i],
      "first_name": first_name,
      "last_name": last_name,
      "birthdate": birthdate,
      "medical_issue": medical_issue,
    }
    $.ajax({
      url: "/child_registration/",
      method: "POST",

      headers: { Authorization: 'Bearer ' + access_token.access },

      contentType: "application/json",
      processData: false,
      async: false,


      data: JSON.stringify(content),
      // type": "post",

      "success": add_success,
      "error": add_error

    });
  }

  // var age_group = 
  // ajax()
  function add_success() {
    window.location.href = "/registration_part2/"
  }

  function add_error() {
    alert("Could not add customer details!");
    return false
  }

}