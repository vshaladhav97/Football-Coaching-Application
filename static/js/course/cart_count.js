$(document).ready(function () {
    var token = sessionStorage.getItem("UserDetails");

    if (token != undefined){
        var access_token = JSON.parse(token);
        $.ajax({
            type: 'get',
            url: '/dashboard_counts/',
            headers: { Authorization: 'Bearer ' + access_token.access },
            success: function(data) {
                data = JSON.parse(data.data);
                $('.cart-value').text(data.cart_count);
                localStorage.setItem("cartCount", data.cart_count);
                cartCount = localStorage.getItem('cartCount')
                console.log(cartCount, "test");
                if (parseInt(cartCount) != 0){
                    $('#goBack').css('display','none');
                    html = '<button class="button button-sm button-primary" id="checkOut" onclick="checkout();"  style="margin-top:0px;">Checkout</button>';
                }
                else{
                    $('#checkOut').css('display','none');
                    html = '<a href="/courses" id="goBack" class="button button-sm button-primary update-cart">Go back</a>';
                }
                $('#cart-buttons').append(html);
            },
            error: function(data) {
                console.log(data);
               },
        });
    }
})