
$(function(){
    $('.pagination li').first().next().addClass("active1");
    var $li = $('.pagination li').click(function(){
//        alert();
//        $li.removeClass('active1');
//        $(this).addClass('active1');
    });

    $('.next').click(function(){
        $('.pagination').find('.pageNumber.active1').next().addClass('active1');
        $('.pagination').find('.pageNumber.active1').prev().removeClass('active1');
    });

    $('.prev').click(function(){
        $('.pagination').find('.pageNumber.active1').prev().addClass('active1');
        $('.pagination').find('.pageNumber.active1').next().removeClass('active1');
    });

//    var $a = $('.addFocus').find('.temp');
//    if $a.attr('href') == $a.html(){
//        $a.css('color', #5B3F91);
//    }
});


$('.addToCartButton').on("click", function(){
    prod_id = $(this).attr("name");
    quan= "quantity" + prod_id;
    quantity = $('input[name='+quan+']').val();
    $.ajax({
        url: '/cart',
        type: 'POST',
        data:{'product_id' : prod_id, 'quantity': quantity},
        success: function(result) {
            window.location.reload();
        },
        failure: function(){
            alert("failed");
        }
    });
});

$('.updateInCartButton').on("click", function(){
    prod_id = $(this).attr("name");
    quan= "quantity" + prod_id;
    quantity = $('input[name='+quan+']').val();

    $.ajax({
        url: '/updateCart',
        type: 'PUT',
        data:{'id' : prod_id, 'quantity': quantity},
        success: function(result) {
            $('.total'+prod_id).html("Rs " + result['total']);
            $('.grand_total').html("Rs " + result['grand_total']);
        }
    });

});

$('.deleteFromCartButton').on("click", function(){
    prod_id = $(this).attr("name");
    $.ajax({
        url: '/deleteFromCart',
        type: 'DELETE',
        data:{'product_id' : prod_id},
        success: function(result) {
            window.location.reload();
        },
        failure: function(){
            alert("failed");
        }
    });

});

$('.addToWishlistButton').on("click", function(){
    prod_id = $(this).attr("name");
    $.ajax({
        url: '/wishlist',
        type: 'POST',
        data:{'product_id' : prod_id},
        success: function(result) {
            window.location.reload();
        },
        failure: function(){
            alert("failed");
        }
    });
});

$('.deleteFromWishlistButton').on("click", function(){
    prod_id = $(this).attr("name");
    $.ajax({
        url: '/deleteFromWishlist',
        type: 'DELETE',
        data:{'product_id' : prod_id},
        success: function(result) {
            window.location.reload();
        },
        failure: function(){
            alert("failed");
        }
    });

});

$('#placeOrderButton').on('click', function(){
    alert("Order is Placed!")
});

//$('#loginBtn').on("click", function () {
//    swal({
//        title: "Phone Number Verification",
//        text: "Enter your mobile number to Login/SignUp:",
//        content: "input",
//        buttons: {
//            confirm: "Next"
//        },
//        animation: "slide-from-top"
//    }).then(val => {
//        if (val) {
//            swal({
//                title: "Phone Number Verification",
//                text: "Enter 4 digit code to your phone\n" + val,
//                content: "input"
//            }).then(val2 => {
//                if (val2) {
//                    swal({
//                        title: "Thanks!",
//                        text: "Logged In",
//                        icon: "success"
//                    });
//                }
//            });
//        }
//    });
//});
