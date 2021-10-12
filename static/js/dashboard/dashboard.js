$(document).ready(function () {

    $(".notification-bar margin_top15").hide()


    role = localStorage.getItem('role');


    if (role == "Super User"){
        // alert(role)
       $(".notification-bar").hide();
       
    }

    if (role == "Head Coach"){
        // alert(role)
        $('#charts').hide();
        $("#course_top_header").hide();
        $(".notification-bar").hide();
    }

    if (role == "Coach Manager"){
        $('#headcoachcharts').hide();
        $(".notification-bar").hide();
    }

    if (role == "Management") {
        $('#charts').hide();
        $('#headcoachcharts').hide();
        $('#recent_activities').hide();
        $(".notification-bar").hide();
    }

    var token = sessionStorage.getItem("UserDetails");
    var access_token = JSON.parse(token)
    var role = localStorage.getItem('role');


    if (role == "Customer")
    {
        $('#charts').hide();
        $('#headcoachcharts').hide();
        $('#recent_activities').hide();
        $('#customer-view').css({'display':'block'});
        $(".notification-bar").show();
    }



    if (token == null){
        window.location.href = "/"
    }

    var url = "/dashboard/"

    $.ajax({
        type: 'get',
        url: '/dashboard_counts/',
        headers: { Authorization: 'Bearer ' + access_token.access },
        success: function(data) {
            counts_data = JSON.parse(data.data);
            console.log(counts_data);
            google.charts.load('current', {'packages':['corechart']});
            google.charts.setOnLoadCallback(drawChart);
            function drawChart() {

              var data = google.visualization.arrayToDataTable([
              ['Course', 'Counts'],
              ['Publish courses', counts_data.all_courses],
              ['Registration rate', counts_data.total_students_booked],
              ['Cancellation', 1],
              ['Re-join rate', 2],
            ]);

              // Optional; add a title and set the width and height of the chart
              var options = {
                // showInLegend: true, 
              backgroundColor: 'transparent',
              'width':420,
              'height':300,
              legend: {
                position: 'top',
                // verticalAlign: "center", 
                // horizontalAlign: "left" ,
                labels: {
                    fontColor: "white",
                    boxWidth: 20,
                    padding: 20
                }
            },
              colors: ['#E36960', '#f18619', '#577696',
                   '#e49307', '#e49307', '#b9c246'],
              pieSliceText: 'label',};

              // Display the chart inside the <div> element with id="piechart"
              var chart = new google.visualization.PieChart(document.getElementById('piechart'));
              chart.draw(data, options);
            }



            function drawVisualization() {
                  // Create and populate the data table.
                  var data = google.visualization.arrayToDataTable([
                    ['Courses', 'Austria', 'Bulgaria'],
                    ['Assigned vs Unassigned courses', 2 ,    counts_data.all_courses],
                    ['Lead coaches vs Assisting coach vs Students',  5,    8],
                    ['Published vs Draft courses',  3,    3],
                    ['Rejoin vs drop-off rate',  15,    25],
                  ]);

                  // Create and draw the visualization.
                  new google.visualization.BarChart(document.getElementById('barchart')).
                      draw(data,
                           {backgroundColor: 'transparent',
                            width:400, height:300,isStacked: true,
                            legend: {
                                position: 'top',
                                labels: {
                                    fontColor: "white",
                                    boxWidth: 20,
                                    padding: 20
                                }
                            },
                            colors: ['#E36960', '#f18619'],
                            pieSliceText: 'label',
                            }
                      );
                  new google.visualization.BarChart(document.getElementById('barchart1')).
                      draw(data,
                           {backgroundColor: 'transparent',
                            width:400, height:500,isStacked: true,
                            legend: {
                                position: 'top',
                                labels: {
                                    fontColor: "white",
                                    boxWidth: 20,
                                    padding: 20
                                }
                            },
                            colors: ['#E36960', '#f18619'],
                            pieSliceText: 'label',
                            }
                      );
            }

            google.load("visualization", "1", {packages:["corechart"]});
            google.setOnLoadCallback(drawVisualization);







          google.charts.load("current", {packages:["corechart"]});
          google.charts.setOnLoadCallback(drawdonutChart);
          function drawdonutChart() {
            var data = google.visualization.arrayToDataTable([
              ['Purchase', 'Counts'],
            //   ['Courses',     counts_data.total_students_booked], commented on 22 july
              ['Kit',      9.3],
              ['Courses Sold',     90.7]
            ]);

            var options = {
              backgroundColor: 'transparent',
              width:400, height:300,
              pieHole: 0.4,
              legend: {
                position: 'top',
                labels: {
                    fontColor: "white",
                    boxWidth: 20,
                    padding: 20,
                    style:"Bold"
                }
            },
              colors: ['#E36960', '#f18619'],
              pieSliceText: 'label',};

            var chart = new google.visualization.PieChart(document.getElementById('donutchart'));
            chart.draw(data, options);

            var chart = new google.visualization.PieChart(document.getElementById('donutchart1'));
            chart.draw(data, options);
          }



            $('.student').text(counts_data.student);
            $('.classes').text(counts_data.classes);
            $('.absent').text(counts_data.absents);
            $('.rebook').text(counts_data.rebooked);
            $('.notificationCount').text(counts_data.notification);
            if (counts_data.notification != 0){
                txt = counts_data.notification + " new notifications require your attention.";
                $('#blue-notification').text(txt);
            }
            else{
                $('#blue-notification-row').hide();
            }


            $('.cart-value').text(counts_data.cart_count);
            localStorage.setItem("cartCount", counts_data.cart_count);
        },
        error: function(data) {
            console.log(data);
           },
        });


    $.ajax({
        type: 'get',
        url: '/recent_activities/',
        headers: { Authorization: 'Bearer ' + access_token.access },
        success: function(data) {
           jQuery.each(data.data, function (i, item) {
                html = `<tr style="box-shadow: 9px 15px 11px -15px;">
                            <td style="text-align:left";>
                                <img src=${item.user.avatar} style="border-radius: 50%;height:60px;width:60px;">
                            </td>
                            <td style="text-align:center;">
                                    <p>${item.verb}</p>
                            </td>
                            <td>
                                <span style="margin-right:10px;">
                                    ${item.timestamp}
                                </span>
                            </td>
                        </tr>`
                $('#activities').append(html);
           });

        },
        error: function(data) {
            console.log(data);
           },
        });


    $.ajax({
      type: "post",
      url: "/dashboard_page/",
      headers: { Authorization: 'Bearer ' + access_token.access },
      data: {
      },
      success: function (response) {
        if(response.data === "Management"){
            $('#student-menu').hide();
            $('#attendance-panel').hide();
        }
        else {
           if (role == "Customer") {
              $.ajax({
                url: '/events_for_customer/',
                method: 'get',
                headers: { Authorization: 'Bearer ' + access_token.access },
                success: function(doc) {

                   jQuery.each(doc.data, function (i, item) {
                        data.push({
                            title: item.title + '\n\n\n\n\n',
                            start: item.date,
                            end: item.date,
                            id: item.id,
                            color  : '#F00',
                        });
                    });
                    var calendarEl = document.getElementById('calendar');
                    var calendar = new FullCalendar.Calendar(calendarEl, {
                      initialView: 'dayGridMonth',
                      events: data,


                    });
                    calendar.render();

                }
            });
            var data = [];
            $.ajax({
                url: '/booked_events_for_customer/',
                method: 'get',
                headers: { Authorization: 'Bearer ' + access_token.access },
                success: function(doc) {
                   jQuery.each(doc.data, function (i, item) {
                        data.push(
                            {
                                title: "No. of stds emr 1",
                                start: item.start_date,
                                end: item.end_date,
                                id: i,
                            },
                            {
                                title: item.course,
                                start: item.start_date,
                                end: item.end_date,
                                id: i,
                            },
                        );
                    });
                    var calendarEl = document.getElementById('calendar');
                    var calendar = new FullCalendar.Calendar(calendarEl, {
                      initialView: 'dayGridMonth',
                      events: data,
                      eventDisplay: 'block',
                    });
                    calendar.render();

                }
            });

            var upcomingData = [];
            $.ajax({
                url: '/upcoming_courses/',
                method: 'get',
                headers: { Authorization: 'Bearer ' + access_token.access },
                success: function(doc) {

                   jQuery.each(doc.data, function (i, item) {
                        data.push(
                            {
                                title: item.course_name + "\n No of students enrolled " + item.no_of_students,
                                start: item.start_date,
                                end: item.end_date,
                                id: i,
                                color  : '#F00',
                            },
                        );
                    });
                    var calendarEl = document.getElementById('calendar');
                    var calendar = new FullCalendar.Calendar(calendarEl, {
                      initialView: 'dayGridMonth',
                      events: data,
                    });
                    calendar.render();

                }
            });
           }

        }
        if(response.status == 204){
            window.location.href = "/update_role_page/"
        }
        console.log(response);
      },
      error: function (data) {
        getAccessToken(url);
        console.log(data);
      },
    });
    var data = [];

    $.ajax({
            url: '/events_for_coach/',
            method: 'get',
            headers: { Authorization: 'Bearer ' + access_token.access },
            success: function(doc) {

               jQuery.each(doc.data, function (i, item) {
                    data.push({
                        title: item.title,
                        start: item.date,
                        end: item.date,
                        id: item.id,
                    });
                });
                var calendarEl = document.getElementById('calendar');
                var calendar = new FullCalendar.Calendar(calendarEl, {
                  initialView: 'dayGridMonth',
                  events: data,
                });
                calendar.render();

            }
        });





    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      events: data,
    });
    calendar.render();

