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
var fields;
var fields_year;
var group_type;
var child_group = [
  { age_id: 5, group: "Group 1" },
  { age_id: 6, group: "Group 2" },
  { age_id: 7, group: "Group 3" },
  { age_id: 8, group: "Group 4" },
];

function sortFunction(a, b) {
  if (a[0] === b[0]) {
    return 0;
  } else {
    return a[0] < b[0] ? -1 : 1;
  }
}

var age_id_by_course = JSON.parse(sessionStorage.getItem("age_id_by_course"));
var payment_success_student = JSON.parse(
  localStorage.getItem("payment_student")
);


course_type_id = localStorage.getItem("course_type_id")
var prev_age;
var tempArray = [];
$(document).ready(function () {
  var counter = 0;
  var course_type_name = localStorage.getItem("course_type_name");

  $.ajax({
    type: "get",
    url:
      "/student_with_course_type/" +
      localStorage.getItem("customer_id") + '/' + course_type_id,
    data: {},
    success: function (data) {

        
    
      
      // var i;
      // To filter payment done students.

      for (i = 0; i < data.length; i++) {

        // this will remove already paid students from data.ty

        if (payment_success_student != null){

          data = data.filter(val => !payment_success_student.includes(val.id));
        }

            if (age_id_by_course.length > 0) {

                for (j = 0; j < age_id_by_course.length; j++) {

                    if (data[i].coursedetail[0].age == age_id_by_course[j]) {
                        for (l = 0; l < child_group.length; l++) {
                            console.log("child group", child_group[l]);
                            if (data[i].coursedetail[0].age == child_group[l].age_id) {
                            group_type = child_group[l].group;
                            fields = data[i].age.split("(");
                            fields_year = "(" + fields[1];
                            }
                }

                counter = counter + 1;
                var start_time = toConvertGlobalTime(
                    data[i].coursedetail[0].start_time
                );
                var end_time = toConvertGlobalTime(
                    data[i].coursedetail[0].end_time
                );

              html = `
                                    
                                        <div class="col-md-4 ${course_type_name}">
                                            <div class="card-header child-header" >
                                                <table style="width:100%">
                                                    <tr style="display: flex; flex-direction: column;">
                                                        
                                                        <td><strong>Start time -</strong> <span>${start_time} to ${end_time}</span></td>
            
                                                        <td><strong>${group_type} : ${fields_year}</strong></td>
                                                        <td><strong>Age:</strong> <span>${data[i].age}</span></td>
                                                        <td><strong>Venue:</strong> <span>${data[i].coursedetail[0].location}</span></td>
                                                        
                                                    </tr>
                                                </table>
                                            </div>
                    
                                            <div class="card-body child-body">
                                            <div class="d-flex justify-content-between body_content">
                                            <div class="child_count">Child ${counter}</div>
                                            <div class="checkbox_"><span>Enroll</span> <input type="checkbox" id="myCheck" onchange="myFunction(this, ${data[i].id})" class="enroll_value"  value="${data[i].id}"></div>
                                            </div>
                                            <div class="form_lable">
                                                <label>First name:</label>
                                                <input type="text" value="${data[i].firstname}" readonly/>
                                            </div>
                                            <div class="form_lable">
                                                <label>Last name:</label>
                                                <input type="text" value="${data[i].lastname}" readonly/>
                                            </div>
                                            <div class="form_lable">
                                                <label>DOB:</label>
                                                <input type="text" value="${data[i].dob}" readonly/>
                                            </div>
                                            <div class="form_lable d-block">
                                                <label>Allergies/Medial condition:</label>
                                                <input type="text" value="${data[i].medical_issue}" readonly/>
                                            </div>
                                            </div>
                                        </div>
                                            `;

              $("#child_infos_others").append(html);

              var index_value = i;

              // this code is added to make child already Enrolled.
              for (k = 0; k < dropdown_array.length; k++) {
                if (
                  dropdown_array[k][0] == data[i].coursedetail[0].age &&
                  dropdown_array[k][1] == 1 &&
                  prev_age != data[i].coursedetail[0].age
                ) {
                  prev_age = data[i].coursedetail[0].age;
                  if(!tempArray.includes(data[i].coursedetail[0].age)){

                    $("input[value='" + data[i].id + "']").prop("checked", true);
                    student_id.push(data[i].id);
                  }
                  tempArray.push(data[i].coursedetail[0].age)
                }
              }
            }
          }
        }

      }

      localStorage.setItem("student_id", JSON.stringify(student_id));
      // We are storing already enrolled children.
    },
  });
});

//to convert 24hour time to 12hour with am pm
function toConvertGlobalTime(time) {
  var timeString = time;
  var H = +timeString.substr(0, 2);
  var h = H % 12 || 12;
  var ampm = H < 12 ? "AM" : "PM";
  timeString = h + timeString.substr(2, 3) + ampm;

  return timeString; // return adjusted time or original string
}

var student_id = [];
function myFunction(value, id) {
  if (value.checked == true) {
    student_id.push(id);
  } else {
    student_id.splice($.inArray(id, student_id), 1);
  }

  localStorage.setItem("student_id", JSON.stringify(student_id));
}

function goForOrderSummary() {
  if (student_id.length > 0) {
    window.location.href = "/order_summary/";
  } else {
    alert("please select atleast one child");
  }
}

function goBackFromPaymentSelection() {
  localStorage.removeItem("myMap");
  sessionStorage.removeItem("age_id_by_course");
  window.location.href = "/course_edit_by_venue/";
}
