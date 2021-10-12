$("#course-type").change(function () {
  var course_type_value = this.value;
  sessionStorage.setItem(course_type_value, "course_type_value");
});

$(document).ready(function () {
  $(
    ".no_of_weeks,.joining_fee,.course_price,.start_date,.end_date,.no_of_groups,.group,.course,.no_of_weeks_holiday,.per_day_price"
  ).css("display", "none");
  $(function () {
    $("#course-type").change(function () {
      $(
        ".no_of_weeks,.joining_fee,.course_price,.start_date,.end_date,.no_of_groups,.group,.course,.no_of_weeks_holiday,.per_day_price, .from_drop_off_time, .to_drop_off_time, .from_pick_up_time, .to_pick_up_time"
      ).css("display", "none");
      var option_no = $("option:selected").val();
      var option = $("option:selected", this).attr("text");
      localStorage.setItem("course_type", option_no);
      if (option == "Evening") {
        $(".no_of_weeks, .no_of_groups").css("display", "block");
        $("#course_description").show();
        $(".start_date,.end_date,.course_price,.no_of_groups").css(
          "display",
          "block"
        );
      } else if (option == "Nursery") {
        $(".no_of_weeks").css("display", "none");
        $(".start_date,.end_date,.joining_fee,.course_price,.no_of_groups").css(
          "display",
          "block"
        );
      } else if (option == "Holiday") {
        $(".no_of_weeks_holiday").css("display", "block");
        $(".start_date,.end_date,.per_day_price").css("display", "block");
        $(".from_drop_off_time, .to_drop_off_time, .from_pick_up_time, .to_pick_up_time").css("display", "block");
      }
      getCompanyName();
    });
    $("#select-weeks-for-evening").change(function () {
      if ($(this).val() == "Y") {
        $("#course_description").show();
      } else {
        $(".course_price").css("display", "block");
      }
    });
    $("#default_course_rate").keypress(function () {
      $(".start_date,.end_date").css("display", "block");
      $("#next").css("display", "block");
    });

    //
    //        $('#maximum_capacity').(function () {
    //            $('.course').css('display', 'none');
    //        });
  });
  $.ajax({
    type: "get",
    url: "/course_type_for_dropdown/",
    data: {},
    success: function (data) {
      jQuery.each(data.data, function (i, item) {
        $("#course-type").append(
          "<option value=" +
            item.id +
            " text=" +
            item.course_name +
            ">" +
            item.course_name +
            "</option>"
        );
        console.log(typeof item.course_name);
      });
    },
    error: function (data) {
      console.log(data);
      //                $('#error-msg').text(data.responseJSON.status);
    },
  });
  $.ajax({
    type: "get",
    url: "/event_type/",
    data: {},
    success: function (data) {
      jQuery.each(data.data, function (i, item) {
        $("#event_type").append(
          "<option value=" + item.id + ">" + item.type_name + "</option>"
        );
      });
    },
    error: function (data) {
      console.log(data);
      //                $('#error-msg').text(data.responseJSON.status);
    },
  });
  $.ajax({
    type: "get",
    url: "/class_status/",
    data: {},
    success: function (data) {
      jQuery.each(data.data, function (i, item) {
        $("#class_status").append(
          "<option value=" + item.id + ">" + item.status_name + "</option>"
        );
      });
    },
    error: function (data) {
      console.log(data);
      //                $('#error-msg').text(data.responseJSON.status);
    },
  });
  $.ajax({
    type: "get",
    url: "/months/",
    data: {},
    success: function (data) {
      jQuery.each(data.data, function (i, item) {
        $("#months").append(
          "<option value=" + item.id + ">" + item.month + "</option>"
        );
      });
    },
    error: function (data) {
      console.log(data);
      //                $('#error-msg').text(data.responseJSON.status);
    },
  });

  // This is location commented code.
  //     var course_type = localStorage.getItem('course_type');
  //     $.ajax({
  //         type: 'get',
  //         url: '/get_location/' + course_type,
  //         data: {

  //         },
  //         success: function(data) {
  //             jQuery.each(data.company_name, function (i, item) {
  //                 $('#location').append("<option value=" + item.location +">" + item.location__location + "</option>")
  //             });
  //         },
  //         error: function(data) {
  //             console.log(data);
  // //                $('#error-msg').text(data.responseJSON.status);
  //             },
  //         });
  //     $.ajax({
  //         type: 'get',
  //         url: '/playing_surface/',
  //         data: {

  //         },
  //         success: function(data) {
  //             jQuery.each(data.data, function (i, item) {
  //                 $('#playing_surface').append("<option value=" + item.id +">" + item.surface + "</option>")
  //             });
  //         },
  //         error: function(data) {
  //             console.log(data);
  // //                $('#error-msg').text(data.responseJSON.status);
  //             },
  //         });
  $.ajax({
    type: "get",
    url: "/get_all_coach/",
    data: {},
    success: function (data) {
      jQuery.each(data.data, function (i, item) {
        $("#lead_coach").append(
          "<option value=" + item.id + ">" + item.first_name + "</option>"
        );
      });
    },
    error: function (data) {
      console.log(data);
      //                $('#error-msg').text(data.responseJSON.status);
    },
  });
  $(document).on("click", ".add", function () {
    html = `<tr>
                <td>
                    <select class="form-control location" id="location[]" name="location[]">
                        <option>Select Locations</option>
                    </select>
                </td>
                <td>
                    <select class="form-control coach" id="coach[]" name="coach[]">
                        <option>Select Coach</option>
                    </select>
                </td>
                <td>
                    <input type="text" class="form-control total_seats" id="total_seats[]" name="total_seats[]" name="total_seats[]">
                </td>
                <td>
                    <button type="button" name="remove" class="btn btn-danger btn-sm remove"><span class="glyphicon glyphicon-minus"></span>Remove</button>
                </td>
                </tr>`;
    $("#coach-mapping").append(html);
  });

  var course_type = localStorage.getItem("course_type");
  $.ajax({
    type: "get",
    url: "/get_all_company_name/" + course_type,
    data: {},
    success: function (data) {
      jQuery.each(data.company_name, function (i, item) {
        $(".location").append(
          "<option value=" +
            item.location +
            ">" +
            item.location__location +
            "</option>"
        );
      });
    },
    error: function (data) {
      console.log(data);
    },
  });

  // var course_type = localStorage.getItem('course_type');
  // $.ajax({
  //     type: 'get',
  //     url: '/get_company_name/' + course_type,
  //     data: {

  //     },
  //     success: function(data) {
  //         jQuery.each(data.company_name, function (i, item) {
  //             $('#company_name').append("<option value=" + item.location__company__id +">" + item.location__company__company_name + "</option>")
  //         });
  //     },
  //     error: function(data) {
  //         console.log(data);
  //     },
  // });

  $.ajax({
    type: "get",
    url: "/get_all_coach/",
    data: {},
    success: function (data) {
      jQuery.each(data.data, function (i, item) {
        // $('.coach').append("<option value=" + item.id +">" + item.first_name + "</option>")
      });
    },
    error: function (data) {
      console.log(data);
    },
  });
  $(document).on("click", ".remove", function () {
    $(this).closest("tr").remove();
  });
  for (var i = 4; i <= 16; i++) {
    $("#select-weeks-for-evening").append(
      "<option value=" + i + "> Week " + i + "</option>"
    );
  }

  for (var i = 1; i <= 6; i++) {
    $("#select-weeks-for-holiday").append(
      "<option value=" + i + "> Week " + i + "</option>"
    );
  }
});