//    document.addEventListener('DOMContentLoaded', function() {
//
//      });
    $.ajax({
        type: 'get',
        url: '/student_booked/',
        headers: { Authorization: 'Bearer ' + access_token.access },
        success: function(data) {
            jQuery.each(data.data, function (i, item) {
                $('#student,#student1').append("<option value=" + item.student.id +">" + item.student.first_name + "</option>")
            });
        },
        error: function(data) {
            console.log(data);
//                $('#error-msg').text(data.responseJSON.status);
            },
        });
})





function confirm(){
    var token = sessionStorage.getItem("UserDetails");
    var access_token = JSON.parse(token)
    if($("input[name='is_absent']").is(':checked')) {
        var is_absent = $("input[name='is_absent']:checked").val();
    }
    else {
        return false;
    }

    if (is_absent == "Yes")
    {
        $('#std-name').text($('#select2-chosen-1').text());

        $('#absentModal').modal('show');
    }
    else {
        $('#std-name1').text($('#select2-chosen-1').text());
        $('#rebookModal').modal('show');
    }
}


function absent(){
    var token = sessionStorage.getItem("UserDetails");
    var access_token = JSON.parse(token)
    $.ajax({
                type: 'post',
                url: '/events_for_customer/',
                headers: { Authorization: 'Bearer ' + access_token.access },
                data: {
                    'date': $('#date').val(),
                    'student': $('#student').val(),
                },
                success: function(data) {
                    location.reload();
                    window.location.href = "/dashboard/";
                },
                error: function(data) {
                       console.log(data);
                    },
                });
}


function rebook(){


    var token = sessionStorage.getItem("UserDetails");
    var access_token = JSON.parse(token)
    $.ajax({
        type: 'post',
        url: '/events_for_coach/',
        headers: { Authorization: 'Bearer ' + access_token.access },
        data: {
            'date': $('#date1').val(),
            'student': $('#student').val(),
            'title': "ReBook"
        },
        success: function(data) {
            location.reload();
            window.location.href = "/dashboard/";
        },
        error: function(data) {
               console.log(data);
            },
        });
}


$('#student1').change(function () {
    $.ajax({
        type: 'get',
        url: '/get_tokens/',
        data: {
            'student': this.value,
        },
        success: function(data) {
            $('#tokens').val(data.tokens);
        },
        error: function(data) {
               console.log(data);
            },
        });
})



function close_notification(){
    // alert("hello");
    $(".notification-bar").hide();
}


