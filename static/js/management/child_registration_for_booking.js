$("#child_infos").hide();
$("#child_infos_others").hide();
var group_type;

// to get years from age group
var regex = /\d+/g;
// var string = "6- 8 years old(year 2)";

// var fields = string.split('(');
var fields;
var fields_year;
var year;

var lowest_year;
var highest_year;
var min_date;
var max_date;

// calculate year belongs to that group or not
var enteredDate = "2020-06-1";

var child_group = [
  { age_id: 5, group: "Group 1" },
  { age_id: 6, group: "Group 2" },
  { age_id: 7, group: "Group 3" },
  { age_id: 8, group: "Group 4" },
  { age_id: 3, group: "Group 1" },
  { age_id: 4, group: "Group 2" },
  { age_id: 2, group: "Group 3" },
];

var dropdown_values = localStorage.getItem("myMap");
if (dropdown_values != null) {
  var map = new Map(JSON.parse(localStorage.myMap));
  var dropdown_array = [];
  for (let [key, value] of map.entries()) {
    var key_value = [];
    key_value.push(key);
    key_value.push(value);
    dropdown_array.push(key_value);
    dropdown_array.sort(sortFunction);
  }
}

function sortFunction(a, b) {
  if (a[0] === b[0]) {
    return 0;
  } else {
    return a[0] < b[0] ? -1 : 1;
  }
}