function getCompanyName() {
  var course_type = localStorage.getItem("course_type");
  $.ajax({
    type: "get",
    url: "/get_all_company_name/",
    data: {},
    success: function (data) {
      jQuery.each(data.company_name, function (i, item) {
        $("#company_name").append(
          "<option value=" + item.id + ">" + item.company_name + "</option>"
        );
      });
    },
    error: function (data) {
      console.log(data);
    },
  });

  // For Location
  // $('#location').on('change', function() {
  // $.ajax({
  //         type: 'get',
  //         url: '/get_location/' + course_type,
  //         data: {

  //         },
  //         success: function(data) {
  //             jQuery.each(data.company_name, function (i, item) {
  //                 $('#location').append("<option value=" + item.location +">" + item.location__location + "</option>")
  //             });
  //         },
  //         error: function(data) {
  //             console.log(data);
  // //                $('#error-msg').text(data.responseJSON.status);
  //             },
  //         });
}

$("#no_of_groups").on("change", function () {
  $("#age-groups").empty();

  var count = parseInt(this.value);
  console.log(count);
  var course_type = localStorage.getItem("course_type");
  console.log(course_type);
  $.ajax({
    type: "get",
    url: "/ages/" + course_type,
    data: {},
    success: function (data) {
      var myHtml = "";
      var row = "";
      // setTimeout(function() {
      //     AutoReload();
      // });
      for (var i = 1; i <= count; i++) {
        jQuery.each(data.data, function (index, item) {
          if (item.checked) {
            myHtml +=
              "<input type='radio' id='age_with_course_type' name='age_group[" +
              i +
              "]' value='" +
              item.id +
              "' required /> <span style='color:black; font-weight: 500;'>" +
              item.age +
              "</span><br>";
          } else {
            myHtml +=
              "<input type='checkbox' disabled name='age_group[" +
              i +
              "]' value='" +
              item.id +
              "'> " +
              item.age +
              "<br>";
          }
        });

        if (course_type == 3) {
          row = `<div class="row">
                                        <div class="col-md-3">
                                            <div class="form-group">
                                                <label for="from_drop_off_time">Drop off time</label>
                                                <input type="time" class="form-control" id="from_drop_off_time" name='from_drop_off_time[${i}]'>
                                            </div>
                                         </div>
                                        <div class="col-md-1">
                                            <div class="form-group">
                                            </div>
                                        </div>
                                        <div class="col-md-3">
                                            <div class="form-group">
                                                <label for="from_pick_up_time">Pick up time</label>
                                                <input type="time" class="form-control" id="from_pick_up_time" name="from_pick_up_time[${i}]">
                                            </div>
                                        </div>
                                    </div>
                                    <div class="row" style="margin-top:0px;">
                                        <div class="col-md-3">
                                            <div class="form-group">
                                                <label for="tp_drop_off_time">to</label>
                                                <input type="time" class="form-control" id="to_drop_off_time" name="to_drop_off_time[${i}]">
                                            </div>
                                         </div>
                                        <div class="col-md-1">
                                            <div class="form-group">
                                            </div>
                                        </div>
                                        <div class="col-md-3">
                                            <div class="form-group">
                                                <label for="tp_pick_up_time">to</label>
                                                <input type="time" class="form-control" id="to_pick_up_time" name="to_pick_up_time[${i}]">
                                            </div>
                                        </div>
                                    </div>`;
        } else {
          row = `<div class="row">
                                        <div class="col-md-3">
                                            <div class="form-group">
                                                <label for="start_time">Start time <sup style="color: red;">*</sup></label>
                                                <input type="time" class="form-control" id="start_time" name="start_time[${i}]" required />
                                            </div>
                                         </div>
                                        <div class="col-md-1">
                                            <div class="form-group">
                                                <label></label><br>
                                                <span>To</span>
                                            </div>
                                        </div>
                                        <div class="col-md-3">
                                            <div class="form-group">
                                                <label for="end_time">End time <sup style="color: red;">*</sup></label>
                                                <input type="time" class="form-control" id="end_time" name="end_time[${i}]" required />
                                            </div>
                                        </div>
                                    </div>`;
        }

        html = `<div class="col-md-12">
                           <fieldset class="scheduler-border">
                                <legend class="scheduler-border">Group ${i}</legend>
                                    ${myHtml}
                                    ${row}
                                <div class="row" style="margin-top:0px;">
                                    <div class="col-md-3">
                                        <div class="form-group">
                                            <label for="maximum_capacity">Maximum capacity <sup style="color: red;">*</sup></label>
                                              <input type="number" id="maximum_capacity" name="maximum_capacity[${i}]" min="1" max="150" step="1" required />
                                        </div>
                                     </div>
                                </div>
                            </fieldset>
                    </div>`;
        myHtml = "";
        $("#age-groups").append(html);
      }
    },
    error: function (data) {
      console.log(data);
      //                $('#location').text(data.responseJSON.status);
    },
  });
});

