var courseTitle = "";
var course_id = $("#course-id").val();

$(function () {
  localStorage.setItem("course_type_id", course_id);
  console.log(course_id);
  getCourseDetails();
});

$("#search").click(function () {
  let month = $("#date").val();
  let id = $("#location").val();
  localStorage.setItem("location_id", id);
  if (parseInt(id) == 0) {
    toastr.error("Please select location");
    return false;
  }
  if (parseInt(month) == 0) {
    toastr.error("Please select date");
    return false;
  }
});

function changeFunc() {
  
  var selectBox = document.getElementById("venue");
  var selectedValue = selectBox.options[selectBox.selectedIndex].value;
  localStorage.setItem("location_id", selectedValue);
  venueByCourseDetail(selectedValue)
  // window.location.href = "/course_edit_by_venue/";
}

function changeFuncForVenue(){
  var selectBox = document.getElementById("course_detail_id_by_venue");
  var selectedValue = selectBox.options[selectBox.selectedIndex].value;
  localStorage.setItem("course_detail_id", selectedValue);
  window.location.href = "/course_edit_by_venue/";
}

function GoToVenue(data) {
  localStorage.setItem("location_id", data);
  // window.location.href = "/course_edit_by_venue/";
}

function ToSeePostcodeSearch() {
  var postcode_value = (document.getElementById("Entered_postcode").value).toUpperCase();
  console.log('upper case',postcode_value.toUpperCase())
  $(".all_mile").empty();

  $(".postcode_window").css({
    display: "none",
  });
  $.ajax({
    url: "/get_distance_by_postcode/",
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    data: JSON.stringify({
      postcode: postcode_value,
      course_type_id: localStorage.getItem("course_type_id"),
    }),
    // async: false,
    success: function (data) {
      if (data.message.length > 0) {
        jQuery.each(data.message, function (i, item) {
          html = `
                    <div class="all_miles">
                        <div class="fst_div">
                            <h5 class="location_postcode">${item.location}</h5>
                            <p>
                                <span>${item.address}</span>
                                <span>${item.town}</span>
                                <span>${item.postal_code}</span>
                                <span>${item.country}</span>
                            </p>
                        </div>

                        <div class="mile_div">
                            <h5>${item.distance}</h5>
                        </div>
                        <div class="select_venue">
                            <button onclick="GoToVenue(${item.location_id})">Select Venue </button>
                        </div>
                    </div>
                `;

          $(".all_mile").append(html);
        });
      }

      $(".postcode_window").css({
        display: "block",
      });
      console.log(courseTitle);
      if (data.message.length == 0) {
        $("#course_title").text(`No result found.`);
      } else {
        $("#course_title").text(`${courseTitle}`);
      }
    },

    error: function (data, status) {
      toastr.error(data.responseJSON.message);
    },
  });
}

// GET course details
function getCourseDetails() {
  $.ajax({
    type: "get",
    url: "/course_detail_data/" + course_id,
    data: {},
    success: function (data) {
      localStorage.setItem("course_type_name", data.data.course_type.course_name);
      courseTitle = data.data.course_type.course_title;
      let htmlTem = `<article class="post-corporate" id=${course_id}>
                        <div class="post-corporate-content">
                        <div class="post-corporate-header" id="course_name">
                            ${data.data.course_type.course_title}
                        </div>
                        <div class="post-corporate-text">
                            <div id="course-detail">${data.data.course_type.course_description}</div>
                            <h4>Find a venue</h4>
                            <input type=text placeholder="Enter Your Postcode" maxlength="8" value="" id="Entered_postcode" /> <button onclick = "ToSeePostcodeSearch()" class="to_see_locations_by_postcode">GO</button> <span class="or"> or </span>
                           
                            <select class="select select-minimal" id="venue" onchange="changeFunc();"
                                    data-placeholder="Select an option"
                                    data-dropdown-class="select-minimal-dropdown" style="min-width: 150px">
                                <option value="0" selected="">Select a Venue</option>
                            </select>
                            <select class="select select-minimal" id="course_detail_id_by_venue" style="
                            background-color: blue;" onchange="changeFuncForVenue();"
                            data-placeholder="Select an option"
                            data-dropdown-class="select-minimal-dropdown" style="min-width: 150px">
                        <option value="0" selected="">Select a Venue</option>
                    </select>
                            
                            <span id="error"></span>
                        </div>
                        <div class = "postcode_window">
                            <div class="modal-header">
                                <h4 class="modal-title">${data.data.course_type.course_title}</h4>
                            </div>
                            <div class="modal-body">
                                <h3 id="course_title">Available holiday clubs near you.</h3>
                                <div class="all_mile">
                                    
                            </div>
                        </div>
                        </div>
                        <div id="course_type_logo">
                        <img src="${data.data.logo}" alt="${data.data.course_type.course_title}"/>
                        </div>
                        <br>
                        <div class="card card-custom" id="classes" style="padding-left:0px;">
    
                        </div>
                        <div id="location">
                        </div>
                    </div>
                </article>
                `;

      $("#course_detail_html").append(htmlTem);
      getLocation();
    },
    error: function (data) {
      $("#location").text(data.responseJSON.status);
    },
  });
}

// GET LOCATION
// function getLocation() {
//   $.ajax({
//     type: "get",
//     url: "/get_location/" + course_id,
//     data: {},
//     success: function (data) {
//       var counter = 0
//       jQuery.each(data.company_name, function (i, item) {
//         counter = counter +1
//         $("#venue").append(
//           "<option value=" +
//             item.location +
//             ">" +
//             item.location__location + " - " + counter +
//             "</option>"
//         );
//       });
//     },
//     error: function (data) {
//       $("#venue").text(data.responseJSON.status);
//     },
//   });
// }

function getLocation() {
  venueByCourseDetail()
  var token = sessionStorage.getItem("UserDetails");
  var access = JSON.parse(token)
  $.ajax({
    type: "GET",

    url: "/get_venues_by_status/",
    data: {},
    success: function (data) {

      var counter = 0
      console.log(data)
      jQuery.each(data.data, function (i, item) {

        if (item.course_type_id == localStorage.getItem("course_type_id") && ((item.completed/item.no_of_weeks)*100 <= 80)){
          counter = counter +1
          $("#venue").append(
            "<option value=" +
              item.location_id +
              ">" +
              item.location + " - " + counter +
              "</option>"
          );

        }
  
      });
    },
    error: function (data) {
      $("#venue").text(data.responseJSON.status);
    },
  });
}

// $('#venue').on('change', function() {
  
// }

// course_detail_id_by_venue

function venueByCourseDetail(selectedValue) {
  $("#course_detail_id_by_venue").find('option').remove().end()
  .append('<option value="0">Select Venue</option>')
  .val('0')
;


  var token = sessionStorage.getItem("UserDetails");
  var access = JSON.parse(token)
  $.ajax({
    type: "GET",

    url: "/course_detail_by_location/" + selectedValue + "/" + localStorage.getItem("course_type_id") ,
    data: {},
    success: function (data) {
      var counter = 0
      console.log(data)

      jQuery.each(data, function (i, item) {
        if (((item.completed/item.no_of_weeks)*100 <= 80)){
       
          counter = counter +1
          $("#course_detail_id_by_venue").append(
            "<option id='abcd' value=" +
              item.id +
              ">"+ localStorage.getItem("course_type_name")+ " - " +
              item.start_date + " to " + item.end_date  +
              "</option>"
          );
        
        }
        
  
      });
    },
    error: function (data) {
      // $("#course_detail_id_by_venue").text(data.responseJSON.status);
    },
  });
}