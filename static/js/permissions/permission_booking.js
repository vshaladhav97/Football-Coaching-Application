$(document).ready(function () {
    $('.master').hide();
    $('.coach').hide();
    $('.notification').hide();
    $('.download').hide();
    $('#student-menu').hide();
    $('.addstudent').hide();
    $( ".record" ).hide();
    $(".staff").hide();
    $('.customer').hide();
    $('.superuser').hide();
    $('.venue_analytics').hide();
    $('#class_register').hide();
    SetPermissionsUserDashboard();


    cartCount = localStorage.getItem('cartCount')
    if (cartCount !== "0"){
        $('.cart-value').text(cartCount);
    }

    $('#current_date').text(new Date().toDateString());

    var token = sessionStorage.getItem("UserDetails");
    var access_token = JSON.parse(token)

    if (token !== null){
        $.ajax({
        type: 'get',
        url: '/book/',
        headers: { Authorization: 'Bearer ' + access_token.access },
        success: function(data) {
            counts_data = JSON.parse(data.data);
            console.log(counts_data);
            $('#weekly-count').text(counts_data.weekly_football_count);
            $('#nursery-count').text(counts_data.nursery);
            $('#holiday-count').text(counts_data.holiday);
            $('#weekly-location-count').text(counts_data.evening_development_locations);
            $('#nursery-location-count').text(counts_data.nursery_locations);
            $('#holiday-location-count').text(counts_data.holiday_locations);
            if (counts_data.notification != 0){
                txt = counts_data.notification + " new notifications require your attention.";
                $('#blue-notification').text(txt);
            }
            else{
                $('#blue-notification-row').hide();
            }
        },
        error: function(data) {
            console.log(data);
           },
        });
    }

})

function SetPermissionsUserDashboard(){
    var userPermissions = localStorage.getItem('UserPermissions')

    if(!jQuery.isEmptyObject(userPermissions)){
        if (userPermissions.includes('master_pages')){
            $( ".master" ).show();
        }
        if (userPermissions.includes('coach_pages')){
            $( ".coach" ).show();
        }
        if (userPermissions.includes('student_menu')){
            $( "#student-menu" ).show();
        }
        if (userPermissions.includes('download_menu')){
            $( ".download" ).show();
        }
        if (userPermissions.includes('notification_menu')){
            $( ".notification" ).show();
        }
        if (userPermissions.includes('map_student_to_course')){
            $( ".addstudent" ).show();
        }
        if (userPermissions.includes('account_record_menu')){
            $( ".record" ).show();
        }
        if (userPermissions.includes('staff_menu')){
            $( ".staff" ).show();
        }
        if (userPermissions.includes('super_user_menu')){
            $( ".superuser" ).show();
        }
        if (userPermissions.includes('master_pages')){
            $( ".customer" ).show();
        }
        if (userPermissions.includes('venuanalytics_menu')){
            $( ".venue_analytics" ).show();
        }
        if (userPermissions.includes('class_register_menu')){
            $( ".class_register" ).show();
        }
    }
}