var ase = localStorage.getItem("email");
var counter = 0;
var childIndex = 0;
$(document).ready(function () {
  var location_id = localStorage.getItem("location_id");
  var course = localStorage.getItem("course_type_id");
  var user_id = localStorage.getItem("user_id");
  var course_type_name = localStorage.getItem("course_type_name");
  if (
    course_type_name == "Nursery" ||
    course_type_name == "Evening Development"
  ) {
    {
      $("#child_infos").show();
      $.ajax({
        type: "get",
        url: "/booking_by_course_type_data/" + location_id + "/" + localStorage.getItem('course_detail_id'),
        data: {},
        success: function (data) {
          $("#edit-booking").empty();
          console.log(data.data, "booking data");
          var age_groups = [];
          jQuery.each(data.data[0].course_group, function (i, item) {
            console.log("item data", item);

            var age_id = item.age.id;
            for (i = 0; i < dropdown_array.length; i++) {
              if (dropdown_array[i][0] == age_id) {
                var iterate_value = dropdown_array[i][1];
                console.log(iterate_value);

                for (j = 0; j < iterate_value; j++) {
                  age_groups.push(item.age.id);
                  for (l = 0; l < child_group.length; l++) {
                    console.log("child group", child_group[l]);
                    if (item.age.id == child_group[l].age_id) {
                      group_type = child_group[l].group;
                      fields = item.age.age.split("(");
                      fields_year = ": (" + fields[1];
                      if (fields[1] == undefined) {
                        fields_year = "";
                      }
                      year = fields[0].match(regex);
                      lowest_year = year[0];
                      if ((lowest_year = "18")) {
                        lowest_year = 1;
                      }
                      highest_year = year[1];
                      var d = new Date();
                      d.toLocaleDateString();
                      d.setFullYear(d.getFullYear() - lowest_year);
                      var split_max_date = d.toLocaleDateString();
                      max_date = split_max_date.split("/").reverse().join("-");

                      d = new Date();
                      d.toLocaleDateString();
                      d.setFullYear(d.getFullYear() - highest_year);
                      var split_min_date = d.toLocaleDateString();

                      min_date = split_min_date.split("/").reverse().join("-");
                      // alert(typeof(min_date))
                    }
                  }

                  counter = counter + 1;
                  html = `<div class="col-md-4 child_registration_for_bookings child${course}">
                                      <div class="card-header child-header" >
                                          <table style="width:100%">
                                              <tr style="display: flex; flex-direction: column;">
                                                  <td><strong>Start time -</strong> <span>${item.start_time} to ${item.end_time}</span></td>
                                                  <td><strong>${group_type}  ${fields_year}</strong></td>
                                                  <td><strong>Age:</strong> <span>${item.age.age}</span></td>
                                              </tr>
                                          </table>
                                      </div>
                                      <div class="card-body child-body">
                                          <div class="child_count">Child ${counter}</div>
                                          <div class="form_lable">
                                          <label>First name: <span style="color:red">*</span></label>
                                          <input type="text" name="fName" id="first_name_${childIndex}" style="width:60%; border:none;" required />
                                          </div>
                                          <div class="form_lable">
                                          <label>Last name: <span style="color:red">*</span></label>
                                          <input type="text" name="lName" id="last_name_${childIndex}" style="width:61%; border:none;" required />
                                          </div>
                                          <div class="form_lable">
                                          <label>DOB: <span style="color:red">*</span></label>
                                          <input name="DOB" type="date" id="dob_${childIndex}" min="${min_date}" max="${max_date}" style="width:79%; border:none;" required />
                                          </div>
                                          <div class="form_lable d-block">
                                          <label>Allergies/Medial condition: <span style="color:red">*</span></label>
                                          <input type="text" name="mName" id="medical_issue_${childIndex}" style="width: 98%; border:none;" required />
                                          </div>
                                      </div>
                                  </div>
                          `;
                  childIndex = childIndex + 1;
                  $("#child_infos").append(html);
                }
              }
            }

            // counter = counter + 1;
            // html = `<div class="col-md-4 child_registration_for_bookings child${course}">
            //                       <div class="card-header child-header" >
            //                           <table style="width:100%">
            //                               <tr style="display: flex; flex-direction: column;">
            //                                   <td><strong>Start time -</strong> <span>${item.start_time} to ${item.end_time}</span></td>
            //                                   <td><strong>Group ${counter}</strong></td>
            //                                   <td><strong>Age:</strong> <span>${item.age.age}</span></td>
            //                               </tr>

            //                           </table>
            //                       </div>
            //                       <div class="card-body child-body">
            //                           <div class="child_count">Child ${counter}</div>
            //                           <div class="form_lable">
            //                           <label>First name:</label>
            //                           <input type="text" id="first_name_${i}" style="width:60%; border:none;">
            //                           </div>
            //                           <div class="form_lable">
            //                           <label>Last name:</label>
            //                           <input type="text" id="last_name_${i}" style="width:61%; border:none;">
            //                           </div>
            //                           <div class="form_lable">
            //                           <label>DOB:</label>
            //                           <input type="date" id="dob_${i}" style="width:79%; border:none;">
            //                           </div>
            //                           <div class="form_lable d-block">
            //                           <label>Allergies/Medial condition:</label>
            //                           <input type="text" id="medical_issue_${i}" style="width: 98%; border:none;">
            //                           </div>
            //                       </div>
            //                   </div>
            //           `;
            // $("#child_infos").append(html);
          });
          localStorage.setItem("age_groups", age_groups);
          var age_group_detail = localStorage.getItem("age_groups");
        }, // success function ends here
      }); //ajax ends here
    }
  } else {
    $("#child_infos_others").show();
    counter = counter + 1;
    var no_of_child_selected = localStorage.getItem("no_of_childs");
    $.ajax({
      type: "get",
      url: "/booking_by_course_type_data/" + location_id + "/" + localStorage.getItem('course_detail_id'),

      data: {},
      success: function (data) {
        $("#edit-booking").empty();
        console.log(data.data, "booking data");
        var age_groups = [];

        for (var n = 0; n < no_of_child_selected; n++) {
          html = `
            <div class="col-md-4 child_registration_for_bookings child${course}">
           
            <div class="card-header child-header" >
                <table style="width:100%">
                    <tr style="display: flex; flex-direction: column;">
                        <td><strong>Start time -</strong> <span>${data.data[0].course_group[0].start_time} to ${data.data[0].course_group[0].end_time}</span></td>
                        
                        <td><strong>Group ${counter}</strong></td>
                        <td><strong>Age:</strong> <span>${data.data[0].course_group[0].age.age}</span></td>
                        <td><strong>Venue:</strong> <span>${data.data[0].location}</span></td>
                        
                    </tr>
                </table>
            </div>
            <div class="card-body child-body">
            <div class="child_count">Child ${counter}</div>
              <div class="form_lable">
                <label>First name :</label>
                <input name="fName" type="text" id="first_name_${n}" style="width:60%; border:none; required">
              </div>
              <div class="form_lable">
                <label>Last name:</label>
                <input name="lName" type="text" id="last_name_${n}" style="width:61%; border:none;required">
              </div>
              <div class="form_lable">
                <label>DOB:</label>
                <input name= "DOB" type="date" id="dob_${n}" style="width:79%; border:none; required">
                
              </div>
              <div class="form_lable d-block">
                <label>Allergies/Medial condition:</label>
                <input name="mName" type="text" id="medical_issue_${n}" style="width: 98%; border:none;required">
            </div>
           
          </div>
            `;
          $("#child_infos_others").append(html);
        }
        localStorage.setItem("age_groups", age_groups);
        var age_group_detail = localStorage.getItem("age_groups");
      }, // success function ends here
    }); //ajax ends here
  }
}); //document.ready ends here