$("#location").on("change", function () {
  var course_type = localStorage.getItem("course_type");
  $.ajax({
    type: "get",
    url: "/locations/" + this.value,
    data: {},
    success: function (data) {
      $("#street").val(data.data.address_line_1).attr("readonly", true);
      $("#town").val(data.data.town).attr("readonly", true);
      $("#postal_code").val(data.data.postal_code).attr("readonly", true);
      // $('#playing_surface_name').val(data.data.playing_surface);
      $("#playing_surface")
        .val(data.data.playing_surface_id)
        .attr("readonly", true);
    },
    error: function (data) {
      console.log(data);
    },
  });
});

/**Date : 22 july 2021
 * Author: Nilesh
 * This function is created for changing locations based on selected company
 *
 */
$("#company_name").on("change", function () {
  course_type_id = localStorage.getItem("course_type");
  company_id = $("#company_name").val();

  $.ajax({
    type: "get",
    url: "/location_by_company/" + company_id,
    data: {},
    success: function (data) {
      jQuery.each(data.company_name, function (i, item) {
        $("#location").append(
          "<option value=" + item.id + ">" + item.location + "</option>"
        );
      });
    },
    error: function (data) {
      console.log(data);
      //                $('#error-msg').text(data.responseJSON.status);
    },
  });
  console.log("company changed", $("#company_name").val(), course_type_id);
});

