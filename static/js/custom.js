
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
        error: function(){
            swal("Couldn't add to cart","Please try again later", "error");
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
        error: function() {
            swal("Couldn't update the cart","Please try again later", "error");
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
        error: function(){
            swal("Couldn't delete from cart","Please try again later", "error");
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
        error: function(){
            swal("Couldn't add to wishlist","Please try again later", "error");
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
        error: function(){
            swal("Couldn't delete from wishlist","Please try again later", "error");
        }
    });

});

function disablePlaceOrderButton(){
    $("#placeOrderButton").attr("disabled", true);
    $("#placeOrderButton").css('cursor', 'default');
    $("#placeOrderButton").css('background-color', 'grey');
}

$('#placeOrderButton').on('click', function(){
    disablePlaceOrderButton();
    firstName = $('#firstName').val();
    lastName = $('#lastName').val();
    email = $('#email').val();
    gender = $('#gender').val();
    address = $('#address').val();
    city = $('#city').val();
    zipcode = $('#zipCode').val();
    grandTotal = $('#grandTotal').val();
    $.ajax({
        url: '/checkout',
        type: 'POST',
        data:{'firstName' : firstName, 'lastName' : lastName, 'email' : email, 'gender' : gender,
        'address' : address, 'city' : city, 'zipCode' : zipcode, 'grandTotal' : grandTotal},
        success: function(result) {
            swal("Your oder is Placed!","", "success");
            window.location.reload();
        },
        error: function(){
            swal("Your oder isn't Placed!","Please try again later", "error");
            window.location.replace("/");
        }
    });
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
