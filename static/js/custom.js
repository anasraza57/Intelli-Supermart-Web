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
