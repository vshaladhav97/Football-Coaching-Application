// NEW JS FILE
var childrens = [];

var counter = 0;
var ageDropdownArray = [];
var course_age_limit_array = [];
$("#add-child-button").hide();
// $("#add-child-button").show()
var user_id = localStorage.getItem("user_id");
if (user_id != null) {
  if (localStorage.getItem("role") == "Customer") {
    $("#add-child-button").show();
  }
}
$(function () {
  $("#checkbox-error-msg").hide();
  $("#main-div").hide();
  $("#main-div-others").hide();
  counter = 0;
  ageDropdownArray = [];
  var location_id = localStorage.getItem("location_id");
  var course = localStorage.getItem("course_type_id");
 
  var course_type_name = localStorage.getItem("course_type_name");

  if (
    course_type_name == "Nursery"
  ) {
    $("#main-div").show();

    $.ajax({
      type: "get",
      url: "/booking_by_course_type_data/" + location_id + "/" + localStorage.getItem("course_detail_id"),
      // headers: { Authorization: 'Bearer ' + access.access },
      data: [
        { id: 1, count: 2 },
        { id: 2, count: 3 },
      ],
      success: function (data) {
        // childrens = data.data[0].course_group;
        // console.log(data.data[0].location);
        $("#edit-booking").empty();
        localStorage.setItem("course_detail_id", data.data[0].id);
        html = `BOOKINGS - ${data.data.location}`;
        // $(`#booking_header`).append(html);

        html = `<img src="${data.data[0].logo}" style="height: 230px; width: 100%;" ></img>`;
        $("#first-div-first-child").append(html);

        localStorage.setItem("no_of_weeks", data.data[0].no_of_weeks);
        html = `<div class="${course_type_name}">
                <b style="text-align:center;">${data.data[0].course_name}</b>
            <div>`;
        $("#first-div-second-child").append(html);

        html = `${data.data[0].course_name}`;
        $("#title_for_course_edit_by_venue").append(html);

        html = `<span class="group-contents">
                <span class="group-style-1">
                    <span style="display: flex; margin-bottom: 10px;">
                        <label><strong>Start Date:</strong> <span>${data.data[0].start_date_with_day}</span></label>
                        <label "></label>
                    </span>
                    
                <span style="display: flex; margin-bottom: 10px;">
                    <label><strong>Duration:</strong> <span>${data.data[0].no_of_weeks} Weeks</span></label>
                    
                </span>
                
                <span style="display: flex; margin-bottom: 10px;">
                    <label><strong>Monthly Cost:</strong> <span>£ ${data.data[0].default_course_rate}</span></label>
    
                </span>
                </span>
                </span>`;
        $("#second-div-first-child").append(html);

        jQuery.each(data.data[0].course_group, function (i, item) {
          counter = counter + 1;

          html = `<div class="${course_type_name}">
                <span class="course-group">
                <span class="ages">
                <table style="width:100%">
                <tr class="group-style">
                <td style="width: 238px; text-align:center;"><span style="font-weight: bold;">Group ${counter}</span> - ${item.age.age}</td>
    
                </tr>
                <hr>
                </table>
                </span>
                </span>
                </div>
                `;
          localStorage.setItem("counter_for_children", counter);
          $("#second-div-second-child").append(html);
        });

        html = `<span class="time-contents">
                <span class="time-content-1">
                <span><label><strong>Preston -</strong> <span>${data.data[0].location}</span></label>
                </span>
    
                <span>
                <label style="margin-top:20px;">Every <span style="color:red;">${data.data[0].day_filter}</span style="color:red;"></label>
                
              </span>            
                
                
                </span>
                </span>`;

        $("#third-div-first-child").append(html);

        jQuery.each(data.data[0].course_group, function (i, item) {
          // dropdownDetails.push([{id:i}])
          // alert(i)
          // var e = document.getElementById("dropdowns");
          // var value = e.options[e.selectedIndex].value;
          // alert(value)
          // counter = counter + 1;
          course_age_limit_array.push(item.age.id);

          ageDropdownArray.push(item.age.id);
          html = `<div>
                    <span class="times" >
                    <table style="width: 100%; text-align: center;">
                    <tr class="time-content">
                    
                    <td >${item.start_time} to ${item.end_time} <select name="" id=${item.age.id}  onchange="GetDropDownVal(this, ${item.age.id})"  class="dropdwn1 dropdown2">
                    <option value=""> - </option>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                    <option value="5">5</option>
                    <option value="6">6</option>
                    <option value="7">7</option>
                    <option value="8">8</option>
                    <option value="9">9</option>
                    <option value="10">10</option>
                  </select></td>
                    </tr>
                    <hr>
                    </table>
                    </span>
                    </div>   
                        `;

          // $("#dropdowns :selected").val();
          $("#third-div-second-child").append(html);
        });

        sessionStorage.setItem(
          "age_id_by_course",
          JSON.stringify(course_age_limit_array)
        );

        html =
          `
                Total Selected 
                ` + '<span id="counter_total"><span>';

        $("#third-div-third-child").append(html);
      }, // success function ends here.
    }); //ajax ends here
  } else if (course_type_name == "Evening Development") {
    $("#main-div").show();

    $.ajax({
      type: "get",
      url: "/booking_by_course_type_data/" + location_id + "/" + localStorage.getItem("course_detail_id"),
      // headers: { Authorization: 'Bearer ' + access.access },
      data: [
        { id: 1, count: 2 },
        { id: 2, count: 3 },
      ],
      success: function (data) {
        // childrens = data.data[0].course_group;
        // console.log(data.data[0].location);
        $("#edit-booking").empty();
       

        html = `BOOKINGS - ${data.data.location}`;
        // $(`#booking_header`).append(html);

        html = `<img src="${data.data[0].logo}" style="height: 230px; width: 100%;" ></img>`;
        $("#first-div-first-child").append(html);
        localStorage.setItem("course_detail_id", data.data[0].id);
        localStorage.setItem("no_of_weeks", data.data[0].no_of_weeks);
        html = `<div class="${course_type_name}">
                <b style="text-align:center;">${data.data[0].course_name}</b>
            <div>`;
        $("#first-div-second-child").append(html);

        html = `${data.data[0].course_name}`;
        $("#title_for_course_edit_by_venue").append(html);

        html = `<span class="group-contents">
                <span class="group-style-1">
                    <span style="display: flex; margin-bottom: 10px;">
                        <label><strong>Start Date:</strong> <span>${data.data[0].start_date_with_day}</span></label>
                        <label "></label>
                    </span>
                    
                <span style="display: flex; margin-bottom: 10px;">
                    <label><strong>Duration:</strong> <span>${data.data[0].no_of_weeks} Weeks</span></label>
                    
                </span>
                
                <span style="display: flex; margin-bottom: 10px;">
                    <label><strong>Weekly Cost:</strong> <span>£ ${data.data[0].default_course_rate}</span></label>
    
                </span>
                </span>
                </span>`;
        $("#second-div-first-child").append(html);

        jQuery.each(data.data[0].course_group, function (i, item) {
          counter = counter + 1;

          html = `<div class="${course_type_name}">
                <span class="course-group">
                <span class="ages">
                <table style="width:100%">
                <tr class="group-style">
                <td style="width: 238px; text-align:center;"><span style="font-weight: bold;">Group ${counter}</span> - ${item.age.age}</td>
    
                </tr>
                <hr>
                </table>
                </span>
                </span>
                </div>
                `;
          localStorage.setItem("counter_for_children", counter);
          $("#second-div-second-child").append(html);
        });

        html = `<span class="time-contents">
                <span class="time-content-1">
                <span><label><strong>Preston -</strong> <span>${data.data[0].location}</span></label>
                </span>
    
                <span>
                <label style="margin-top:20px;">Every <span style="color:red;">${data.data[0].day_filter}</span style="color:red;"></label>
                
              </span>            
                
                
                </span>
                </span>`;

        $("#third-div-first-child").append(html);

        jQuery.each(data.data[0].course_group, function (i, item) {
          // dropdownDetails.push([{id:i}])
          // alert(i)
          // var e = document.getElementById("dropdowns");
          // var value = e.options[e.selectedIndex].value;
          // alert(value)
          // counter = counter + 1;
          course_age_limit_array.push(item.age.id);

          ageDropdownArray.push(item.age.id);
          html = `<div>
                    <span class="times" >
                    <table style="width: 100%; text-align: center;">
                    <tr class="time-content">
                    
                    <td >${item.start_time} to ${item.end_time} <select name="" id=${item.age.id}  onchange="GetDropDownVal(this, ${item.age.id})"  class="dropdwn1 dropdown2">
                    <option value=""> - </option>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                    <option value="5">5</option>
                    <option value="6">6</option>
                    <option value="7">7</option>
                    <option value="8">8</option>
                    <option value="9">9</option>
                    <option value="10">10</option>
                  </select></td>
                    </tr>
                    <hr>
                    </table>
                    </span>
                    </div>   
                        `;

          // $("#dropdowns :selected").val();
          $("#third-div-second-child").append(html);
        });

        sessionStorage.setItem(
          "age_id_by_course",
          JSON.stringify(course_age_limit_array)
        );

        html =
          `
                Total Selected 
                ` + '<span id="counter_total"><span>';

        $("#third-div-third-child").append(html);
      }, // success function ends here.
    }); //ajax ends here
  } else {
    $("#main-div-others").show();
    $("#main-div").hide();
    $("#preschol_button").hide();
    $("#next-btn").hide();

    $.ajax({
      type: "get",
      url:
        "/booking_by_course_type_data_for_others/" + localStorage.getItem("location_id") + "/" + localStorage.getItem("course_detail_id"),
      // headers: { Authorization: 'Bearer ' + access.access },
      data: [
        { id: 1, count: 2 },
        { id: 2, count: 3 },
      ],
      success: function (data) {
        htmlTemp = `
                <div class="${course}">
                    <div class="course_edit_by_heading">Bury - Fairfield Community Centre</div>
                        <div class="row no-gutters" style="margin-top: 0px;">
                            <div id="first-div-for-others" class="col-sm-4">
                                <div id="first-div-first-child-for-others" class="col-sm-12">
                                <img src="${data.data[0].logo}" alt="banner" /></div>
                                <div id="first-div-second-child-for-others" class="col-sm-12">
                                    <b>${data.data[0].course_name}</b><br>
                                </div>
                            </div>
                            <div id="second-div-for-others" class="col-sm-4">

                                <div id="second-div-1st-child-for-others" class="inside_ch">
                                    <p><strong>When: </strong>${data.data[0].start_date_with_day} to ${data.data[0].end_date_for_booking}</p>
                                </div>
                                <div id="second-div-2nd-child-for-others" class="inside_ch">
                                    <p><strong>Group 1 , Age: </strong>${data.data[0].course_group[0].age.age}</p>
                                </div>
                                <div id="second-div-3rd-child-for-others" class="inside_ch">
                                    <p><strong>Maximum capacity: </strong>${data.data[0].course_details[0].maximum_capacity}</p>
                                </div>
                                <div id="second-div-4th-child-for-others" class="inside_ch">
                                    <p><strong>Drop off between: </strong>${data.data[0].course_details[0].from_drop_off_time} to ${data.data[0].course_details[0].to_drop_off_time}</p>
                                </div>
                                <div id="second-div-5th-child-for-others" class="inside_ch">
                                    <p><strong>Pick up between: </strong>${data.data[0].course_details[0].from_pick_up_time} to ${data.data[0].course_details[0].to_pick_up_time}</p>
                                </div>
                                <div id="second-div-6th-child-for-others" class="inside_ch">
                                    <p><strong>Type of holiday club: </strong>${data.data[0].surface}</p>
                                </div>

                            </div>
                            <div id="third-div-for-others-others" class="col-sm-4">
                                <div id="third-div-second-child-others" class="col-sm-12"><label for="cars">Select number
                                        of children</label>
                                    <select name="cars" id="no_of_child" onclick="MyFunctForChild()">
                                        <option value="1">1</option>
                                        <option value="2">2</option>
                                        <option value="3">3</option>
                                        <option value="4">4</option>
                                        <option value="5">5</option>
                                        <option value="6">6</option>
                                        <option value="7">7</option>
                                        <option value="8">8</option>
                                    </select>
                                </div>
                                <div id="time-scroll-others" class="col-sm-12">
                                    <div id="third-div-third-child-others">
                                        <div id="third-div-third-child-others">
                                            <div class="" style="margin-top: 75px">
                                                <div class="col-3">
                                                    <button id="Button" type="submit" onclick="CheckForLogin()">
                                                        Continue
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                            </div>
                        </div>
                        </div>
                    </div>
                `;
        $(".all_3evening_development").append(htmlTemp);
      },
    });
  }
}); //document.ready ends here

