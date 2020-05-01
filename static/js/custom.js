
$('.pagination').on("click", function() {
    alert();
});

$('.updateButton').on("click", function(){
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

$('.deleteButton').on("click", function(){
    prod_id = $(this).attr("name");
    $.ajax({
        url: '/deleteFromCart',
        type: 'DELETE',
        data:{'id' : prod_id},
        success: function(result) {
            window.location.reload();
        },
        failure: function(){
            alert("failed");
        }
    });

});

$('#loginBtn').on("click", function () {
    swal({
        title: "Phone Number Verification",
        text: "Enter your mobile number to Login/SignUp:",
        content: "input",
        buttons: {
            confirm: "Next"
        },
        animation: "slide-from-top"
    }).then(val => {
        if (val) {
            swal({
                title: "Phone Number Verification",
                text: "Enter 4 digit code to your phone\n" + val,
                content: "input"
            }).then(val2 => {
                if (val2) {
                    swal({
                        title: "Thanks!",
                        text: "Logged In",
                        icon: "success"
                    });
                }
            });
        }
    });
});
