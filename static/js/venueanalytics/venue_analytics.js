$(document).ready(function () {

    var token = sessionStorage.getItem("UserDetails");
    var access_token = JSON.parse(token)


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
            function drawVisualization() {
                  // Create and populate the data table.
                  var data = google.visualization.arrayToDataTable([
                     ['Element', 'Density'],
                     ['Assigned classes', 8.94],            // RGB value
                     ['Attendance rate', 10.49],            // English color name
                     ['Cancellation', 19.30],
                     ['Re-join rate', 21.45], // CSS-style declaration
                  ]);

                  // Create and draw the visualization.
                  new google.visualization.BarChart(document.getElementById('singlebarchart')).
                      draw(data,
                           {backgroundColor: 'transparent',
                            width:400, height:500,
                            legend: 'none',
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
              ['Drop-off rate',     counts_data.total_students_booked],
              ['Re-joined rate',      2],
            ]);

            var options = {
              backgroundColor: 'transparent',
              title: 'Rates',
              width:400, height:500,
              pieHole: 0.4,
              legend: 'none',
              pieSliceText: 'label',};

            var chart = new google.visualization.PieChart(document.getElementById('venuedonutchart'));
            chart.draw(data, options);
          }
       },
        error: function(data) {
            console.log(data);
        },

});

});