// to filter student who has already done payments.
var payment_done_student_id = [];
$(document).ready(function () {
  $.ajax({
    type: "get",
    url: "/student_with_payment_done/" + localStorage.getItem("customer_id"),
    data: {},
    success: function (data) {
      console.log(data);
      data.forEach((element) => {
        console.log(element.nursery_and_weekly_student_order_details.student);
        payment_done_student_id.push(
          element.nursery_and_weekly_student_order_details.student
        );
        localStorage.setItem(
          "payment_student",
          JSON.stringify(payment_done_student_id)
        );
      });
    },
  });
});

// To Check children belongs to which age group.
course_type_id = localStorage.getItem("course_type_id");
$(document).ready(function () {
  var counter = 0;
  var course_type_name = localStorage.getItem("course_type_name");

  $.ajax({
    type: "get",
    url:
      "/student_with_course_type/" +
      localStorage.getItem("customer_id") +
      "/" +
      course_type_id,
    data: {},
    success: function (data) {
      if (payment_done_student_id.length != 0) {
        data = data.filter((val) => !payment_done_student_id.includes(val.id));
      }
      // payment_done_student_id.forEach(ele => {

      for (i = 0; i < data.length; i++) {
        // if(ele != data[i].id) {

        childrens.push(data[i].coursedetail[0].age);
        // }
      }
      // })
    },
  });
});

