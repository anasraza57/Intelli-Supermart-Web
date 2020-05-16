
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
            if (result == "duplicate"){
                swal("Couldn't add to wishlist","This product is already in cart!", "warning");
            }else{
                swal({
                    title: "Added!",
                    text: "This product is added to cart.",
                    icon: "success",
                })
                .then((value) => {
                    window.location.reload();
                });
            }
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
            swal("Updated","This product is updated to wishlist", "success");
        },
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
            swal({
                title: "Deleted!",
                text: "This product is deleted from cart.",
                icon: "success",
            })
            .then((value) => {
                window.location.reload();
            });
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
            if (result == "duplicate"){
                swal("Couldn't add to wishlist","This product is already in wishList!", "warning");
            }else{
                swal("Added","This product is added to wishlist", "success");
                window.location.reload();
            }
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
            swal({
                title: "Deleted!",
                text: "This product is deleted from wishlist.",
                icon: "success",
            })
            .then((value) => {
                window.location.reload();
            });
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
            swal({
                title: "Congrats!",
                text: "Your order is Placed.",
                icon: "success",
            })
            .then((value) => {
                window.location.reload();
            });
        },
        error: function(){
            swal({
                title: "Your oder isn't Placed!",
                text: "Please try again later.",
                icon: "error",
            })
            .then((value) => {
                window.location.replace("/");
            });
        }
    });
});

$('#submit').on('click', function(){
    $('#contact-form').submit(function(){
        $.ajax({
            url: $('#contact-form').attr('action'),
            type: 'POST',
            data : $('#contact-form').serialize(),
            success: function(result){
                swal({
                    title: "Your message has been sent!",
                    text: "We will contact you shortly.",
                    icon: "success"
                });
            },
            error: function(){
                swal({
                    title: "Your message has not been sent!",
                    text: "Please try again later.",
                    icon: "error",
                })
                .then((value) => {
                    window.location.replace("/");
                });
            }
        });
        return false;
    });
});