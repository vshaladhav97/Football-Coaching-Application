$(document).ready(function () {

    var data = JSON.parse(localStorage.getItem("course_detail"));

    if (data !== null){
        var qty = data[0].qty;
        if(parseInt(qty) <= 0){
            localStorage.removeItem('course_detail');
        }
    }


    $.ajax({
        type: 'post',
        url: '/cart/',
        data: {
            'location_id': localStorage.getItem('location_id'),
            'course_id': localStorage.getItem('course_id'),
         },
        success: function(data) {
            if(data.data != null || data.data != undefined){
                $('#logo').attr('src', data.data.course_detail.logo);
                $('#course-type').text(data.data.course_detail.course_type.course_name);
                $('#avl-qty').val(data.data.maximum_capacity);
                $('#qty').attr('max', data.data.maximum_capacity);
                $('#price').text(data.data.course_detail.default_course_rate);
                $('#total-price').text(data.data.course_detail.default_course_rate);

    //            course_detail = JSON.localStorage.getItem('course_detail')
    //            if (course_detail !== null){
    //                course_to_book = course_detail
    //            }
    //            else{
                course_to_book = [];
    //            }

                course_to_book.push({
                    location_id: localStorage.getItem('location_id'),
                    course_id: localStorage.getItem('course_id'),
                    course_type: data.data.course_detail.course_type.course_name,
                    aval_qty: data.data.available_seats,
                    qty: $('#qty').val(),
                    price: data.data.course_detail.default_course_rate,
                    logo: data.data.course_detail.logo
                })
                localStorage.setItem('course_detail', JSON.stringify(course_to_book))
                }
        },
        error: function(data) {
                $('#location').text(data.responseJSON.status);
            },
        });
})

$('#qty').on('change', function () {

    var value = $(this).val();
    var max = parseInt($('#avl-qty').val());
    var price = parseInt($('#price').text());


    if ((value !== '') && (value.indexOf('.') === -1)) {

        $(this).val(Math.max(Math.min(value, max), -max));
        var course_detail = JSON.parse(localStorage.course_detail);
        course_detail[0].qty = Math.max(Math.min(value, max), -max);  //add two
        localStorage.setItem("course_detail", JSON.stringify(course_detail));
        var value = parseInt($(this).val());
        console.log(price, value);
        $('#total-price').text(price * value);
    }


});


function checkout(){
    let formData = new FormData($("#cart-add")[0]);
    var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)
    if (token == null){
      window.location.href = "/"
    }
    $.ajax({
        type: 'post',
        url: '/cart_update/',
        headers: { Authorization: 'Bearer ' + access.access },
        enctype: 'multipart/form-data',
        data : formData,
        contentType : false,
        processData: false,
        async : false,
        success: function(data) {
            console.log(data);
            window.location.href = "/student_add/"
        },
        error: function(data) {
            console.log(data);
           },
        });
}