var myMap = new Map();
var counter_total = 0;
var duplicate_numberofchild_flag = false;
var selected_no_child = new Map();
function GetDropDownVal(selectObject, q) {
  var total_count = 0;
  ageDropdownArray.forEach((element) => {
    var selectedVal = $(`#${element} option:selected`).text();
    if (parseInt(selectedVal)) {
      total_count = total_count + parseInt(selectedVal);
    }
  });

  var value = parseInt(selectObject.value);
  if(value) {
    myMap.set(q, value);
  }
  counter_total = counter_total + value;

  var tempArr = [];

  // To check How many time selected value Appear.
  function getOccurrence(array, value) {
    return array.filter((v) => v === value).length;
  }

  number_of_children_selected = getOccurrence(childrens, q);
  var customer = localStorage.getItem("customer_id");

  if (value > number_of_children_selected && customer != undefined) {
    duplicate_numberofchild_flag = true;
    tempArr.push(q, true);

    alert(
      "You Have Only " +
        number_of_children_selected +
        " Childrens For This Group and You Selected " +
        value +
        " Childrens. Please Select " +
        number_of_children_selected +
        " Children to Continue"
    );
  } else {
    duplicate_numberofchild_flag = false;
    tempArr.push(q, false);
  }
  selected_no_child.set(q, duplicate_numberofchild_flag);
  // localStorage.setItem('no_of_age_child_flag',JSON.stringify(selected_no_child))
  tempArr = [];
  // selected_no_child =[]
  document.getElementById("counter_total").innerHTML = total_count;

  var matched = false;
  var statusFlag = false;
  //  for non register user
  if (childrens.length == 0) {
    localStorage.myMap = JSON.stringify(Array.from(myMap.entries()));
    localStorage.selected_no_child = JSON.stringify(
      Array.from(selected_no_child.entries())
    );
  } else {
    for (var i = 0; i < childrens.length; i++) {
      // console.log(childrens[i].age.id)
      if (childrens[i] == q) {
        matched = true;
        console.log(i);
        localStorage.myMap = JSON.stringify(Array.from(myMap.entries()));
        localStorage.selected_no_child = JSON.stringify(
          Array.from(selected_no_child.entries())
        );
        break;
      } else {
        localStorage.myMap = JSON.stringify(Array.from(myMap.entries()));
        localStorage.selected_no_child = JSON.stringify(
          Array.from(selected_no_child.entries())
        );
        statusFlag = true;
      }
    }
  }
  if (statusFlag == true && matched == false) {
    alert(
      "Your Children Age is not matched with this Age Group. Add child First For this Age group"
    );
    // document.getElementById("Button").disabled = true;
    // document.addEventListener("DOMContentLoaded", function(event) {
    //   document.getElementById("Button").disabled = true;
    // });
    matched = false;
  }
}

