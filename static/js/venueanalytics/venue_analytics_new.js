// var counter = 0;

// $("#coach-heading").hide();
// $("#coach-analytics").hide();
$("#coach-heading").hide();
$("#coach-analytics").hide();
$("#venue-heading").hide();
$("#venue-analytics").hide();
$("#coach-selection").hide();
$("#venue-selection").hide();
$(document).ready(function (){

    var token = sessionStorage.getItem("UserDetails");
    var access_token = JSON.parse(token)


    if (token == null){
        window.location.href = "/"
    }

    // var url = "/dashboard/"

    $.ajax({
        type: 'get',
        url: '/venue_analytics_count/',
        headers: { Authorization: 'Bearer ' + access_token.access },
        success: function(data) {
    
        console.log(data);
            
            $("#total_course").html(data[0].total_course);   
            $("#total_attendence").html(data[0].total_attendence);   
            $("#total_student").html(data[0].total_student);
            $("#courses_unstaffed").html(data[0].courses_unstaffed); 

       },
        error: function(data) {
            console.log(data);
        },

    }); //ajax ends here


        }); //document.ready ends here


$(document).ready(function(){
    var token = sessionStorage.getItem("UserDetails");
    var access_token = JSON.parse(token)


    if (token == null){
        window.location.href = "/"
    }


    $.ajax({
        type: 'get',
        url: '/coach_list_analytics/',
        headers: { Authorization: 'Bearer ' + access_token.access },
        success: function(data) {
            
            
        
                            jQuery.each(data, function (i, item) {   
                                html = 
                            `
                            
                            
                            <option id="${item.id}" onclick="filter_coach(${item.id})" value="${item.first_name}">${item.first_name}</option>
                            
                            `
                            $("#selction-option-coach").append(html);
                            
                            });
                            
              
       },
        error: function(data) {
            console.log(data);
        },

    }); //ajax ends here

    $.ajax({
        type: 'get',
        url: '/venue_list_analytics/',
        headers: { Authorization: 'Bearer ' + access_token.access },
        success: function(data) {
            
            console.log(data);
        
                            jQuery.each(data, function (i, item) {   
                                    html = 
                                `
                                <option value="${item.location}">${item.location}</option>
                                `
                            $("#selction-option-venue").append(html);
                            });
                            
              
       },
        error: function(data) {
            console.log(data);
        },

    });

}); //document ready ends here

function get_overview(){
    $("#coach-heading").hide();
    $("#coach-analytics").hide();
    $("#overview-heading").show();
    $("#overview-analytics").show();
    $("#venue-heading").hide();
    $("#venue-analytics").hide();
    $("#coach-selection").hide();
    $("#venue-selection").hide();
}

function get_coach(){
   
    $("#overview-heading").hide();
    $("#venue-heading").hide();
    $("#coach-heading").show();
    $("#overview-analytics").hide();
    $("#coach-analytics").show();
    $("#venue-analytics").hide();
    $("#coach-selection").show();
    $("#venue-selection").hide();



}

function get_venue(){
    $("#overview-heading").hide();
    $("#overview-analytics").hide();
    $("#coach-heading").hide();
    $("#coach-analytics").hide();
    $("#venue-heading").show();
    $("#venue-analytics").show();
    $("#coach-selection").hide();
    $("#venue-selection").show();
}


function dynamic_coach_count(id){
    var token = sessionStorage.getItem("UserDetails");
    var access_token = JSON.parse(token)
    $.ajax({
        type: 'get',
        url: '/venue_analytics_count/' + id,
        headers: { Authorization: 'Bearer ' + access_token.access },
        success: function(data) {
    
        console.log(data);
            
            $("#total_course").html(data[0].total_course);   
            $("#total_attendence").html(data[0].total_attendence);   
            $("#total_student").html(data[0].total_student);   

       },
        error: function(data) {
            console.log(data);
        },

    }); //ajax ends here
}


function getval(sel)
{
    var coach_id = $('#selction-option-coach :selected').attr("id");
    alert(coach_id);
    dynamic_coach_count(coach_id)

}





// function filter_coach(id){
//     alert(id);
// }

// function