function showSection() {
  var maximum_capacity = $("#maximum_capacity").val();
  var start_date = $("start_date").val();
  var end_date = $("#end_date").val();
  var no_of_groups = $("#no_of_groups").val();

  if (start_date != "" && end_date != "") {
    $(".no_of_groups").css("display", "block");
  }

  $(".group").css("display", "block");

  if (maximum_capacity != "" && typeof maximum_capacity != "undefined") {
    $(".course").css("display", "block");
    if (
      $("#company_name").val() != "" &&
      $(".location").val() != "" &&
      $("#street").val() != "" &&
      $("#town").val() != "" &&
      $("#postal_code").val() != "" &&
      $("#postal_code").val() != "" &&
      $("#contact_number").val() != "" &&
      $("#lead_coach").val() != "" &&
      $("#course_description").val() != ""
    ) {
      $("#confirmation").modal("show");
    }
  }
  $("#course_start_date").text($("#start_date").val());
  $("#course_price").text($("#default_course_rate").val());
}
function addRow() {
  html = `<tr>
                <td>
                    <select class="form-control location" id="location[]" name="location[]">
                        <option>Select Locations</option>
                    </select>
                </td>
                <td>
                    <select class="form-control coach" id="coach[]" name="coach[]">
                        <option>Select Coach</option>
                    </select>
                </td>
                <td>
                    <input type="text" class="form-control total_seats" id="total_seats" name="total_seats" name="total_seats[]">
                </td>
                <td>
                    <button onclick="addRow();" type="button">Add</button>
                </td>
                </tr>`;

  $("#coach-mapping").append(html);
  var course_type = localStorage.getItem("course_type");
  $.ajax({
    type: "get",
    url: "/get_location/" + course_type,
    data: {},
    success: function (data) {
      jQuery.each(data.company_name, function (i, item) {
        $(".location").append(
          "<option value=" +
            item.location +
            ">" +
            item.location__location +
            "</option>"
        );
      });
    },
    error: function (data) {
      console.log(data);
    },
  });

  $.ajax({
    type: "get",
    url: "/get_all_coach/",
    data: {},
    success: function (data) {
      jQuery.each(data.data, function (i, item) {
        $(".coach").append(
          "<option value=" + item.id + ">" + item.first_name + "</option>"
        );
      });
    },
    error: function (data) {
      console.log(data);
      //                $('#error-msg').text(data.responseJSON.status);
    },
  });

  return false;
}

// default checkbox selected message.
$("#course_default").change(function () {
  defaultmsg = "This is a Football Course for children";
  let msg;
  if ($(this).is(":checked")) {
    //    console.log('checked')
    $("#course_description").val(defaultmsg);
  } else {
    $("#course_description").val(msg);
  }
});

function saveCourse() {
  let formData = new FormData($("#course-add")[0]);
  var welcome_message = $("#confirmation-email").val();

  formData.set("status", "Published");
  formData.set("welcome_message", welcome_message);

  var token = sessionStorage.getItem("UserDetails");
  var access = JSON.parse(token);

  if (token == null) {
    window.location.href = "/";
  }

  $.ajax({
    url: "/management_courses_add_data/",
    method: "POST",
    headers: { Authorization: "Bearer " + access.access },
    enctype: "multipart/form-data",
    data: formData,
    contentType: false,
    processData: false,
    async: false,
    success: function (data) {
      //here after publish we are storing default course rate in price matric for single day data

      console.log(data);
      SaveDefaultCourseRate(data.course_detail_id);
      window.location.href = "/listing/";
    },
    error: function (data) {
      console.log(data);
    },
  });
}
function approvalCourse() {
  let formData = new FormData($("#course-add")[0]);
  var welcome_message = $("#confirmation-email").val();
  formData.set("status", "Approval Needed");
  formData.set("welcome_message", welcome_message);

  var token = sessionStorage.getItem("UserDetails");
  var access = JSON.parse(token);

  if (token == null) {
    window.location.href = "/";
  }

  $.ajax({
    url: "/management_courses_add_data/",
    method: "POST",
    headers: { Authorization: "Bearer " + access.access },
    enctype: "multipart/form-data",
    data: formData,
    contentType: false,
    processData: false,
    async: false,
    success: function (data) {
      console.log(data);
      window.location.href = "/listing/";
    },
    error: function (data) {
      console.log(data);
    },
  });
}