function MyFunctForChild() {
  var selectBox = document.getElementById("no_of_child");
  // alert(selectBox);
  for (i = 0; i < selectBox.length; i++) {
    var selectedValue = selectBox.options[selectBox.selectedIndex].value;
    // var selectedValue1 = selectBox.options[selectBox.selectedIndex].value;
  }

  // var selectedValue2 = selectBox[2].options[selectBox.selectedIndex].value;
  localStorage.setItem("no_of_childs", selectedValue);
  // alert(selectedValue1);
}

var customer_id = parseInt(localStorage.getItem("customer_id"));
var student_count = [];
$.ajax({
  type: "get",
  url: "/student_details_by_customer/" + customer_id,
  // headers: { Authorization: 'Bearer ' + access.access },
  data: {},
  success: function (data) {
    jQuery.each(data.data, function (i, item) {
      student_count.push(item.id);
    });
  },
  error: function (data) {
    $("#error-msg").text("error");
  },
});

function addChildren() {
  if (localStorage.getItem("myMap") != null) {
    window.location.href = "/child_registration_for_booking/";
  } else {
    alert("Please select child!");
  }
}

function CheckForLogin() {
  var role = localStorage.getItem("role");
  var user_id = localStorage.getItem("user_id");

  // to check whether user selected all valid child.
  if (
    localStorage.getItem("no_of_childs") ||
    localStorage.getItem("selected_no_child")
  ) {
    var valid_age_child = JSON.parse(localStorage.getItem("no_of_childs"));
    var check_for_all_valid_child = JSON.parse(
      localStorage.getItem("selected_no_child")
    );

    if (valid_age_child != null) {
      console.log(valid_age_child.length);
      for (z = 0; z < valid_age_child.length; z++) {
        console.log(valid_age_child[z][1]);
        if (valid_age_child[z][1]) {
          duplicate_numberofchild_flag = true;
        }
      }
    }
    if (check_for_all_valid_child != null) {
      for (s = 0; s < check_for_all_valid_child.length; s++) {
        // console.log(check_for_all_valid_child[s][1] == true)
        var boolval = check_for_all_valid_child[s][1];
        if (boolval == true) {
          duplicate_numberofchild_flag = true;
        }
      }
    }
  }

 var mymap = JSON.parse(localStorage.getItem("myMap"))
 if(mymap){

   for(m = 0; m < mymap.length; m++) {
    console.log(mymap[m][1])
    if(mymap[m][1] == null) {
      alert("please select atleast one child");
      return false;
    }
   }
 
 }
  if (localStorage.getItem("myMap") != null) {
    if (user_id != null) {
      if (role == "Customer") {
        if (student_count.length > 0) {
          if (localStorage.getItem("course_type_name") == "Nursery") {
            if (duplicate_numberofchild_flag == false) {
              window.location.href = "/order_summary/";
            } else {
              alert(
                "Please Select Correct Number Of Children First To Continue."
              );
            }
          } else if (
            localStorage.getItem("course_type_name") == "Evening Development"
          ) {
            if (duplicate_numberofchild_flag == false) {
              if (childrens.length == 0) {
                alert("Payment for all children are completed!");
              } else {
                window.location.href = "/child_selection_for_payement/";
              }
            } else {
              alert(
                "Please Select Correct Number Of Children First To Continue."
              );
            }
          } else {
            window.location.href = "/week_booking/";
          }
        } else {
          alert(
            "customer has no children. If you want to register a child then click on add child button"
          );
        }
      } else {
        alert(role + " has no children. Please use customer login!");
      }
    } else {
      window.location.href = "/check_for_member/";
    }
  } else if (localStorage.getItem("course_type_name") == "Holiday Camp") {
    if (user_id != null) {
      if (role == "Customer") {
        if (localStorage.getItem("no_of_childs")) {
          window.location.href = "/week_booking/";
        } else {
          alert("please select in the dropdown");
        }
      }
    } else {
      if (localStorage.getItem("no_of_childs")) {
        window.location.href = "/check_for_member/";
      } else {
        alert("please select atleast one child");
      }
    }
  } else {
    alert("please select atleast one child");
  }
}