function go_back() {
  localStorage.removeItem("myMap");
  window.location.href = "/course_edit_by_venue/";
}
//

$(document).ready(function () {
  $.ajax({
    type: "get",
    url: "/last_register_customer/",
    data: {},
    success: function (data) {
      $("#customer_id_for_child").html(data.data[0].id);
      localStorage.setItem("customers_new_id", data.data[0].id);
    },
    error: function (data) {
      $("#error-msg").text(data.responseJSON.status);
    },
  });
});

var validation_flag = true;
function addChild() {
  var fName = document.childRegistration.fName.value;
  temparray = Array.from(document.childRegistration.fName);

  var lName = document.childRegistration.lName.value;
  ltemparray = Array.from(document.childRegistration.lName);

  dtemparray = Array.from(document.childRegistration.DOB);
  mtemparray = Array.from(document.childRegistration.mName);

  for (var v = 0; v < temparray.length; v++) {
    if (temparray[v].value == "" || temparray[v].value == null) {
      validation_flag = false;
      return false;
    } else if (ltemparray[v].value == "" || ltemparray[v].value == null) {
      validation_flag = false;
      return false;
    } else if (dtemparray[v].value == "" || dtemparray[v].value == null) {
      validation_flag = false;
      return false;
    } else if (mtemparray[v].value == "" || mtemparray[v].value == null) {
      validation_flag = false;
      return false;
    } else {
      validation_flag = true;
    }
  }
  if (validation_flag) {
    var age_group_detail = localStorage.getItem("age_groups");
    var array = age_group_detail.split(",");
    var token = sessionStorage.getItem("UserDetails");
    console.log("array", array);

    var access_token = JSON.parse(token);
    course = localStorage.getItem("course");
    var customer_id = parseInt(localStorage.getItem("customer_id"));
    if (customer_id == null) {
      customer_id = localStorage.getItem("customers_new_id");
    }
    // var user_id = parseInt(users_id);
    var i;
    for (i = 0; i < array.length; i++) {
      var first_name = $("#first_name_" + i).val();
      var last_name = $("#last_name_" + i).val();
      // Below one is the single line logic to calculate the no. of years...
      var dob = $("#dob_" + i).val();
      // var birthdate = new Date(new Date() - new Date(dob)).getFullYear() - 1970;
      // var birthdate = dob;
      // console.log(birthdate, "birthdate");
      var medical_issue = $("#medical_issue_" + i).val();
      //ajax ends here

      // if(birthdate >= lowest_year &&  birthdate <= highest_year) {
      //   alert("dob not valid", birthdate)
      // }

      var content = {
        customer_id: customer_id,
        age_group: array[i],
        first_name: first_name,
        last_name: last_name,
        birthdate: dob,
        medical_issue: medical_issue,
      };
      $.ajax({
        url: "/child_registration/",
        method: "POST",
        contentType: "application/json",
        processData: false,
        async: false,
        data: JSON.stringify(content),
        // success: add_success,
        // error: add_error,
      })
        .done(function () {
          add_success();
        })
        .fail(function () {
          return false;
        });
    }

    function add_error() {
      alert("Could not add customer details!");
      return false;
    }
  }
}
function add_success() {
  if (localStorage.getItem("course_type_name") == "Nursery") {
    window.location.href = "/order_summary/";
  } else if (
    localStorage.getItem("course_type_name") == "Evening Development"
  ) {
    window.location.href = "/child_selection_for_payement/";
  } else {
    window.location.href = "/week_booking/";
  }
}

function format(inputDate) {
  var date = new Date(inputDate);
  if (!isNaN(date.getTime())) {
    var day = date.getDate().toString();
    var month = (date.getMonth() + 1).toString();
    // Months use 0 index.

    return (
      (month[1] ? month : "0" + month[0]) +
      "-" +
      (day[1] ? day : "0" + day[0]) +
      "-" +
      date.getFullYear()
    );
  }
}

console.log(format("2015/01/25"));