function confirmationEmail() {
  var course_type = localStorage.getItem("course_type");
  $("#course_type").text(course_type);
  $("#overview").modal("show");
}

$("#course_submit").on("click", function () {
  months = $("#months").val();
  locations = [];
  $(".location").each(function () {
    var count = 1;
    if ($(this).val() == "") {
      error += "<p>Select location at " + count + " Row</p>";
      return false;
    }
    locations.push($(this).val());
    count = count + 1;
  });
  coachs = [];
  $(".coach").each(function () {
    var count = 1;
    if ($(this).val() == "") {
      error += "<p>Select coach at " + count + " Row</p>";
      return false;
    }
    coachs.push($(this).val());
    count = count + 1;
  });
  total_seats = [];
  $(".total_seats").each(function () {
    var count = 1;
    if ($(this).val() == "") {
      error += "<p>Select coach at " + count + " Row</p>";
      return false;
    }
    total_seats.push($(this).val());
    count = count + 1;
  });
  //   validation = checkForm();
  //    if (validation == false) {
  //      return false;
  //    }

  let formData = new FormData($("#course-add")[0]);

  formData.set("months", months);
  formData.set("locations", locations);
  formData.set("coachs", coachs);
  formData.set("total_seats", total_seats);

  var token = sessionStorage.getItem("UserDetails");
  var access = JSON.parse(token);

  if (token == null) {
    window.location.href = "/";
  }

  $.ajax({
    url: "/management_courses_add_data/",
    method: "POST",
    headers: { Authorization: "Bearer " + access.access },
    enctype: "multipart/form-data",
    data: formData,
    contentType: false,
    processData: false,
    async: false,
    success: function (data) {
      console.log(data);
      window.location.href = "/listing/";
    },
    error: function (data) {
      console.log(data);
    },
  });
});

$(
  "#default_course_rate, #single_day, #two_days, #three_days, #four_days, #five_days"
).on("keypress keyup blur", function (event) {
  $(this).val(
    $(this)
      .val()
      .replace(/[^\d].+/, "")
  );
  if (event.which < 48 || event.which > 57) {
    event.preventDefault();
  }
});

//to save default course rate in price matrix for single day data
var version_id = 1;
function SaveDefaultCourseRate(course_detail_id) {
  if ((sessionStorage.getItem("course_type_value") == 1) || (sessionStorage.getItem("course_type_value") == 2) ) {
    var content1 = {
        course_detail: course_detail_id,
        version: version_id,
        single_day: $("#default_course_rate").val(),
      };
    
      $.ajax({
        url: "/price_matrix_for_saving_single_data/",
        method: "POST",
        contentType: "application/json",
        processData: false,
        async: false,
        data: JSON.stringify(content1),
        // success: add_success,
        // error: add_error,
      })
        .done(function () {
          //   add_success();
        })
        .fail(function () {
          return false;
        });
  }
  else{
    var content2 = {

        course_detail : course_detail_id,
        version : version_id,
        single_day : $("#single_day").val(),
        two_days : $("#two_days").val(),
        three_days : $("#three_days").val(),
        four_days : $("#four_days").val(),
        five_days : $("#five_days").val(),
    
      };
    $.ajax({
        url: "/price_matrix_for_saving_holiday_data/",
        method: "POST",
        contentType: "application/json",
        processData: false,
        async: false,
        data: JSON.stringify(content2),
        // success: add_success,
        // error: add_error,
      })
        .done(function () {
        //   add_success();
        })
        .fail(function () {
          return false;
        });
  }

}

//price_matrix_for_saving_holiday_data