var isSyncingLeftScroll = false;
var isSyncingRightScroll = false;
var leftDiv = document.getElementById("second-div-second-child");
var rightDiv = document.getElementById("third-div-second-child");

leftDiv.onscroll = function () {
  if (!isSyncingLeftScroll) {
    isSyncingRightScroll = true;
    rightDiv.scrollTop = this.scrollTop;
  }
  isSyncingLeftScroll = false;
};

rightDiv.onscroll = function () {
  if (!isSyncingRightScroll) {
    isSyncingLeftScroll = true;
    leftDiv.scrollTop = this.scrollTop;
  }
  isSyncingRightScroll = false;
};

// if (role == "Customer") {
//   if (student_count.length > 0) {
//     if (localStorage.getItem("myMap") != null) {
//
//
//         if (user_id != null) {
//           if (localStorage.getItem("course_type_name") == "Nursery") {
//             window.location.href = "/order_summary/";
//           } else if (
//             localStorage.getItem("course_type_name") == "Evening Development"
//           ) {
//             window.location.href = "/child_selection_for_payement/";
//           } else {
//             window.location.href = "/week_booking/";
//           }
//         } else {
//           window.location.href = "/check_for_member/";
//         }
//       } else {
//         alert("select atleast one child ");
//       }
//     }
//     else {
//       alert("You have 0 children registered");
//     }

//   }

//   else {
//     alert(role + " has no children");
//   }
// }




