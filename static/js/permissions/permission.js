$(document).ready(function () {
  $(".master").hide();
  $(".coach").hide();
  $(".notification").hide();
  $(".download").hide();
  $("#student-menu").hide();
  $(".addstudent").hide();
  $(".record").hide();
  $(".staff").hide();
  $(".customer").hide();
  $(".superuser").hide();
  $(".venue_analytics").hide();
  $("#student-add-menu").hide();
  $(".rota_in_menu").hide();
  $(".class_register_in_menu").hide();
  $(".venue_analytics_in_menu").hide();
  $(".child_header").hide();

  // $('#class_register').hide();
  // $("#course_listing_header").hide();
  // $("#message_header").hide();
  // $("#booking_header").hide();
  // $("#staff_header").hide();
  // $("#coach_header").hide();
  // $("#parent_header").hide();
  // $("#location_header").hide();
  // $("#reviews_header").hide();
  // $("#download_header").hide();
  // $("#child_header").hide();
  // $("#financial_report_header").hide();
  SetPermissionsUserDashboard();

  cartCount = localStorage.getItem("cartCount");
  if (cartCount !== "0") {
    $(".cart-value").text(cartCount);
  }

  $("#current_date").text(new Date().toDateString());

  var token = sessionStorage.getItem("UserDetails");
  var access_token = JSON.parse(token);

  if (token !== null) {
    $.ajax({
      type: "get",
      url: "/dashboard_counts/",
      headers: { Authorization: "Bearer " + access_token.access },
      success: function (data) {
        counts_data = JSON.parse(data.data);
        console.log(counts_data);
        $("#weekly-count").text(counts_data.weekly_football_count);
        $("#nursery-count").text(counts_data.nursery);
        $("#holiday-count").text(counts_data.holiday);
        $("#weekly-location-count").text(
          counts_data.evening_development_locations
        );
        $("#nursery-location-count").text(counts_data.nursery_locations);
        $("#holiday-location-count").text(counts_data.holiday_locations);
        if (counts_data.notification != 0) {
          txt =
            counts_data.notification +
            " new notifications require your attention.";
          $("#blue-notification").text(txt);
        } else {
          $("#blue-notification-row").hide();
        }
      },
      error: function (data) {
        console.log(data);
      },
    });
  }
});

