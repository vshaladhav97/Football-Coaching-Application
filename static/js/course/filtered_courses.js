
//<div class="card-standing-team-country"><b>Age Group</b> :${item.age_group.age_group_text}</div>
$('#date').on('change', function() {
    var location_id = $('#location-id').val();
    var course_id = $('#course-id').val();
    var month = $('#date').val();
    $.ajax({
        type: 'post',
        url: '/get_class_on_month/',
        data: {
            'location_id': location_id,'course_id': course_id, 'month': month,
//            'month': month,
        },
        success: function(data) {
            $('#accordion1Heading1').remove();
            $('#classes').empty();
            if (data.data.length == 0){
                $('#classes').append("No match found for your criteria");
            }
            jQuery.each(data.data, function (i, item) {

            html =  `<div class="card-header" id="accordion1Heading1" role="tab">
                        <div class="card-standing-team-item">
                          <div class="card-standing-team">
                            <div class="card-standing-team-title">
                              <div class="card-standing-team-name"><b>Course</b> :${item.course_type.course_name}</div>

                              <div class="card-standing-team-country"><b>Description</b> :${item.course_description}</div>
                              <div class="card-standing-team-country"><b>Location</b> :${data.location.location}</div>
                            </div>
                          </div>
                          <div class="card-standing-diff price">$ ${item.default_course_rate}</div>
                          <div class="card-standing-button">
                              <button type="button" class="btn btn-primary" onclick="book(${item.id}, ${data.location.id}, ${item.default_course_rate})">Add to cart</button>
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
});
