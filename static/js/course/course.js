$(window).load(function () {
    $.ajax({
        type: "get",
        url: "/get_all_locations/",
        data: {},
        success: function (data) {
            jQuery.each(data.data, function (i, item) {
                $("#location").append(
                    "<option value=" + item.id + ">" + item.location + "</option>"
                );
            });
        },
        error: function (data) {
            console.log(data);
            //                $('#location').text(data.responseJSON.status);
        },
    });

    $.ajax({
        type: "get",
        url: "/age_group/",
        data: {},
        success: function (data) {
            jQuery.each(data.data, function (i, item) {
                $("#age-group").append(
                    "<option value=" + item.id + ">" + item.age_group_text + "</option>"
                );
            });
        },
        error: function (data) {
            console.log(data);
            //                $('#location').text(data.responseJSON.status);
        },
    });

    $.ajax({
        type: "get",
        url: "/course_type/",
        data: {},
        success: function (data) {
            jQuery.each(data.data, function (i, item) {
                $("#course-type").append(
                    "<option value=" + item.id + ">" + item.course_name + "</option>"
                );
            });
        },
        error: function (data) {
            console.log(data);
            //                $('#location').text(data.responseJSON.status);
        },
    });

    //     $.ajax({
    //         type: 'get',
    //         url: '/course_listing_data/',
    //         data: {},
    //         success: function(data) {
    //             console.log(data)
    //             jQuery.each(data.data, function (i, item) {

    //                html = '<div class="col-md-6 col-lg-3">'+
    //                       '<div class="card">'+
    //                           '<center>'+
    //                           '<div class="card-header" style="background-color:#35ad79;color:black;">'+
    //                                 item.course_type.course_name +
    //                                 '<br>'+
    //                           '</div>'+
    //                           '</center>'+
    //                           '<div class="card-body" style="height:200px;">'+
    // //                               '<h5 class="card-title">Special title treatment</h5>'+
    //                                '<p class="card-text">'+ item.course_description +'</p>'+
    //                           '</div>'+
    //                           '<div class="card-footer">'+
    //                                 '<center>'+
    //                                 '<a href="/course_detail/'+ item.id +'" class="btn btn-primary">More</a>'+
    //                                  '</center>'+
    //                           '</div>'+
    //                       '</div>'+
    //                       '</div>'

    //                 $('#course-list').append(html);
    //             });
    //         },
    //         error: function(data) {
    //             console.log(data);
    // //                $('#error-msg').text(data.responseJSON.status);
    //             },
    //         });
    $.ajax({
        type: "get",
        url: "/course_category/",
        data: {},
        success: function (data) {
            console.log(data);
            jQuery.each(data.data, function (i, item) {
                if (item.course_name != "Parties") {
                    html =
                        '<div class="col-md-6 col-lg-3 courses_list">' +
                        '<div class="card">' +
                        "<center>" +
                        '<div class="card-header">' +
                        "<span>" +
                        item.course_title +
                        "</span>" +
                        "</div>" +
                        "</center>" +
                        '<div class="card-body">' +
                        //                               '<h5 class="card-title">Special title treatment</h5>'+
                        '<p class="card-text">' +
                        item.course_description +
                        "</p>" +
                        "</div>" +
                        '<div class="card-footer">' +
                        "<center>" +
                        '<a href="/course_description/' +
                        item.id +
                        '" class="btn btn-primary">Book Now</a>' +
                        "</center>" +
                        "</div>" +
                        "</div>" +
                        "</div>";

                    $("#course-list").append(html);
                }
                else {
                    html =
                        '<div class="col-md-6 col-lg-3 courses_list">' +
                        '<div class="card">' +
                        "<center>" +
                        '<div class="card-header">' +
                        "<span>" +
                        item.course_title +
                        "</span>" +
                        "</div>" +
                        "</center>" +
                        '<div class="card-body">' +
                        //                               '<h5 class="card-title">Special title treatment</h5>'+
                        '<p class="card-text">' +
                        item.course_description +
                        "</p>" +
                        "</div>" +
                        '<div class="card-footer">' +
                        "<center>" +
                        '<a href="https://docs.google.com/forms/d/1XDXsFBIIZYA86V5aHihyjGXlKJ4bKOm0XpDXVCYQkP8/viewform?edit_requested=true/' +
                    
                        '" class="btn btn-primary" target="_blank">Book Now</a>' +
                        "</center>" +   
                        "</div>" +
                        "</div>" +
                        "</div>";

                    $("#course-list").append(html);
                }

            });
        },
        error: function (data) {
            console.log(data);
            //                $('#error-msg').text(data.responseJSON.status);
        },
    });
});
