$(document).ready(function () {
    var course_type_id = localStorage.getItem("course_type_id", course_type_id);
    // var course_id = $('#course-id').val()
    var course_id = course_type_id
    console.log(course_id);
    $.ajax({
        type: 'get',
        url: '/get_location/' + course_id,
        data: {},
        success: function(data) {
            jQuery.each(data.company_name, function (i, item) {
                $('#venue').append("<option value=" + item.location +">" + item.location__location + "</option>")
            });
        },
        error: function(data) {
                $('#venue').text(data.responseJSON.status);
            },
    });
    $.ajax({
        type: 'get',
        url: '/get_company_name/' + course_id,
        data: {},
        success: function(data) {
            jQuery.each(data.company_name, function (i, item) {
                $('#company').append("<option value=" + item.location__company__id +">" + item.location__company__company_name + "</option>")
            });
        },
        error: function(data) {
                $('#company').text(data.responseJSON.status);
            },
    });
    $.ajax({
        type: 'get',
        url: '/course_detail_data/'+course_id,
        data: {},
        success: function(data) {
            $('#course-name').text(data.data.course_title);
            // $('#course-detail').text(data.data.course_description);
            $('#course-type-logo').css('background-image', "url(" + data.data.logo + ")");
            // jQuery.each(data.data.course_details, function (i, item) {
            //     $('#location').append("<option value=" + item.location.id +">" + item.location.location + "</option>")
            //     $('#date').append("<option value=" + item.location.company.id +">" + item.location.company.company_name + "</option>")
            // });
            // jQuery.each(data.data, function (i, item) {
            //     $('#date').append("<option value=" + item.id +">" + item.month + "</option>")
            // });
        },
        error: function(data) {
                $('#location').text(data.responseJSON.status);
            },
        });

    // $.ajax({
    //     type: 'get',
    //     url: '/course_category_detail/'+course_id,
    //     data: {},
    //     success: function(data) {
    //         $('#course-name').text(data.data.course_name);
    //         $('#course-detail').text(data.data.course_description);
    //         // $('#course-type-logo').css('background-image', "url(" + data.data.logo + ")");
    //     },
    //     error: function(data) {
    //             $('#location').text(data.responseJSON.status);
    //         },
    //     });

});

$('#search').click(function(){
   month = $('#date').val();
   id = $('#location').val();
   var course_id = $('#course-id').val()
   localStorage.setItem('location_id',id)
   if(parseInt(id) == 0){
        toastr.error("Please select location")
        return false;
   }
   if(parseInt(month) == 0){
        toastr.error("Please select date")
        return false;
   }
   $.ajax({
        type: 'get',
        url: '/filtered_course_data/'+id+'/'+course_id+'/'+month,
        data: {},
        success: function(data) {
        $('#classes').empty();
        if (data.data.length == 0){
            $('#classes').append("No match found for your criteria");
        }
        jQuery.each(data.data, function (i, item) {
            console.log(item);


            var months = ""

//            jQuery.each(item.course_detail.course_months, function (i, item) {
//               months = months + "," + item.month.month;
//            })
//            console.log(months);
//<div class="card-standing-team-country"><b>Age Group</b> :${item.age_group.age_group_text}</div>
//  <div class="card-standing-team-country"><b>Months</b> : ${months} </div>
            html =  `<div class="card-header" id="accordion1Heading1" role="tab">
                        <div class="card-standing-team-item">
                          <div class="card-standing-team">
                            <div class="card-standing-team-title">
                              <div class="card-standing-team-name"><b>Course</b> :${item.course_type.course_name}</div>

                              <div class="card-standing-team-country"><b>Description</b> :${item.course_description}</div>
                              <div class="card-standing-team-country"><b>Location</b> :${item.location.location}</div>

                            </div>
                          </div>
                          <div class="card-standing-diff price">$ ${item.default_course_rate}</div>
                          <div class="card-standing-button">
                              <button type="button" class="btn btn-primary" onclick="book(${item.id}, ${item.location.id}, ${item.default_course_rate})">Add to cart</button>
                          </div>
                        </div>
                    </div>`
                $('#classes').append(html);
             });
        },
        error: function(data) {
                $('#location').text(data.responseJSON.status);
            },
        });
})

function book(courseId, locationId, amount){
    var token = sessionStorage.getItem("UserDetails");

    if (token == undefined) {
        toastr.error("Please login");
    }
    var access = JSON.parse(token)

    localStorage.setItem('course_id',courseId)
    localStorage.setItem('location_id', locationId);
    $.ajax({
        type: 'post',
        url: '/cart_add/',
        headers: { Authorization: 'Bearer ' + access.access },
        data: {
            'course': courseId,
            'location': locationId,
            'amount': amount,
        },
        success: function(data) {
            window.location.href = '/cart/';
        },
        error: function(data) {
            console.log(data);
        }
    });
}

//$('#location').change(function() {
//    $.ajax({
//        type: 'get',
//        url: '/locations/'+this.value,
//        data: {},
//        success: function(data) {
//            $('#course-type-logo').css('background-image', "url(" + data.data.logo + ")");
//        },
//        error: function(data) {
//                $('#location').text(data.responseJSON.status);
//            },
//        });
//})