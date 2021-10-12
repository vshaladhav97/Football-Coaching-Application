console.log("helloooo");
$(document).ready(function () {
    var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)

    $.ajax({
        type: 'get',
        url: '/cart_add/',
        headers: { Authorization: 'Bearer ' + access.access },
        data: {},
        success: function(data) {
            var cartItemCount = 0
            jQuery.each(data.data, function (i, item) {
              cartItemCount = cartItemCount + parseInt(item.course.default_course_rate);
     
                html = `<tr class="item" id="product-${i}">
                    <input type="hidden"  name="product['id'][]" value="${item.id}">
                    <td>
                      <div class="product-cart-name"><a class="product-cart-media" href="product-page.html"><img src="${item.course.logo}" alt="" id="logo"></a>
                        <p class="product-cart-title" id="course-type">${item.course.course_type.course_name}</p>
                      </div>
                    </td>
                    <td>
                        <input class="form-input" id="avl-qty" readonly="readonly" value=${item.location.available_seats}>
                    </td>
                    <td>
                      <div class="stepper-modern">
                        <input class="form-input qty" name="product['qty'][]" type="number" data-zeros="true" id="qty" value="1" min="1" oninput="calc()">
                      </div>
                    </td>
                    <td>
                      <div class="product-cart-price">$<span id="price" class="price">${item.course.default_course_rate}</span></div>
                    </td>
                    <td>
                      <div class="product-cart-delete"><span class="icon fl-bigmug-line-recycling10" onclick="deleteItem(${item.id})"></span></div>
                    </td>
                </tr>`
                $('#courses').append(html);

            });

            html = `<span>${cartItemCount}</span>`
            $("#total-payment").append(html);
        },
        error: function(data) {
            console.log(data);

            },
        });

})


function deleteItem(id){
    var token = sessionStorage.getItem("UserDetails");
    var access = JSON.parse(token)

    $.ajax({
        type: 'delete',
        url: '/cart_delete/'+id,
        headers: { Authorization: 'Bearer ' + access.access },
        data: {

        },
        success: function(data) {
            localStorage.removeItem('location_id');
            location.reload();
        },
        error: function(data) {
            console.log(data);
//                $('#error-msg').text(data.responseJSON.status);
            },
        });
}

  function calc() {
    total = 0
        $('.item').each(function() {
//            var qty = $("input[name=qty]").val();
//            var price = $("input[name=price]").val();
//            var total = Number(qty) * Number(price);
//            $(this).find('.price').text(total);

             var row = $(this).closest("tr");

            // Get the values from _this row's_ inputs, using `row.find` to
            // look only within this row
            var qty = parseFloat(row.find('.qty').val());
            var price = parseFloat(row.find('.price').text());
            console.log(qty, price);
            total += parseInt(qty) * parseInt(price);

            console.log(total);

        });

        $('#total-price').text(total);
    }