function SetPermissionsUserDashboard() {
  var userPermissions = localStorage.getItem("UserPermissions");

  var role = localStorage.getItem("role");
  console.log(role);
  if (localStorage.getItem("role") == "Super User") {
      if(!jQuery.isEmptyObject(userPermissions)){
    
     
      if (userPermissions.includes('master_pages_get')){
          $( ".master" ).show();
          $(".rota_in_menu").hide();
          $(".class_register_in_menu").hide();
          $(".venue_analytics_in_menu").hide();
      }
      if (userPermissions.includes('coach_pages')){
          $( ".coach" ).show();
      }
      if (userPermissions.includes('student_menu_get')){
          $( "#student-menu" ).show();
      }
      if (userPermissions.includes("class_register_menu_get")) {
        $(".child_header").hide();
      }
      if (userPermissions.includes('download_menu')){
          $( ".download" ).show();
      }
      if (userPermissions.includes('notification_menu_get')){
          $( ".notification" ).show();
      }
      if (userPermissions.includes('notification_header_get')){
          $( "#message_header" ).show();
      }
      if (userPermissions.includes('map_student_to_course')){
          $( ".addstudent" ).show();
      }
      if (userPermissions.includes('account_record_menu_get')){
          $( ".record" ).show();
      }
      if (userPermissions.includes('staff_menu_get')){
          $( ".staff" ).show();
      }
      if (userPermissions.includes('super_user_menu_get')){
          $( ".superuser" ).show();
      }
      if (userPermissions.includes('master_pages_get')){
          $( ".customer" ).show();
      }
      if (userPermissions.includes('venuanalytics_menu_get')){
          $( "#venue_analytics" ).show();

      }
      if (userPermissions.includes('class_register_menu_get')){
          $( "#class_register" ).show();
      }

      // if (userPermissions.includes('')){
      //     $("#course_listing_header").show()
      // }
  }
  }
  if (localStorage.getItem("role") == "Management") {
    if(!jQuery.isEmptyObject(userPermissions)){
  
    
    if (userPermissions.includes('master_pages_get')){
        $( ".master" ).show();
        $(".rota_in_menu").hide();
        $(".class_register_in_menu").hide();
        $(".venue_analytics_in_menu").hide();

    }
    if (userPermissions.includes('coach_pages')){
        $( ".coach" ).show();
    }
    if (userPermissions.includes('student_menu_get')){
        $( "#student-menu" ).show();
    }
    if (userPermissions.includes('download_menu')){
        $( ".download" ).show();
    }
    if (userPermissions.includes('notification_menu_get')){
        $( ".notification" ).show();
    }
    if (userPermissions.includes('notification_header_get')){
        $( "#message_header" ).show();
    }
    if (userPermissions.includes('map_student_to_course')){
        $( ".addstudent" ).show();
    }
    if (userPermissions.includes('account_record_menu_get')){
        $( ".record" ).show();
    }
    if (userPermissions.includes('staff_menu_get')){
        $( ".staff" ).show();
    }
    if (userPermissions.includes('super_user_menu_get')){
        $( ".superuser" ).show();
    }
    if (userPermissions.includes('master_pages_get')){
        $( ".customer" ).show();
    }
    if (userPermissions.includes('venuanalytics_menu_get')){
        $( "#venue_analytics" ).show();

    }
    if (userPermissions.includes('class_register_menu_get')){
        $( "#class_register" ).show();
    }

    // if (userPermissions.includes('')){
    //     $("#course_listing_header").show()
    // }
}
}



  if (localStorage.getItem("role") == "Customer") {
    $(".child_header").show();
    if (!jQuery.isEmptyObject(userPermissions)) {
      if (userPermissions.includes("master_pages_get")) {
        $(".master").show();
      }
      if (userPermissions.includes("coach_pages")) {
        $(".coach").show();
      }
      if (userPermissions.includes("student_menu_get")) {
        $("#student-menu").hide();
      }
      if (userPermissions.includes("download_menu")) {
        $(".download").show();
      }
      if (userPermissions.includes("notification_menu_get")) {
        $(".notification").show();
      }
      if (userPermissions.includes("notification_header_get")) {
        $("#message_header").show();
      }
      if (userPermissions.includes("map_student_to_course")) {
        $(".addstudent").show();
      }
      if (userPermissions.includes("account_record_menu_get")) {
        $(".record").show();
      }
      if (userPermissions.includes("staff_menu_get")) {
        $(".staff").show();
      }
      if (userPermissions.includes("super_user_menu_get")) {
        $(".superuser").show();
      }
      if (userPermissions.includes("master_pages_get")) {
        $(".customer").show();
      }
      if (userPermissions.includes("venuanalytics_menu_get")) {
        $(".venue_analytics").show();
      }
      if (userPermissions.includes("class_register_menu_get")) {
        $(".class_register").show();
      }
      if (userPermissions.includes("class_register_menu_get")) {
        $(".child_header").show();
      }
      if (userPermissions.includes("location_header_get")) {
        $("#location_header").hide();
      }
      if (userPermissions.includes("coach_header_get")) {
        $("#coach_header").hide();
      }
      if (userPermissions.includes("parent_header_get")) {
        $("#parent_header").hide();
      }
      if (userPermissions.includes("staff_header_get")) {
        $("#staff_header").hide();
      }
      if (userPermissions.includes("booking_header_get")) {
        $("#booking_header").hide();
      }
      if (userPermissions.includes("booking_header_get")) {
        $("#booking_header").show();
        $("#reviews_header").hide();
        $("#download_header").hide();
        $("#financial_report_header").hide();
      }
      if (userPermissions.includes("")) {
        $("#course_listing_header").hide();
      }
    }


  }


  if (localStorage.getItem("role") == "Head Coach") {
    $(".rota_in_menu").show();
    $(".class_register_in_menu").show();
    $(".venue_analytics_in_menu").show();
    $("#courses_header").hide();
    $("#child_header").hide();
    $("#booking_header").hide();
    if (!jQuery.isEmptyObject(userPermissions)) {
      if (userPermissions.includes("master_pages_get")) {
        $(".master").show();
      }
      if (userPermissions.includes("coach_pages")) {
        $(".coach").hide();
      }
      if (userPermissions.includes("student_menu_get")) {
        $("#student-menu").hide();
      }
      if (userPermissions.includes("download_menu")) {
        $(".download").show();
      }
      if (userPermissions.includes("notification_menu_get")) {
        $(".notification").show();
      }
      if (userPermissions.includes("notification_header_get")) {
        $("#message_header").show();
      }
      if (userPermissions.includes("map_student_to_course")) {
        $(".addstudent").show();
      }
      if (userPermissions.includes("account_record_menu_get")) {
        $(".record").show();
      }
      if (userPermissions.includes("staff_menu_get")) {
        $(".staff").show();
      }
      if (userPermissions.includes("super_user_menu_get")) {
        $(".superuser").show();
      }
      if (userPermissions.includes("master_pages_get")) {
        $(".customer").show();
      }
      if (userPermissions.includes("venuanalytics_menu_get")) {
        $(".venue_analytics").show();
      }
      if (userPermissions.includes("class_register_menu_get")) {
        $(".class_register").show();
      }
      if (userPermissions.includes("class_register_menu_get")) {
        $("#child_header").hide();
      }
      if (userPermissions.includes("location_header_get")) {
        $("#location_header").hide();
      }
      if (userPermissions.includes("coach_header_get")) {
        $("#coach_header").hide();
      }
      if (userPermissions.includes("parent_header_get")) {
        $("#parent_header").hide();
      }
      if (userPermissions.includes("staff_header_get")) {
        $("#staff_header").hide();
      }
      if (userPermissions.includes("booking_header_get")) {
        $("#booking_header").hide();
      }
      if (userPermissions.includes("booking_header_get")) {

        $("#reviews_header").hide();
        $("#download_header").hide();
        $("#financial_report_header").hide();
      }
      if (userPermissions.includes("")) {
        $("#course_listing_header").hide();
      }
    }


  }

  if (localStorage.getItem("role") == "Coach Manager") {
    $(".rota_in_menu").show();
    $(".class_register_in_menu").show();
    $(".venue_analytics_in_menu").show();
    $("#courses_header").hide();
    $("#child_header").hide();
    $("#booking_header").hide();
    $("#reviews_header").hide();
    $("#parent_header").hide();
    $("#financial_report_header").hide();
    if (!jQuery.isEmptyObject(userPermissions)) {
      if (userPermissions.includes("master_pages_get")) {
        $(".master").show();
      }
      if (userPermissions.includes("coach_pages")) {
        $(".coach").hide();
      }
      if (userPermissions.includes("student_menu_get")) {
        $("#student-menu").hide();
      }
      if (userPermissions.includes("download_menu")) {
        $(".download").show();
      }
      if (userPermissions.includes("notification_menu_get")) {
        $(".notification").show();
      }
      if (userPermissions.includes("notification_header_get")) {
        $("#message_header").show();
      }
      if (userPermissions.includes("map_student_to_course")) {
        $(".addstudent").show();
      }
      if (userPermissions.includes("account_record_menu_get")) {
        $(".record").show();
      }
      if (userPermissions.includes("staff_menu_get")) {
        $("#staff_header").show();
      }
      if (userPermissions.includes("super_user_menu_get")) {
        $(".superuser").show();
      }
      if (userPermissions.includes("master_pages_get")) {
        $(".customer").show();
      }
      if (userPermissions.includes("venuanalytics_menu_get")) {
        $(".venue_analytics").show();
      }
      if (userPermissions.includes("class_register_menu_get")) {
        $(".class_register").show();
      }
      if (userPermissions.includes("class_register_menu_get")) {
        $("#child_header").hide();
      }
      if (userPermissions.includes("location_header_get")) {
        $("#location_header").hide();
      }
      if (userPermissions.includes("coach_header_get")) {
        $("#coach_header").hide();
      }
      if (userPermissions.includes("parent_header_get")) {
        $("#parent_header").hide();
      }
      if (userPermissions.includes("staff_header_get")) {
        $("#staff_header").show();
      }
      if (userPermissions.includes("booking_header_get")) {
        $("#booking_header").hide();
      }
      if (userPermissions.includes("booking_header_get")) {

      
        $("#download_header").hide();
        
      }
      if (userPermissions.includes("location_header_get")) {
        $("#course_listing_header").show();
      }
    }


  }


}
