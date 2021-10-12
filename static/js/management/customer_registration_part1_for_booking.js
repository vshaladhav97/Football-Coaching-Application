var counter = 0;
$(document).ready(function () {
  course = localStorage.getItem("course");
  $.ajax({
    type: "get",
    url: "/edit_booking/" + course,

    data: {},
    success: function (data) {
      $("#edit-booking").empty();
      console.log(data.data, "booking data");

      html = `BOOKINGS - ${data.data.course_type} - ${data.data.location}`;
      $(`#booking_header`).append(html);
    }, // success function ends here.
  }); //ajax ends here
}); //document.ready ends here

$(document).on("submit", ".customer-form", function (e) {
  var token = localStorage.getItem("UserDetails");
  var access_token = JSON.parse(token);

  alert("hello");

  $.ajax({
    url: "/registration_post/",
    method: "POST",
    enctype: "multipart/form-data",
    headers: { Authorization: "Bearer " + access_token.access },
    data: formData,
    contentType: false,
    processData: false,
    async: false,
    success: function (data) {
      console.log(data);
      alert("data is added succesfully");

    },
    error: function (data) {
      alert("data is not added succesfully");
      console.log(data);
    },
  });
});

var start_date;
$(document).ready(function () {
  course = localStorage.getItem("course");

  $.ajax({
    type: "get",
    url: "/edit_booking/" + course,
    data: {},
    success: function (data) {
      $("#course_type").html(data.data.course_type);
      $("#start_date_with_day").html(data.data.start_date_with_day);
      $("#no_of_weeks").html(data.data.no_of_weeks);
      $("#default_course_rate").html(data.data.default_course_rate);
      $("#logo").attr("src", data.data.logo);
      $("#location").html(data.data.location);
      $("#day_filter").html(data.data.day_filter);
      $("#start_time").html(data.data.course_group);
      $("#end_time").html(data.data.course_group);
      $("#abcd").each(function (item) {
        item.append(data.data.course_group.age);
      });
    },
    error: function (data) {
      //            console.log(data);
      $("#error-msg").text(data.responseJSON.status);
    },
  });
});

function go_back() {
  window.location.href = "/management_book_edit_page/";
}

function AddCustomer() {
  // var token = localStorage.getItem('UserDetails');
  console.log("hello");
  // var ab = localStorage.getItem("user_id");
  // console.log(ab)

  // var access_token = JSON.parse(token)
  // console.log(access_token.access)

  var first_name = $("#first_name").val();
  var last_name = $("#last_name").val();
  var email = $("#email").val();
  var phone_number = $("#phone_number").val();
  var mobile = $("#mobile").val();
  var address = $("#address").val();
  var postcode = $("#postcode").val();
  var country_code = $("#country_code").val();
  var image = $("#profile-pic").val();
  var password = $("#password").val();

  var formData = new FormData();
  formData.append("image", $("#profile-pic")[0].files[0]);
  formData.append("first_name", first_name);
  formData.append("last_name", last_name);
  formData.append("email", email);
  formData.append("landline", phone_number);
  formData.append("mobile", mobile);
  formData.append("address", address);
  formData.append("postal_code", postcode);
  formData.append("country_code", country_code);

  formData.append("password", password);

  var content = {
    // "user_id": localStorage.getItem("user_id"),

    first_name: first_name,
    last_name: last_name,
    email: email,
    landline: phone_number,
    mobile: mobile,
    address: address,
    postal_code: postcode,
    country_code: country_code,
    profile_image: image,
    password: password,
  };
  $.ajax({
    url: "/customers/",

    method: "POST",
    enctype: "multipart/form-data",
    data: formData,
    contentType: false,
    processData: false,
    async: false,

    success: function (data) {
      console.log("customer", data)
      if (data){
        localStorage.setItem('customer_id', data.customer_id)
      }
      window.location.href = "/child_registration_for_booking/";
    },
    error: function (data) {

      $("#error-msg").text(data.responseJSON.status);
    },
    // "error": add_error
  }); // ajax()

}